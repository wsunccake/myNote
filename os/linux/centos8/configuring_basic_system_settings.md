# configuring basic system settings

## getting started with system administration

### web console

```bash
centos:~ # dnf install cockpit
centos:~ # systemctl enable --now cockpit.socket
centos:~ # ss -lutnp | grep 9090

centos:~ # firewall-cmd --permanent --add-service=cockpit
centos:~ # firewall-cmd --reload
```

browser <ip>:9090

```bash
# change port
centos:~ # vi /usr/lib/systemd/system/cockpit.socket
[Socket]
ListenStream=9090

centos:~ # systemctl daemon-reload
centos:~ # systemctl restart cockpit.socket

# prevent root
centos:~ # vi /etc/pam.d/cockpit
auth       requisite    pam_succeed_if.so uid >= 1000  # add this to 1st line

# setup
centos:~ # vi /etc/cockpit/cockpit.conf
[Session]
Banner=/etc/issue.cockpit
IdleTimeout=3

centos:~ # vi /etc/issue.cockpit
This is an example banner for the RHEL web console login page.

centos:~ # systemctl try-restart cockpit
```


### time

```bash
centos:~ # timedatectl
centos:~ # date
```


### local

```bash
centos:~ # localectl status

centos:~ # localectl list-locales
centos:~ # localectl set-locale LANG=en-US

centos:~ # localectl list-keymaps
centos:~ # localectl set-keymap us
```

### network

```bash
centos:~ # nmcli connection add <con-name> <ex-con> ifname <interface> type ethernet
centos:~ # nmcli connection show <ex-con>

# ipv4
centos:~ # nmcli connection modify <ex-con> ipv4.addresses 192.0.2.1/24
centos:~ # nmcli connection modify <ex-con> ipv4.gateway 192.0.2.254
centos:~ # nmcli connection modify <ex-con> ipv4.dns "192.0.2.200"
centos:~ # nmcli connection modify <ex-con> ipv4.dns-search example.com
centos:~ # nmcli connection modify <ex-con> ipv4.method manual

# ipv6
centos:~ # nmcli connection modify <ex-con> ipv6.addresses 2001:db8:1::1/64
centos:~ # nmcli connection modify <ex-con> ipv6.gateway 2001:db8:1::fffe
centos:~ # nmcli connection modify <ex-con> ipv6.dns "2001:db8:1::ffbb"
centos:~ # nmcli connection modify <ex-con> ipv6.dns-search example.com
centos:~ # nmcli connection modify <ex-con> ipv6.method manual

centos:~ # nmcli connection up <ex-con>
centos:~ # nmcli connection down <ex-con>
centos:~ # nmcli device status

centos:~ # nmtui
```


## systemd

```bash
centos:~ # systemctl enable <service>
centos:~ # systemctl enable --now <service>
centos:~ # systemctl disable <service>
centos:~ # systemctl status <service>

centos:~ # systemctl unmask <service>
centos:~ # systemctl mask <service>
```

### selinux

```bash
centos:~ # getenforce
centos:~ # setenforce Enforcing
centos:~ # setenforce Permissive

centos:~ # cat /etc/selinux/config
```


### account

```bash
centos:~ # id
centos:~ # useradd <user>
centos:~ # passwd <user>
centos:~ # usermod -aG <group> <user>
```


### recove and restore

```bash
centos:~ # dnf install rear genisoimage syslinux
centos:~ # rear mkrescue
centos:~ # vi /etc/rear/local.conf
BACKUP=NETFS
BACKUP_URL=backup.location
NETFS_KEEP_OLD_BACKUP_COPY=y
BACKUP_TYPE=incremental
```


### log file

/var/log/messages - all syslog messages except the following
/var/log/secure - security and authentication-related messages and errors
/var/log/maillog - mail server-related messages and errors
/var/log/cron - log files related to periodically executed tasks
/var/log/boot.log - log files related to system startup

```bash
centos:~ # journalctl -b
centos:~ # journalctl -k -b -1
```


---

## managing software packages

### list

```bash
# search package
centos:~ # yum search <term>
centos:~ # yum search --all <term>

# list package
centos:~ # yum list --all
centos:~ # yum list --installed
centos:~ # yum list --available

# list repository
centos:~ # yum repolist
centos:~ # yum repolist --disabled
centos:~ # yum repolist --all
centos:~ # yum repoinfo

centos:~ # yum info <package-name>

# list package group
centos:~ # yum group summary
centos:~ # yum group list
centos:~ # yum group info <group-name>

centos:~ # yum provides "*/<file-name>"
centos:~ # yum provides \*/<ile-name>
```


