# debian 11

---

# package manager

## dpkg

```bash
debian:~ # dpkg -i <pkg>.deb   # install package
debian:~ # dpkg -l <pkg>       # search package
debian:~ # dpkg -r <pkg>       # remove package
debian:~ # dpkg -P <pkg>       # remove package and config

debian:~ # dpkg -c <pkg>.deb   # list .deb content
debian:~ # dpkg -L <pkg>       # list package content
debian:~ # dpkg -s <pkg>       # show package info
debian:~ # dpkg -S <path>      # search package by <path>

# ie
debian:~ # dpkg -l curl
debian:~ # dpkg -l | grep curl
debian:~ # dpkg -i curl_7.64.0-4+deb10u2_amd64.deb
debian:~ # dpkg -r curl
debian:~ # dpkg -P curl

debian:~ # dpkg -L curl
debian:~ # dpkg -s curl
debian:~ # dpkg -S /usr/bin/curl
debian:~ # dpkg -S $(which curl)
debian:~ # dpkg -c curl_7.64.0-4+deb10u2_amd64.deb

# ar
debian:~ # ar t <pkg>.deb               # list package
debian:~ # ar x <pkg>.deb               # extract package
debian:~ # ar r <pkg>.deb <file>...     # create package
```

---

## apt

```bash
# package
debian:~ # apt-get update
debian:~ # apt-cache search <pkg>
debian:~ # apt-get install <pkg>
debian:~ # apt-get download <pkg>
debian:~ # apt-cache show <pkg>
debian:~ # apt-cache showpkg <pkg>

# repository
debian:~ # apt-cache policy [<pkg>]

# cd/dvd
debian:~ # apt-cdrom add

# check sum
debian:~ # sha256sum <image>.iso
debian:~ # cat SHA256SUMS.txt
<sha256sum> <image>.iso
debian:~ # sha256sum -c SHA256SUMS.txt

# iso
debian:~ # mkdir <mount_point>
debian:~ # mount -oloop <image>.iso <mount_point>
debian:~ # apt-cdrom -d=<mount_point> add

# config
debian:~ # /etc/apt/sources.list
deb url distribution component1 component2 component3 [..] componentX
deb-src url distribution component1 component2 component3 [..] componentX
->
deb http://ftp.tw.debian.org/debian/ bullseye main contrib non-free
deb-src http://ftp.tw.debian.org/debian/ bullseye main contrib non-free

debian:~ # /etc/apt/sources.list.d/*.list
```

### other tool

```bash
debian:~ # apt install aptitude synaptic
debian:~ # apt install software-properties-common
debian:~ # apt install debconf-utils
```

---

## debconf

```bash
debian:~ # debconf-show --listowners                           # -> /var/cache/debconf
debian:~ # debconf-show <pkg>
debian:~ # debconf-get-selections | grep ^<pkg> > <pkg>.conf
debian:~ # debconf-set-selections < <pkg>.conf

# ie.
debian:~ # export DEBIAN_FRONTEND=noninteractive
debian:~ # dpkg-reconfigure debconf     # interactive
debian:~ # debconf-show debconf
debian:~ # debconf-get-selections | grep ^debconf
debconf	debconf/frontend	select	Dialog
debconf	debconf/priority	select	medium
debian:~ # debconf-set-selections << EOF
debconf	debconf/frontend	select	Noninteractive
debconf	debconf/priority	select	high
```

---

# haredware

```bash
# cpu
debian:~ # lscpu
debian:~ # cat /proc/cpuinfo

# usb
debian:~ # lsusb

# pci
debian:~ # lspci -nn
debian:~ # lspci -k

# block
debian:~ # lsblk
debian:~ # lsblk -l
debian:~ # lsblk -p

# other
debian:~ # dmidecode
debian:~ # dmesg
debian:~ # sensors
```

---

# network

- en -- ethernet
- sl -- serial line IP (slip)
- wl -- wlan
- ww -- wwan

- b<number> -- BCMA bus core number
- ccw<name> -- CCW bus group name
- o<index> -- on-board device index number
- s<slot>[f<function>][d<dev_port>] -- hotplug slot index number
- x<MAC> -- MAC address
- [P<domain>]p<bus>s<slot>[f<function>][d<dev_port>] -- PCI geographical location
- [P<domain>]p<bus>s<slot>[f<function>][u<port>][..][c<config>][i<interface>] -- USB port number chain

## NetworkManager

```bash
debian:~ # systemctl start NetworkManager
debian:~ # systemctl enable NetworkManager
debian:~ # systemctl status NetworkManager

debian:~ # tree /etc/NetworkManager
/etc/NetworkManager
├── conf.d
├── dispatcher.d
│   ├── 01-ifupdown
│   ├── no-wait.d
│   ├── pre-down.d
│   └── pre-up.d
├── dnsmasq.d
├── dnsmasq-shared.d
├── NetworkManager.conf
└── system-connections
    └── <conn>

debian:~ # nmcli connection show
debian:~ # nmcli device status
debian:~ # nmcli device show <nic>

debian:~ # nmtui
```

