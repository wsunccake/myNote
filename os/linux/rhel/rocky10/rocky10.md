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
