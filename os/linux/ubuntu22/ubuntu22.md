# ubuntu 22.04

---

## content

- [basic](#basic)
- [develop](#develop)
- [cli](#cli)
- [gui](#gui)
- [service](#service)

---

## basic

```bash
ubuntu:~ # apt update

ubuntu:~ # apt install curl git vim-nox
```

---

## develop

```bash
# gcc, g++
ubuntu:~ # apt install build-essential

# git
ubuntu:~ # apt install git

# cmake
ubuntu:~ # apt install cmake
```

---

## cli

```bash
# bash
ubuntu:~ # apt install bash-completion

# zsh
ubuntu:~ # apt install zsh

# oh-my-zsh
ubuntu:~ $ chsh -s /bin/zsh
ubuntu:~ $ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
ubuntu:~ $ omz update

# oh-my-zsh config
ubuntu:~ $ vi ~/.zshrc
ZSH_THEME="robbyrussell"    -> ZSH_THEME="agnoster"
plugins=()                  -> plugins=(git tmux)
```

---

## gui

```bash
# can't open terminal in virtualbox
linux:~ # grep LANG= /etc/default/locale
LANG="en_US"
>>
linux:~ # sed s/LANG=.*/LANG=\"en_US.UTF-8\"/ /etc/default/locale
LANG="en_US.UTF-8"

linux:~ # locale-gen --purge
linux:~ # reboot
```

---

## network

### disable ipv6

```bash
ubuntu:~ # ip a | grep inet6

ubuntu:~ # cat << EOF >> /etc/sysctl.conf
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1
EOF

ubuntu:~ # reboot

ubuntu:~ # sysctl -w net.ipv6.conf.all.disable_ipv6=1
ubuntu:~ # sysctl -w net.ipv6.conf.default.disable_ipv6=1
ubuntu:~ # sysctl -w net.ipv6.conf.lo.disable_ipv6=1
```

### enable ipv6

```bash
ubuntu:~ # ip a | grep inet6

ubuntu:~ # cat << EOF >> /etc/sysctl.conf
net.ipv6.conf.all.disable_ipv6=0
net.ipv6.conf.default.disable_ipv6=0
net.ipv6.conf.lo.disable_ipv6=0
EOF

ubuntu:~ # reboot

ubuntu:~ # sysctl -w net.ipv6.conf.all.disable_ipv6=0
ubuntu:~ # sysctl -w net.ipv6.conf.default.disable_ipv6=0
ubuntu:~ # sysctl -w net.ipv6.conf.lo.disable_ipv6=0
```

---

## service

```bash
# sshd
ubuntu:~ # apt install openssh-server

ubuntu:~ # systemctl enable|disable sshd
ubuntu:~ # systemctl start|stop     sshd
ubuntu:~ # systemctl status         sshd
```

[ufw](../ubuntu20/ufw.md)