---

## networking

```bash
debian:~ # systemctl start networking
debian:~ # systemctl enable networking
debian:~ # systemctl status networking

debian:~ # vi /etc/network/interfaces
auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet static
    address 192.168.0.10
    gateway 192.168.0.1
    netmask 255.255.255.0
    dns-nameserver 8.8.8.8
    dns-search site

debian:~ # ifquery --list
debian:~ # ifdown <nic>
debian:~ # ifup <nic>
```

---

## systemd-networkd

```bash
debian:~ # systemctl enable systemd-networkd
debian:~ # systemctl start systemd-networkd
debian:~ # systemctl status systemd-networkd

debian:~ # ls /etc/systemd/network
debian:~ # ls /etc/systemd/networkd.conf
debian:~ # networkctl list
debian:~ # networkctl status
debian:~ # networkctl up <device>
debian:~ # networkctl down <device>
```

---

# date time

## timezone

```bash
debian:~ # date
debian:~ # date +%m%d%Y
debian:~ # echo $TZ

# setup time zone
debian:~ # dpkg-reconfigure tzdata
debian:~ # ls /etc/timezone
debian:~ # ls /usr/share/zoneinfo
debian:~ # ls -l /etc/localtime

debian:~ # timedatectl status
debian:~ # timedatectl list-timezones
debian:~ # timedatectl set-timezone UTC

# sync time
debian:~ # systemctl enable systemd-timesyncd
debian:~ # systemctl start systemd-timesyncd
debian:~ # systemctl status systemd-timesyncd

debian:~ # timedatectl set-ntp true
debian:~ # timedatectl show-timesync --all
debian:~ # timedatectl timesync-status
```

---

## ntp

```bash
debian:~ # vi /etc/default/ntpdate
```

---

# env

## locale

```bash
debian:~ # locale

debian:~ # localectl status
debian:~ # localectl set-locale LANG=en_US.UTF-8

debian:~ # dpkg-reconfigure locales
debian:~ # debconf-show locales
* locales/locales_to_be_generated: en_US.UTF-8 UTF-8, zh_TW.UTF-8 UTF-8     # /etc/locale.gen
* locales/default_environment_locale: en_US.UTF-8                           # /etc/default/locale

debian:~ # cat /etc/locale.gen
debian:~ # cat /etc/default/locale
```

---

## hostname

```bash
debian:~ # systemctl enable systemd-hostnamed
debian:~ # systemctl start systemd-hostnamed
debian:~ # systemctl status systemd-hostnamed

debian:~ # hostname
debian:~ # echo $HOSTNAME

debian:~ # hostnamectl status
debian:~ # hostnamectl set-hostname <hostname>

debian:~ # cat /etc/hostname               # hostname
debian:~ # cat /proc/sys/kernel/hostname   # hostname
debian:~ # cat /etc/hosts                  # name
debian:~ # cat /etc/resolv.conf            # dns
debian:~ # cat /etc/nsswitch.conf
host:   ...
```

---

## shell

```bash
# bash
## for system
debian:~ # cat /etc/bash.bashrc    # interactive
debian:~ # cat /etc/profile        # login

## for user
debian:~ # cat ~/.bashrc
debian:~ # cat ~/.bash_profile

# tcsh
debian:~ # cat /etc/csh.cshrc
debian:~ # cat /etc/csh.login
debian:~ # cat /etc/csh.logout

# zsh
debian:~ # cat /etc/zshrc
debian:~ # cat /etc/zshenv
```

---

## update-alternatives

```bash
debian:~ # update-alternatives --get-selections
debian:~ # update-alternatives --list <name>
debian:~ # update-alternatives --display <name>
debian:~ # update-alternatives --config <name>

# ie
debian:~ # update-alternatives --get-selections
debian:~ # update-alternatives --list editor
debian:~ # update-alternatives --display editor
debian:~ # update-alternatives --config editor

debian:~ # ls /var/lib/dpkg/alternatives
```

---

# account

## user and group

```bash
# user
debian:~ # password [<user>]       # change password
debian:~ # password -e <user>      # expire
debian:~ # password -l <user>      # lock
debian:~ # password -u <user>      # unlock

debian:~ # usermod

debian:~ # vipw
debian:~ # chage

debian:~ # id
debian:~ # su - [<user>]
debian:~ # su <user> <command>

debian:~ # cat /etc/passwd
debian:~ # cat /etc/shadow

# group
debian:~ # gpasswd <group>
debian:~ # gpasswd -r <group>

debian:~ # groupmod

debian:~ # vigr

debian:~ # groups
debian:~ # sg - [<group>]
debian:~ # sg <group> <command>

debian:~ # cat /etc/group

debian:~ # cat /etc/nsswitch.conf
passwd: ...
group:  ...
shadow: ...

# get the entry
debian:~ # getent passwd
debian:~ # getent group

# perl sciprt
debian:~ # adduser
debian:~ # delser
debian:~ # addgroup <group>
debian:~ # delgroup
```

