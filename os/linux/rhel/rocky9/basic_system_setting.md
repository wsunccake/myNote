# basic system settings

## cockpit / web console

```bash
rocky:~ # dnf install cockpit
rocky:~ # systemctl enable --now cockpit
rocky:~ # firewall-cmd --add-service=cockpit --permanent
rocky:~ # firewall-cmd --reload

rocky:~ # curl https://localhost:9090

rocky:~ # cat /etc/pam.d/cockpit

rocky:~ # ls /etc/cockpit
rocky:~ # vi /etc/cockpit/cockpit.conf
rocky:~ # vi /etc/cockpit/disallowed-users
rocky:~ # systemctl try-restart cockpit
```

---

## network

```bash
rocky:~ # nmcli connection show
rocky:~ # nmcli connection add con-name <connection-name> ifname <device-name> type ethernet
rocky:~ # nmcli connection modify <connection-name> connection.id <connection-name>
rocky:~ # nmcli connection show <connection-name>

# ipv4
rocky:~ # nmcli connection modify <connection-name> ipv4.method auto # dhcp
rocky:~ # nmcli connection modify <connection-name> ipv4.method manual ipv4.addresses 192.0.2.1/24 ipv4.gateway 192.0.2.254 ipv4.dns 192.0.2.200 ipv4.dns-search example.com # static

# ipv6
rocky:~ # nmcli connection modify <connection-name> ipv6.method auto # slaac
rocky:~ # nmcli connection modify <connection-name> ipv6.method manual ipv6.addresses 2001:db8:1::fffe/64 ipv6.gateway 2001:db8:1::fffe ipv6.dns 2001:db8:1::ffbb ipv6.dns-search example.com # static

rocky:~ # nmcli connection modify <connection-name> <setting> <value>
rocky:~ # nmcli connection up <connection-name>
rocky:~ # nmcli device status

rocky:~ # nmtui
```

```bash
rocky:~ # ip address show <interface>
rocky:~ # ip route show default
rocky:~ # ip -6 route show default
rocky:~ # cat /etc/resolv.conf
rocky:~ # ping <host-name-or-IP-address>
rocky:~ # ls /etc/NetworkManager/system-connections
```

---

## basic environment

```bash
# hostname
rocky:~ # hostnamectl
rocky:~ # hostnamectl hostname <hostname>

# date & time
rocky:~ # date
rocky:~ # timedatectl
rocky:~ # systemctl enable systemd-timedated
rocky:~ # timedatectl set-ntp true|false
rocky:~ # timedatectl list-timezones
rocky:~ # timedatectl set-timezone Asia/Taipei
rocky:~ # timedatectl status
rocky:~ # timedatectl help

# system locale
rocky:~ # localectl list-locales
rocky:~ # localectl status
rocky:~ # localectl set-locale LANG=en_US

# keyboard layout
rocky:~ # localectl list-keymaps
rocky:~ # localectl status
rocky:~ # localectl set-keymap us

# font size in text console mode
rocky:~ # setfont /usr/lib/kbd/consolefonts/LatArCyrHeb-19.psfu.gz
rocky:~ # setfont -d LatArCyrHeb-16
rocky:~ # cat /etc/vconsole.conf
rocky:~ # rpm -ql kbd-misc | grep LatAr
```

---

## openssh

```bash
# ssh key pair
ssh-client:~ $ ssh-keygen -t ecdsa
ssh-client:~ $ ssh-copy-id <username>@<ssh-server-example.com>
ssh-client:~ $ ssh -o PreferredAuthentications=publickey <username>@<ssh-server-example.com>

# only key-based authentication
ssh-server:~ # grep PasswordAuthentication /etc/ssh/sshd_config
PasswordAuthentication no
ssh-server:~ # setsebool -P use_nfs_home_dirs 1 # enable nfs-mounted home folder for selinux
ssh-server:~ # systemctl reload sshd

# ssh-agent
ssh-client:~ $ grep ssh-agent ~/.bashrc
eval $(ssh-agent)
ssh-client:~ $ grep AddKeysToAgent ~/.ssh/config
AddKeysToAgent yes
ssh-client:~ $ ssh <example.user>@<ssh-server@example.com>
```

---

## user and group

```bash
cat /usr/share/doc/setup*/uidgid
grep UID_MIN /etc/login.defs
grep GID_MIN /etc/login.defs

# user private group (UPG) system
cat /etc/group

# manage account and group
rocky:~ # id <example.user>

rocky:~ # groupadd [-g <gid>] <example.group>
rocky:~ # tail /etc/group

rocky:~ # useradd [-u <uid>] <example.user>
rocky:~ # passwd <example.user>
rocky:~ # usermod -a -G <example.group> <example.user>
rocky:~ # groups <example.group>
```

---

## sudo

```bash
# user authorizations in sudoer
rocky:~ # cat /etc/sudoers
Defaults   !visiblepw
Defaults    always_set_home
Defaults    match_group_by_gid
Defaults    always_query_group_plugin
Defaults    env_reset
Defaults    env_keep =  "COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS"
Defaults    env_keep += "MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE"
Defaults    env_keep += "LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES"
Defaults    env_keep += "LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE"
Defaults    env_keep += "LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY"
Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin
root	ALL=(ALL) 	ALL
%wheel	ALL=(ALL)	ALL

rocky:~ # visudo

# grant sudo access to user
rocky:~ # usermod --append -G wheel <username>
rocky:~ # id <username>

# enable unprivileged users to run certain commands
rocky:~ # mkdir -p /etc/sudoers.d/
rocky:~ # visudo -f /etc/sudoers.d/<filename>
# <username> <hostname.example.com> = (<run_as_user>:<run_as_group>) <path/to/command>
Defaults    mail_always
Defaults    mailto="<email@example.com>"
user1 host1.example.com = /bin/dnf, /sbin/reboot

```

```bash
rocky:~ $ sudo -i
rocky:~ $ sudo su -
rocky:~ $ sudo <command>
```

---

## repo

```bash
rocky:~ # dnf install epel-release
```

### dnf

```bash
# repo
rocky:~ # dnf repolist [--all]
rocky:~ # dnf repoinfo
rocky:~ # dnf config-manager [--enable|--disable] <repo-id>
rocky:~ # dnf config-manager --add-repo <url>|<file> repo
rocky:~ # ls /etc/yum.repos.d
```
