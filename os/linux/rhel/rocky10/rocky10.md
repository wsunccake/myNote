# rocky linux 10

## system

### network

```bash
# connection
rocky:~ # nmcli connection [show]
rocky:~ # nmcli connection add con-name <connection-name> ifname <device-name> type ethernet
rocky:~ # nmcli connection modify <connection-name> connection.id <connection-name>
rocky:~ # nmcli connection show <connection-name>

# ipv4 - dhcp
rocky:~ # nmcli connection modify <connection-name> ipv4.method auto
# ipv4 - static
rocky:~ # nmcli connection modify <connection-name> ipv4.method manual ipv4.addresses 192.0.2.1/24 ipv4.gateway 192.0.2.254 ipv4.dns 192.0.2.200 ipv4.dns-search example.com

# ipv6 - slaac
rocky:~ # nmcli connection modify <connection-name> ipv6.method auto
# ipv6 - static
rocky:~ # nmcli connection modify <connection-name> ipv6.method manual ipv6.addresses 2001:db8:1::fffe/64 ipv6.gateway 2001:db8:1::fffe ipv6.dns 2001:db8:1::ffbb ipv6.dns-search example.com

rocky:~ # nmcli connection modify <connection-name> <setting> <value>
rocky:~ # nmcli connection edit [con-name]
nmcli> print [ipv4|all]
nmcli> describe ipv4.method
nmcli> set ipv4.method auto
nmcli> set connection.id eth0               # con-name
nmcli> set connection.interface-name eth0   # ifname
nmcli> set 802-11-wireless.mtu auto         # 只有目前設定會改變, 但未套用
nmcli> save                                 # 將設定寫入 ifcfg-ifname, 並套用
nmcli> quit

rocky:~ # nmcli connection up|down <connection-name>

# device
rocky:~ # nmcli device [status|show]
rocky:~ # nmcli device up|down <device-name>

# networking
rocky:~ # nmcli netorking
rocky:~ # nmcli netorking on|off

rocky:~ # nmtui
```

### cockpit

```bash
rocky:~ # dnf install cockpit

rocky:~ # systemctl enable --now cockpit
rocky:~ # firewall-cmd --add-service=cockpit --permanent
rocky:~ # firewall-cmd --reload

rocky:~ # cat /etc/pam.d/cockpit

rocky:~ # ls /etc/cockpit
rocky:~ # vi /etc/cockpit/cockpit.conf
rocky:~ # vi /etc/cockpit/disallowed-users
rocky:~ # systemctl try-restart cockpit

rocky:~ # curl http://127.0.0.1:9090
```

### repository

```bash
rocky:~ # dnf makecache
# --nogpgcheck              停用 GPG 簽名檢查
# --setopt=sslverify=false  停用 SSL 憑證驗證
# --assumeyes               自動將所有的詢問都回答為 "yes"

# repo
rocky:~ # dnf install epel-release
rocky:~ # dnf repolist --all
rocky:~ # dnf config-manager --set-enabled epel-testing
rocky:~ # dnf config-manager --set-enabled crb
```

---

## cli

```bash
rocky:~ # dnf install bash-completion bash-color-prompt
rocky:~ # dnf install vim-common vim-enhanced
rocky:~ # dnf install git
```

---

## scheduling system

### slurm

