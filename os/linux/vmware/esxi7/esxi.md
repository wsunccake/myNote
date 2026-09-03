# ESXi

在 VMware ESXi 中，DCUI、TSM 與 TSM-SSH 是維運人員用來管理與存取 ESXi 主機的 三大核心控制管道。

1. DCUI (Direct Console User Interface)

- 中文名稱：直連控制台使用者介面
- 介面型態：黃黑相間的文字選單（基於 Curses 繪圖）
- 定位與用途：
  - 實體主機的最後一道防線。主要透過伺服器接接的螢幕/鍵盤，或是 iDRAC / iLO 的 Virtual Console 進行操作。
  - 基礎網路與系統配置：用於設定 ESXi 的 Management IP、VLAN ID、DNS、修改 root 密碼，以及執行 Network Restore（重置網路）、重啟主機或檢視 Log。
  - 安全性：選單式操作，不提供開放性的 Shell 命令列，適合日常維護與極限救援。

  ```bash
  # ESXi
  export TERM=linux
  dcui
  ```

2. TSM (ESXi Shell / Technical Support Mode)

- 中文名稱：ESXi 本地指令列殼層 (Technical Support Mode)
- 介面型態：Linux 風格的黑底白字 Console 命令列 (CLI)
- 定位與用途：
  - 本機直連的高級除錯介面。
  - 在實體機（或 iDRAC）的 DCUI 介面按下 Alt + F1 時，跳出的黑底 Shell 命令列就是 TSM。
  - 可以在沒有網路、無法透過 SSH 連線時，直接在主機面前輸入 esxcli、vim-cmd 等底層指令來排除高難度的硬體或系統故障。

3. TSM-SSH (SSH Access)

- 中文名稱：遠端 SSH 服務
- 介面型態：遠端網路連線 (Port 22) 的黑底白字命令列
- 定位與用途：
  - 遠端高級維運與自動化介面。
  - 底層與 TSM 完全相同（都是 ESXi Shell），但允許維運人員透過網路（如 PuTTY、PowerShell、MobaXterm 等工具）遠端登入 ESXi 主機。
  - 預設狀態：出於資安考量，ESXi 安裝完成後 TSM 與 TSM-SSH 預設皆為關閉 (Off)。開啟 SSH 時，ESXi Web UI 會跳出黃色警告標語提示潛在風險。

  ```bash
  # ESXi
  mkdir -p
  echo <PUB KEY> >> /etc/ssh/keys-root/authorized_keys
  chmod 600 /etc/ssh/keys-root/authorized_keys
  ```

| 項目         | DCUI                   | TSM (ESXi Shell)        | TSM-SSH                 |
| ------------ | ---------------------- | ----------------------- | ----------------------- |
| 主要連線管道 | 實體螢幕 / iDRAC / KVM | 實體機按 Alt + F1       | 遠端 Port 22 (SSH)      |
| 操作介面     | 黃黑圖形化文字選單     | 本機 Linux 提示符號 (#) | 遠端 Linux 提示符號 (#) |
| 功能範圍     | 基本網路/密碼/重啟設定 | 完全控制（底層指令）    | 完全控制（底層指令）    |
| 預設狀態     | 開啟 (On)              | 關閉 (Off)              | 關閉 (Off)              |
| 主要權限     | 一般維運 / 初步救援    | 高級除錯 / 系統修復     | 遠端自動化 / 批次維護   |

---

## Basic

- basic

```bash
vmware -v

passwd

reboot
poweroff
```

- storage

```bash
cd /vmfs/volumes/
esxcli storage filesystem list
esxcli storage core device list
```

- network

```bash
esxcli network ip interface ipv4 get
esxcli network nic list
esxcli network vswitch standard list
```

- log

```bash
tail -f /var/log/syslog.log
tail -f  /var/log/vmkernel.log
```

- other

```bash
# ESXi 6.x / 7.x
pam_tally2 --user root
pam_tally2 --user root --reset

# ESXi 8.0+
faillock --user root
faillock --user root --reset
```

---

## Kick Start

### config

`ks.cfg`

```bash
vmaccepteula

clearpart --firstdisk --overwritevmfs
install --firstdisk --overwritevmfs

rootpw <PASSWORD>

keyboard 'US Default'
network --bootproto=dhcp --device=vmnic0 --addvmportgroup=0

reboot

%firstboot --interpreter=busybox

vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/start_ssh

vim-cmd hostsvc/enable_esx_shell
vim-cmd hostsvc/start_esx_shell
```

### boot iso + kick start

```bash
mkdir -p /tmp/esxi_iso /tmp/esxi_custom
mount -o loop VMware-VMca-7.0U3-xxxxxx-depot.iso /tmp/esxi_iso
cp -r /tmp/esxi_iso/* /tmp/esxi_custom/
chmod -R 755 /tmp/esxi_custom

vi /tmp/esxi_custom/ks.cfg
vi /tmp/esxi_custom/boot.cfg
vi /tmp/esxi_custom/efi/boot/boot.cfg

cd /tmp/esxi_custom
genisoimage -max-iso9660-filenames \
  -relaxed-filenames \
  -allow-limited-size \
  -l -J -r -volid "ESXI7_AUTO" \
  -b mboot.c32 \
  -c boot.cat \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -e efi/boot/bootx64.efi \
  -no-emul-boot \
  -o /var/www/html/esxi7-auto.iso .
```

`boot.cfg`

```bash
kernelopt=runweasel cdromBoot
=>
kernelopt=runweasel ks=http://<IP>/ks.cfg   # from http

kernelopt=runweasel ks=cdrom://ks.cfg       # from cdrom
```