### install

```bash
# install package
centos:~ # yum install <package-name>
centos:~ # yum install <package-name-1> <package-name-2>
centos:~ # yum install <package-name>.<arch>
centos:~ # yum install /usr/sbin/<binary-file>
centos:~ # yum install /<path>/

# install package group
centos:~ # yum group install <group-name>
centos:~ # yum install @<group-name>
centos:~ # yum group install <groupID>

centos:~ # yum install-n <name>
centos:~ # yum install-na <name>.<architecture>
centos:~ # yum install-nevra <name-epoch>:<version-release>.<architecture>
```


### update

```bash
centos:~ # yum check-update
centos:~ # yum update <package-name>
centos:~ # yum group update <group-name>
centos:~ # yum update
centos:~ # yum update --security
centos:~ # yum update-minimal --security
```


### auto update

```bash
centos:~ # yum install dnf-automatic
centos:~ # rpm -qi dnf-automatic
centos:~ # vi /etc/dnf/automatic.conf

centos:~ # systemctl enable dnf-automatic-download.timer
centos:~ # systemctl start dnf-automatic-download.timer
centos:~ # systemctl enable dnf-automatic-install.timer
centos:~ # systemctl start dnf-automatic-install.timer
centos:~ # systemctl enable dnf-automatic-notifyonly.timer
centos:~ # systemctl start dnf-automatic-notifyonly.timer
centos:~ # systemctl enable dnf-automatic.timer
centos:~ # systemctl start dnf-automatic.timer
```


### remove

```bash
centos:~ # yum remove <package-name>
centos:~ # yum remove <package-name-1> <package-name-2>
centos:~ # yum group remove <group-name>
centos:~ # yum remove @<group-name>
centos:~ # yum group remove <groupID>

centos:~ # yum remove-n <name>
centos:~ # yum remove-na <name>.<architecture>
centos:~ # yum remove-nevra <name-epoch>:<version-release>.<architecture>
```


### history

```bash
centos:~ # yum history
centos:~ # yum history list <package-name>
centos:~ # yum history info <transactionID>
centos:~ # yum history undo <transactionID>
centos:~ # yum history undo last
centos:~ # yum history redo <transactionID>
centos:~ # yum history redo last
```


### repository

```bash
centos:~ # yum-config-manager --add-repo <repository_URL>
centos:~ # yum-config-manager --enable <repositoryID>
centos:~ # yum-config-manager --disable <repositoryID>
```


### configure

```bash
centos:~ # yum config-manager --dump
centos:~ # yum --noplugins update
centos:~ # yum update --disableplugin=<plugin-name>
```


---

## managing services with systemd


/usr/lib/systemd/system/ - Systemd unit files distributed with installed RPM packages.
/run/systemd/system/ - Systemd unit files created at run time. This directory takes precedence over the directory with installed service unit files.
/etc/systemd/system/ - Systemd unit files created by systemctl enable as well as unit files added for extending a service. This directory takes precedence over the directory with runtime unit files.


`service mapping systemctl`

```
service <name> start                systemctl start <name>.service
service <name> stop                 systemctl stop <name>.service
service <name> restart              systemctl restart <name>.service
service <name> condrestart          systemctl try-restart <name>.service
service <name> reload               systemctl reload <name>.service
service <name> status               systemctl status <name>.service
                                    systemctl is-active <name>.service
service --status-all                systemctl list-units --type service --all
```


`chkconfig mapping systemctl`

```
chkconfig <name> on                 systemctl enable <name>.service
chkconfig <name> off                systemctl disable <name>.service
chkconfig --list <name>             systemctl status <name>.service
                                    systemctl is-enabled <name>.service
chkconfig --list                    systemctl list-unit-files --type service
chkconfig --list                    systemctl list-dependencies --after
chkconfig --list                    systemctl list-dependencies --before
```


`sysv mapping systemctl`

```
0                                   runlevel0.target, poweroff.target
1                                   runlevel1.target, rescue.target
2                                   runlevel2.target, multi-user.target
3                                   runlevel3.target, multi-user.target
4                                   runlevel4.target, multi-user.target
5                                   runlevel5.target, graphical.target
6                                   runlevel6.target, reboot.target

runlevel                            systemctl list-units --type target
telinit runlevel                    systemctl isolate name.target
```