- [SchedMD](https://www.schedmd.com/)

`require`

```bash
rocky:~ # dnf install munge munge-devel                 # repo: appstream, crb
rocky:~ # dnf install readline-devel mariadb-devel      # repo: appstream
rocky:~ # dnf install perl perl-devel
rocky:~ # dnf install pam-devel rpm-build rpmdevtools
rocky:~ # dnf group install development
```

`build`

```bash
rocky:~ $ curl -LO https://download.schedmd.com/slurm/slurm-25.11.1.tar.bz2
rocky:~ $ rpmbuild -ta slurm-25.11.1.tar.bz2

rocky:~ $ ls rpmbuild/RPMS/x86_64/
```

---

## ESXi

ESXi 7.0 搭配 Rocky Linux 10.1 (核心版本通常為 6.x) 算是一個比較尷尬的組合。雖然 ESXi 7.0 支援 VMXNET3，但 Rocky 10 的核心非常新，兩者在 TSO (TCP Segmentation Offload) 的協議溝通上偶爾會出現不同步。

1. 關閉網卡加速功能

常見的解決方案。VMXNET3 在處理大封包卸載時，如果 ESXi 沒能及時處理，網卡驅動會因為傳輸佇列超時（TX Timeout）而直接掛死。

```bash
# 立即生效
rocky:~ # ethtool -K <eth> tso off gso off lro off gro off
rocky:~ # ethtool -k ens256

# 永久生效
rocky:~ # vi /etc/NetworkManager/dispatcher.d/99-disable-offload
#!/bin/bash
if [ "$1" = "<eth>" ] && [ "$2" = "up" ]; then
    /usr/sbin/ethtool -K <eth> tso off gso off lro off gro off
fi

rocky:~ # chmod +x /etc/NetworkManager/dispatcher.d/99-disable-offload
```

| Item | Full Name                    | ethtool -k                   | 說明                                     |
| ---- | ---------------------------- | ---------------------------- | ---------------------------------------- |
| TSO  | TCP Segmentation Offload     | tcp-segmentation-offload     | 由網卡分段大封包，減輕 CPU 負擔。        |
| GSO  | Generic Segmentation Offload | generic-segmentation-offload | TSO 的通用軟體版本，處理非 TCP 封包。    |
| LRO  | Large Receive Offload        | large-receive-offload        | 將收到的多個小封包合併成大封包再給核心。 |
| GRO  | Generic Receive Offload      | generic-receive-offload      | LRO 的改進版，更安全且通用。             |

2. 停用 IPv6 嘗試

日誌看到 dhcp6 正在背景不斷嘗試。在某些 ESXi 虛擬交換器環境下，重複的 IPv6 鄰居發現請求（NS/NA）可能導致 VMXNET3 發生異常重置。

```bash
rocky:~ # journalctl -u NetworkManager -n 100
rocky:~ # journalctl -u NetworkManager --since "YYYY-MM-DD" | grep -i <eth>
rocky:~ # journalctl -u NetworkManager --since "hh:mm" | grep -E -i "<eth>|fail|error|down"

# 立即停用 IPv6
rocky:~ # sysctl -w net.ipv6.conf.all.disable_ipv6=1
rocky:~ # sysctl -w net.ipv6.conf.default.disable_ipv6=1

# 永久停用 IPv6
rocky:~ # echo "net.ipv6.conf.all.disable_ipv6 = 1" | tee -a /etc/sysctl.conf
rocky:~ # echo "net.ipv6.conf.default.disable_ipv6 = 1" | tee -a /etc/sysctl.conf
rocky:~ # sysctl -p
```

3. 停用「省電機制」

在 ESXi 7.0 上運行較新的 Linux 核心，常因 C-States (電源狀態) 轉換導致核心掛起。

```bash
rocky:~ # vi /etc/default/grub
GRUB_CMDLINE_LINUX='... intel_idle.max_cstate=1 processor.max_cstate=1 pcie_aspm=off'

rocky:~ # grub2-mkconfig -o /boot/grub2/grub.cfg
```

4. 防止「靜默崩潰」

當系統死鎖時，預設情況下它會停在原地。調整核心參數，讓系統在崩潰時自動重啟，並將資訊寫入日誌。

```bash
rocky:~ # vi /etc/sysctl.conf
kernel.panic = 10               # 遇到 Kernel Panic 時，10 秒後自動重啟
kernel.softlockup_panic = 1     # 偵測到 Soft Lockup (某個 CPU 被卡住) 時觸發 Panic
kernel.hung_task_panic = 1      # 偵測到 hung task (超過 120 秒沒回應的任務) 時觸發 Panic

rocky:~ # sysctl -p
```
