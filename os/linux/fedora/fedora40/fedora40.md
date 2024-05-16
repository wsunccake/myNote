# fedora 40

---

## content

- [system](#system)
  - [dnf](#dnf)
  - [locale](#locale)
- [network](#network)
  - [network manager](#network-manager)
  - [systemd-networkd](#systemd-networkd)
- [desktop](#desktop)
  - [xfce](#xfce)
  - [gnome](#gnome)
  - [gdm](#gdm)
- [cli](#cli)
- [gui](#gui)

---

## system

### dnf

```bash
fedora:~ # dnf list
fedora:~ # dnf search <package>
fedora:~ # dnf info <package>

fedora:~ # dnf group list -v
fedora:~ # dnf group install <packge_group>
```

### locale

```bash
fedora:~ # dnf search langpacks-
fedora:~ # dnf install langpacks-en

fedora:~ # locale [-a]

fedora:~ # localectl
fedora:~ # localectl list-locales
fedora:~ # localectl set-locale en_US.UTF-8
fedora:~ # localectl set-locale LANG=locale
```

---

## network

### network manager

```bash
# service
fedora:~ # systemctl status NetworkManager

# config
fedora:~ # ls /etc/NetworkManager
fedora:~ # cat /etc/NetworkManager/system-connections/<con-name>.nmconnection
```

#### nmcli

```bash
fedora:~ # nmcli <object>
# objec:
# g[eneral]
# n[etworking]
# r[adio]
# c[onnection]
# d[evice]
# a[gent]
# m[onitor]

# help
fedora:~ # nmcli help
fedora:~ # nmcli <object> help
fedora:~ # nmcli <object> <command> help

# connection
fedora:~ # nmcli c show [<con-name>]
fedora:~ # nmcli c add con-name <con-name> ipv4.method <method> ifname <interface> type <type>
fedora:~ # nmcli c delete <con-name>
fedora:~ # nmcli c modify <ex-con> <key> <value>

### dhcp
fedora:~ # nmcli c add con-name enp0s1 ipv4.method auto type ethernet ifname enp0s1

### ipv4
fedora:~ # nmcli c add con-name enp0s1 ipv4.method manual type ethernet ifname enp0s1 \
  ipv4.addresses 192.0.2.10/24 ipv4.gateway 192.0.2.254 ipv4.dns 192.0.2.200

fedora:~ # nmcli c modify enp0s1 ipv4.addresses 192.0.2.10/24
fedora:~ # nmcli c modify enp0s1 ipv4.gateway 192.0.2.254
fedora:~ # nmcli c modify enp0s1 ipv4.dns 192.0.2.200
fedora:~ # nmcli c modify enp0s1 ipv4.dns-search example.com
fedora:~ # nmcli c modify enp0s1 ipv4.method manual

### bridge

# deivce
fedora:~ # nmcli d show [<con-name>]
```

#### nmtui

```bash
fedora:~ # dnf install NetworkManager-tui
fedora:~ # nmtui
```

### systemd-networkd

```bash
# package
fedora:~ # dnf install systemd-networkd

# service
fedora:~ # systemctl disable NetworkManager
fedora:~ # systemctl disable network

fedora:~ # systemctl enable systemd-networkd
fedora:~ # systemctl start systemd-networkd
fedora:~ # systemctl status systemd-networkd

fedora:~ # systemctl enable systemd-resolved
fedora:~ # systemctl start systemd-resolved
fedora:~ # rm -f /etc/resolv.conf
fedora:~ # ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf

# config
fedora:~ # ls /etc/systemd/network
fedora:~ # ls /etc/systemd/networkd.conf

# usage
fedora:~ # networkctl list
fedora:~ # networkctl status
fedora:~ # networkctl up <device>
fedora:~ # networkctl down <device>
```

---

## desktop

### xfce

```bash
fedora:~ # dnf group list -v --available | grep desktop
fedora:~ # dnf group install xfce-desktop-environment

fedora:~ # echo /usr/bin/startxfce4 > ~/.xinitrc
fedora:~ # startx
```

### gnome

```bash
fedora:~ # dnf group list -v --available | grep desktop
fedora:~ # dnf group install "Basic Desktop" GNOME

fedora:~ # echo /usr/bin/gnome-session > ~/.xinitrc
fedora:~ # echo "env GNOME_SHELL_SESSION_MODE=classic /usr/bin/gnome-session" >> ~/.xinitrc
fedora:~ # startx
```

### gdm

```bash
fedora:~ # ls -l /etc/systemd/system/default.target
fedora:~ # systemctl get-default
fedora:~ # systemctl set-default graphical.target # multi-user.target -> graphical.target
fedora:~ # systemctl isolate graphical.target
```

---

## cli

```bash
# zsh
fedora:~ # dnf install zsh

# oh my zsh
fedora:~ $ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fedora:~ $ ls ~/.oh-my-zsh/themes/
fedora:~ $ ls $ZSH/plugins

## config
fedora:~ $ vi ~/.zshrc
...
plugins=(git)
ZSH_THEME="robbyrussell"
```

---

## gui

---

## dev

```bash
# git
fedora:~ # dnf install git-core
```