`shutting down, suspending, and hibernating mapping systemctl`

```
halt                                systemctl halt
poweroff                            systemctl poweroff
reboot                              systemctl reboot
pm-suspend                          systemctl suspend
pm-hibernate                        systemctl hibernate
pm-suspend-hybrid                   systemctl hybrid-sleep
```


```bash
centos:~ # systemctl stop nfs-server.service
centos:~ # systemctl stop nfs-server
centos:~ # systemctl show nfs-server.service -p Names

centos:~ # chroot /srv/website1
centos:~ # systemctl enable httpd.service

centos:~ # systemctl list-units --type service
centos:~ # systemctl list-units --type service --all
centos:~ # systemctl list-unit-files --type service

centos:~ # systemctl status <name>.service
centos:~ # systemctl is-active <name>.service
centos:~ # systemctl is-enabled <name>.service
centos:~ # systemctl list-dependencies --after <name>.service
centos:~ # systemctl list-dependencies --before <name>.service

centos:~ # systemctl start name.service
centos:~ # systemctl stop name.service
centos:~ # systemctl restart name.service
centos:~ # systemctl try-restart name.service
centos:~ # systemctl reload name.service
centos:~ # systemctl enable name.service
centos:~ # systemctl reenable name.service
centos:~ # systemctl disable name.service
centos:~ # systemctl mask name.service
centos:~ # systemctl unmask name.service

centos:~ # systemctl list-units --type target
centos:~ # systemctl list-units --type target --all

centos:~ # systemctl get-default
centos:~ # systemctl set-default multi-user.target
centos:~ # systemctl isolate multi-user.target

centos:~ # ls -l /lib/systemd/system/default.target
centos:~ # ln -sf /lib/systemd/system/graphical.target 

centos:~ # systemctl rescue
centos:~ # systemctl emergency
centos:~ # systemctl isolate emergency.target
centos:~ # systemctl --no-wall emergency

centos:~ # systemctl poweroff
centos:~ # systemctl halt
centos:~ # systemctl --no-wall poweroff
centos:~ # shutdown --poweroff hh:mm
centos:~ # shutdown --halt +m
centos:~ # shutdown -c
centos:~ # systemctl reboot
centos:~ # systemctl --no-wall reboot
centos:~ # systemctl suspend
centos:~ # systemctl hibernate
centos:~ # systemctl hybrid-sleep
```


### custom unit file

```bash
centos:~ # touch /etc/systemd/system/<name>.service
centos:~ # chmod 664 /etc/systemd/system/<name>.service
centos:~ # vi /etc/systemd/system/<name>.service
[Unit]
Description=service_description
After=network.target

[Service]
ExecStart=<path_to_executable>
Type=forking
PIDFile=<path_to_pidfile>

[Install]
WantedBy=default.target

centos:~ # systemd-delta
centos:~ # systemctl daemon-reload
centos:~ # systemctl start <name>.service
```


### optimizing systemd to boot time

```bash
centos:~ # systemctl list-unit-files --state=enabled
centos:~ # systemd-analyze
centos:~ # systemd-analyze blame
centos:~ # systemd-analyze critical-chain

centos:~ # systemctl cat <service_name>
centos:~ # systemctl help <service_name>
```


---

## introduction to managing user and group accounts

```bash
centos:~ # cat /usr/share/doc/setup*/uidgid
centos:~ # cat /etc/login.defs
UID_MIN
GID_MIN
```


---

## managing users from the command line

```bash
centos:~ # useradd -u 5000 sarah
centos:~ # id sarah
centos:~ # groupadd -g 5000 sysadmins
centos:~ # cat /etc/group
centos:~ # usermod --append -G system-administrators sysadmin
centos:~ # groups sysadmin

centos:~ # groupadd <group-name>
centos:~ # usermod --append -G <group-name> <username>
centos:~ # chown :<group-name> <directory-name>
centos:~ # chmod g+rwxs <directory-name>
```


---

## removing a user from a group from the command line

```bash
centos:~ # usermod -g sarah2 sarah
centos:~ # groups sarah

centos:~ # usermod -G developer sarah
centos:~ # groups sarah
```


---

## managing sudo access

```bash
centos:~ # cat /etc/sudoers
centos:~ # visudo
centos:~ # usermod --append -G wheel sarah
centos:~ # id sarah
```


