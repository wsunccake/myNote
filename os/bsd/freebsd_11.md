
# VM tool

open-vm-tools, vmware-tools 在 vmware 中只要安裝一個即可

## open-vm-tools

```bash
# install
freebsd:~ # pkg install open-vm-tools-nox11

# enable service
freebsd:~ # vi /etc/rc.conf
vmware_guest_vmblock_enable="YES"
vmware_guest_vmhgfs_enable="YES"
vmware_guest_vmmemctl_enable="YES"
vmware_guest_vmxnet_enable="YES"
vmware_guestd_enable="YES"
freebsd:~ # reboot

# list kernel module
freebsd:~ # kldstat
```

## vmware-tools

```bash
# install
freebsd:~ # mount -t cd9660 /dev/cd0 /media/
freebsd:~ # tar zxf /media/vmware-freebsd-tools.tar.gz -C /tmp/
freebsd:~ # umount /media
freebsd:~ # /tmp/vmware-tools-distrib/vmware-install.pl

# list kernel module
freebsd:~ # kldstat

# remove
freebsd:~ # vmware-uninstall-tools.pl
```

vmware-tools rc script in /usr/local/etc/rc.d


---

# Disk & Filesystem

## gpart

```bash
freebsd:~ # gpart show
freebsd:~ # gpart list
freebsd:~ # gpart status
```


## zfs

```
freebsd:~ # zpool list
freebsd:~ # zpool status
```


---

# Startup

## service

```bash
# list service
freebsd:~ # service -l

# service
freebsd:~ # service <service> status
freebsd:~ # service <service> start
freebsd:~ # service <service> stop

freebsd:~ # service <service> restart
freebsd:~ # service <service> onerestart
freebsd:~ # service <service> rcvar


# enable/disable service
freebsd:~ # vi /etc/rc.conf
<service>_enable="YES"
```

service rc script: /etc/rc.d, /usr/local/etc/rc.d

necessary: dbus, sshd

option: clear_tmp


## fs

```bash
freebsd:~ # mount -t procfs proc /proc

freebsd:~ # vi /etc/fstab
proc			/proc	procfs	rw		0	0
```


## console

```bash
freebsd:~ # kldstat -m vesa
freebsd:~ # vidcontrol show
freebsd:~ # vidcontrol -i mode
freebsd:~ # vidcontrol -i active
freebsd:~ # vidcontrol -i adapter

freebsd:~ # vidcontrol MODE_377

freebsd:~ # vi /etc/rc.conf
allscreens_flags="MODE_377"
```


## keyboard

```bash
freebsd:~ # kbdmap
```


## nic

```bash
# for dynamic ip
freebsd:~ # vi /etc/rc.conf
ifconfig_dc0="DHCP"


# for static ip
freebsd:~ # vi /etc/rc.conf
ifconfig_dc0="inet 192.168.1.3 netmask 255.255.255.0"
defaultrouter="192.168.1.1"

# setup dns
freebsd:~ # vi /etc/resolv.conf
nameserver 8.8.8.8


# restart service
freebsd:~ # service netif restart
freebsd:~ # service routing restart
```


---

# Account Manage

## pw

```bash
# 使用者 新增 移除
freebsd:~ # pw useradd <user>
freebsd:~ # pw userdel <user>

# 使用者 資訊
freebsd:~ # pw usershow <user>

# 使用者 加入 群組
freebsd:~ # pw usermod <user> -G <group>

freebsd:~ # pw usernext


# 群組 新增 移除
freebsd:~ # pw groupadd <group>
freebsd:~ # pw groupdel <group>

# 群組 資訊
freebsd:~ # pw groupshow <group>

# 使用者 加入 群組
freebsd:~ # pw groupmod <group> -M <user>
freebsd:~ # pw groupmod <group> -m <user>

# 使用者 移除 群組
freebsd:~ # pw groupmod <group> -d <user>

freebsd:~ # pw groupnext
```


## inactive

```bash
# 使用者 新增
freebsd:~ # adduser

# 使用者 移除
freebsd:~ # rmuser

# 使用者 更新設定
freebsd:~ # chpass
```


---

# Package Manage

## port

```bash
freebsd:~ # cd /usr/ports
freebsd:/usr/ports # make index
freebsd:/usr/ports # make search name=lsof

# install package
freebsd:/usr/ports/sysutils/lsof # make install

# remove package
freebsd:/usr/ports/sysutils/lsof # make deinstall
```


## pkg

```bash
# list package
freebsd:~ # pkg info [<pkg>]
freebsd:~ # pkg list [<pkg>]

# find package
freebsd:~ # pkg search <pkg>

# install pakcage
freebsd:~ # pkg install <pkg>

# remvoe package
freebsd:~ # pkg remove <pkg>
```


---

# GUI

## xorg

```bash
# install xorg
freebsd:~ # pkg install xorg
freebsd:~ # pkg install xf86-video-vmware

# clear previous setup
freebsd:~ # rm /usr/local/etc/X11/xorg.conf
freebsd:~ # rm /etc/X11/xorg.conf

# configure
freebsd:~ # Xorg -configure
freebsd:~ # X -config /root/xorg.conf.new
freebsd:~ # mv xorg.conf.new /usr/local/etc/X11/xorg.conf

# test gui
freebsd:~ # startx

# test resolution
freebsd:~ # xrandr
```


## font

```bash
freebsd:~ # pkg install urwfonts
freebsd:~ # xset fp+ /usr/local/share/fonts/urwfonts
freebsd:~ # xset fp rehash

freebsd:~ # pkg install mkfontdir
freebsd:~ # xset fp rehash

freebsd:~ # fc-cache -f
```


## xfce

```bash
# install
freebsd:~ # pkg install xfce

# configure
freebsd:~ # echo "exec /usr/local/bin/startxfce4 --with-ck-launch" > ~/.xinitrc

# run
freebsd:~ # startxfce4
```
