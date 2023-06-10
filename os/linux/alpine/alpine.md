# alpine

## setup

```bash
~ # setup-alpine
```

---

## network

```bash
alpine:~ # cat /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
        address 192.168.10.11
        netmask 255.255.255.0
        gateway 192.168.10.1

alpine:~ # setup-interfaces
alpine:~ # setup-dns
alpine:~ # setup-hostname
```

---

## gui

### xorg

```bash
alpine:~ # setup-xorg-base

alpine:~ # X -configure
alpine:~ # mv xorg.conf.new /etc/X11/xorg.conf
```

### xfce

```bash
alpine:~ # apk add xfce4 xfce4-terminal xfce4-screensaver lightdm-gtk-greeter
alpine:~ # rc-service dbus start
alpine:~ # rc-update add dbus
alpine:~ # startx
```

### dm

```bash
alpine:~ # rc-service lightdm start
alpine:~ # rc-update add lightdm
```

### awesome

```bash
alpine:~ # apk add awesome feh lxterminal
alpine:~ # apk add lua
alpine:~ # apk add adwaita-gtk2-theme adwaita-icon-theme
alpine:~ # start /usr/bin/awesome
```

### i3

```bash
alpine:~ # apk add i3wm i3status i3lock
alpine:~ # startx /usr/bin/i3
```

### mouse

```bash
alpine:~ # udevadm info --name=/dev/input/mouse0  --query=path
alpine:~ # cat /proc/bus/input/devices
```

---

## apk

```bash
alpine:~ # setup-apkcache
alpine:~ # setup-apkrepos
alpine:~ # vi /etc/apk/repositories

alpine:~ # apk update
alpine:~ # apk search <pkg>
alpine:~ # apk info [-L|-P] [<pkg>]     # installed package
alpine:~ # apk list [<pkg>]             # available package
alpine:~ # apk stats

alpine:~ # apk add <pkg>       # install package
alpine:~ # apk del <pkg>       # uninstall package

alpine:~ # apk cache clean

# ie
alpine:~ # apk search mlocate
alpine:~ # apk add mlocate
alpine:~ # apk del mlocate
```

---

## openrc

```bash
# install openrc
alpine:~ # apk add openrc

# usage openrc
alpine:~ # rc-status [-a]
alpine:~ # rc-status -l        # list runlevel
alpine:~ # rc-service -l       # list service
alpine:~ # rc-service <service> start|stop|status|restart
alpine:~ # rc-update add|del <service> [<runlevel>]
alpine:~ # rc-update show [-v]

# ie
alpine:~ # apk add dropbear
alpine:~ # rc-service --list
alpine:~ # rc-service dropbear start
alpine:~ # rc-service dropbear stop
alpine:~ # rc-service dropbear status
alpine:~ # rc-update add dropbear
alpine:~ # rc-update del dropbear
alpine:~ # rc-status
```

---

## dropbear / ssh

```bash
alpine:~ # apk add dropbear

alpine:~ # cat /etc/conf.d/dropbear
```