---

## changing and resetting the root password

```bash
centos:~ # passwd
```

### forget root password

```bash
# when grub menu

# e

# ctrl + e

load_video
set gfx_payload=keep
insmod gzio
linux ($root)/vmlinuz-4.18.0-80.e18.x86_64 root=/dev/mapper/rhel-root ro crash\
kernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv/swap rhab quiet
initrd ($root)/initramfs-4.18.0-80.e18.x86_64.img $tuned_initrd


->

load_video
set gfx_payload=keep
insmod gzio
linux ($root)/vmlinuz-4.18.0-80.e18.x86_64 root=/dev/mapper/rhel-root ro crash\
kernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv/swap rhab quiet rd.break
initrd ($root)/initramfs-4.18.0-80.e18.x86_64.img $tuned_initrd

# ctrl + x

sh:~ $ mount -o remount,rw /sysroot
sh:~ $ chroot /sysroot
sh:~ $ passwd
sh:~ $ touch /.autorelabel
sh:~ $ exit
sh:~ $ exit
```


---

## managing file permissions

```bash
# mode
centos:~ # ls -l
centos:~ # ls -ld
centos:~ # chmod u+x,g-w,o= my-file.txt
centos:~ # chmod a=rwx my-file
centos:~ # chmod -R g-wx,o= /my-directory

# umask
centos:~ # echo $0
bash           # login shell        -> /etc/profile
-bash          # non-login shell    -> /etc/bashrc
centos:~ # grep umask /etc/profile
centos:~ # grep umask /etc/bashrc

centos:~ # vi /etc/login.defs
UMASK

centos:~ # umask
centos:~ # umask -S
centos:~ # umask -S u+x,g-w,o=
centos:~ # umask a=rwx

# acl
centos:~ # setfacl -m u:andrew:rw- group-project
centos:~ # setfacl -m u:susan:--- group-project
centos:~ # getfacl group-project
```


---

## using the chrony suite to configure ntp

```bash
centos:~ # yum install chrony
centos:~ # systemctl status chronyd
centos:~ # systemctl start chronyd
centos:~ # systemctl enable chronyd

centos:~ # systemctl stop chronyd
centos:~ # systemctl disable chronyd

centos:~ # chronyd -q 'server ntp.example.com iburst'
centos:~ # python3 /usr/share/doc/chrony/ntp2chrony.py -b -v

centos:~ # vi /etc/chrony.conf
allow 192.0.2.0/24
allow 2001:0db8:85a3::8a2e:0370:7334

centos:~ # firewall-cmd --permanent --zone=public --add-port=123/udp
centos:~ # firewall-cmd --reload

centos:~ # chronyc tracking        # checking if chrony is synchronized
centos:~ # chronyc sources         # checking chrony source
centos:~ # chronyc sourcestats     # checking chrony source statistics
centos:~ # chronyc makestep        # manually adjusting the system clock
centos:~ # chronyc ntpdata         # reporting the transmit, receive timestamping and interleaved mode for each NTP source
```


---

## using secure communications between two systems with openssh

### configuring and starting an openssh server

```bash
centos:~ # systemctl start sshd
centos:~ # systemctl enable sshd
centos:~ # vi /etc/ssh/sshd_config

centos:~ # vi /etc/issue

centos:~ # vi /etc/motd

centos:~ # systemctl daemon-reload
centos:~ # systemctl status sshd

centos:~ # ssh <user>@<ssh-server-example.com>
```


### using key pairs instead of passwords for ssh authentication

```bash
centos:~ # vi /etc/ssh/sshd_config
PasswordAuthentication no

centos:~ # setsebool -P use_nfs_home_dirs 1   # NFS-mounted home dir for SELinux
centos:~ # systemctl reload sshd
```


### generating ssh key pairs

```bash
centos:~ # ssh-keygen -t ecdsa
centos:~ # ls ~/.ssh/
centos:~ # ssh-copy-id <user>@<ssh-server-example.com>

centos:~ # ssh <user>@<ssh-server-example.com>
centos:~ # ls ~/.ssh/
```


### using ssh keys stored on a smart card

```bash
centos:~ # ssh-keygen -D pkcs11: > keys.pub
centos:~ # ssh-keygen -D pkcs11:
centos:~ # ssh-copy-id -f -i keys.pub <user>@<example.com>
```

