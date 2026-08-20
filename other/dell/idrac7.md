# iDrac 7

root/calvin

## IPMI Over LAN

1. Dell iDRAC 7 基於安全性考量，許多韌體版本預設關閉了遠端 IPMI LAN 功能。

- iDRAC 7 Web 管理介面，前往 iDRAC Settings $\rightarrow$ Network $\rightarrow$ 找到 IPMI Settings，將 Enable IPMI Over LAN 勾選開啟（Apply）。

2. 密碼錯誤，或者 root 帳號沒有被授予 IPMI LAN 存取權限，也會回傳此錯誤。

- 測試預設帳密： Dell 12G 伺服器 (iDRAC 7) 預設為 root / calvin。
- 確認權限： 在 iDRAC Web 介面中的 iDRAC Settings $\rightarrow$ User Sessions / Users，確認 root 帳號的 LAN 權限為 Administrator 且啟用。

3. 使用 RACADM

```bash
/admin1-> racadm config -g cfgIpmiLan -o cfgIpmiLanEnable 1
/admin1-> racadm set iDRAC.IPMILan.Enable 1
```

---

## SSH

1. iDRAC Settings $\rightarrow$ Network $\rightarrow$ 切換到頁面頂部的 Services 分頁。
2. 找到 SSH Key / SSH 相關設定區塊：
   - SSH Enabled：勾選 Enabled (啟用)。
   - SSH Port：確認埠號（預設為 22）。
   - Max Sessions：建議維持預設（通常為 4 或 8）。

---

## IPMI

---

## RACADM

RACADM (Remote Access Controller Admin) 是 Dell 專為 iDRAC 開發的命令列管理工具。簡單來說，它就是「不用開 Web 網頁介面，直接用 Terminal / Command Line 控制 Dell 伺服器」的工具。

[RACADM](./racadm.md)

---

## Script

[idrac_functions.sh](./idrac_functions.sh)
[idrac_cmd.sh](./idrac_cmd.sh)

---

## Kick Start

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

---

## Boot ISO

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