---

## permission

```bash
debian:~ # chmod <right> <file>
debian:~ # chown <user>[:<group>] <file>
debian:~ # chgrp <group> <file>

debian:~ # umask
```

---

## sudo

```bash
debian:~ # sudo
debian:~ # visudo
debian:~ # vi /etc/sudoers
debian:~ # usermod -aG sudo <user>
```

---

# tool

## mlocate

```bash
debian:~ # apt install mlocate

debian:~ # cat /etc/updatedb.conf
debian:~ # updatedb
debian:~ # locate <pattern>
```

---

## fix bug

```bash
debian:~ # diff -u file.old file.new > file.patch       # generat patch
debian:~ # patch -p0 file.old < file.patch              # patch file

debian:~ # patch -Np0 file.old < file.patch             # forward patch file
debian:~ # patch -Rp0 file.old < file.patch             # reverse patch file
```

---

# gui

## xorg

```bash
debian:~ # X -configure        # -> $HOME/xorg.conf.new
debian:~ # vi xorg.conf.new
debian:~ # cp xorg.conf.nen /etc/X11/xorg.conf
debian:~ # xdpyinfo
```

---

# system

## boot loader

```bash
# lilo
debian:~ # cat /etc/lilo.conf

# grub2
debian:~ # cat /boot/grub/grub.cfg
debian:~ # vi /etc/default/grub

debian:~ # grub-mkconfig > /boot/grub/grub.cfg
debian:~ # grub-install /dev/vda
debian:~ # grub-install --efi-directory=/mnt/efi
```

## mount

```bash
# mount
debian:~ # mount -vt proc proc /proc
debian:~ # mount -vt sysfs sysfs /sys
debian:~ # mount -vt tmpfs tmpfs /dev/shm
debian:~ # mount -vft devpts devpts /dev/pts

# chroot
debian:~ # mount --bind /dev /dev
debian:~ # mount --bind /sys /sys
debian:~ # mount --bind /proc /proc
```

---

## lograte

```bash
debian:~ # logrotate
debian:~ # cat /etc/logrotate.conf
debian:~ # ls /etc/logrotate.d/
```

---

## kerenl

```bash
debian:~ # uname -a

debian:~ # lsmod
debian:~ # insmod <module>
debian:~ # rmmod <module>
debian:~ # modinfo <module>
debian:~ # modprobe <module>
debian:~ # modprobe -r <module>
```

---

## systemd

```bash
debian:~ # ls /lib/systemd/system/
debian:~ # ls /etc/systemd/system/

debian:~ # systemctl status <service>
debian:~ # systemctl start <service>
debian:~ # systemctl stop <service>
debian:~ # systemctl enable <service>
debian:~ # systemctl disable <service>
debian:~ # systemctl is-active <service>
debian:~ # systemctl is-enabled <service>
debian:~ # systemctl is-failed <service>
debian:~ # systemctl daemon-reload <service>
debian:~ # systemctl cat <service>
debian:~ # systemctl edit [--full] <service>

debian:~ # systemctl list-units [--all] [--type target] [--state active]
debian:~ # systemctl list-unit-files
debian:~ # systemctl list-dependencies <service>

debian:~ # systemctl get-default
debian:~ # systemctl set-default <target>
debian:~ # systemctl isolate <target>

debian:~ # systemctl rescue
debian:~ # systemctl suspend
debian:~ # systemctl halt
debian:~ # systemctl poweroff
debian:~ # systemctl reboot

debian:~ # runlevel
debian:~ # who
```

---

# service

## sshd

```bash
debian:~ # systemctl start sshd
debian:~ # systemctl enable sshd
debian:~ # systemctl status sshd

debian:~ # ssh [<user>@]<server>
debian:~ # sftp [<user>@]<server>
debian:~ # scp [<user>@]<server> <src> <dest>

debian:~ # ssh-keygen -t rsa               # $HOME/.ssh/id_rsa.pub, $HOME/.ssh/id_rsa
debian:~ # ssh-copy-id  <server>           # $HOME/.ssh/authorized_keys
debian:~ # ssh-agent
debian:~ # eval "$(ssh-agent -s)"          # launch ssh-agent and set SSH_AGENT_PID variable
debian:~ # ssh-agent -k                    # terminate ssh-agent and unset SSH_AGENT_PID variable
debian:~ # ssh-add $HOME/.ssh/id_rsa       # add private key to ssh-agent
debian:~ # ssh-add -d $HOME/.ssh/id_rsa    # del private key to ssh-agent
debian:~ # ssh-add -l                      # list private key in ssh-agent
```

---

## cron, atd, anacron

---

## quota

---

```bash
debian-installer

# sdb is usb flash
cat debian-10.0.0-amd64-netinst.iso >/dev/sdb; sync
```
