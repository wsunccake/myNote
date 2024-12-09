# debian 12

## system

```bash
# repo
debian:~ # apt edit-sources
deb http://deb.debian.org/debian bookworm main contrib non-free-firmware
#deb-src http://deb.debian.org/debian bookworm main contrib non-free-firmware

deb http://deb.debian.org/debian-security/ bookworm-security main contrib non-free-firmware
#deb-src http://deb.debian.org/debian-security/ bookworm-security main contrib non-free-firmware

deb http://deb.debian.org/debian bookworm-updates main contrib non-free-firmware
#deb-src http://deb.debian.org/debian bookworm-updates main contrib non-free-firmware

debian:~ # apt update
```

---

## develop

```bash
# git
debian:~ # apt install git
```

---

## cli

```bash
# vim
debian:~ # apt install vim-nox
# curl
debian:~ # apt install curl

# zsh
debian:~ # apt install zsh

# oh-my-zsh
debian:~ $ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
debian:~ $ omz update

# fzf
debian:~ $ git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
debian:~ $ ~/.fzf/install

# screen and tmux
debian:~ # apt install screen tmux

# jq
debian:~ # apt install jq

# yq
debian:~ # curl -OL "https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64" -o /usr/local/bin/yq
debian:~ # chmod +x /usr/local/bin/yq

# unetbootin
debian:~ # apt install mtools
debian:~ # wget https://github.com/unetbootin/unetbootin/releases/download/702/unetbootin-linux64-702.bin
debian:~ # chmod +x unetbootin-linux64-702.bin
debian:~ # ./unetbootin-linux64-702.bin
```

---

## gui

```bash
# vscode
debian:~ # dpkg -i code_1.79.2-1686734195_amd64.deb

# chrome
debian:~ # dpkg -i google-chrome-stable_current_amd64.deb

# ibus
debian:~ # apt install ibus
```

### vnc server

```bash
debian:~ # apt install dbus-x11

debian:~ # apt install tightvncserver
debian:~ $ vncserver [-geometry 1920x1080] [:1]
debian:~ $ vncserver -list
debian:~ $ vncserver -kill :1
```

---

## wm

[i3](./i3.md)

---

## de

### xfce4

```bash
debian:~ # apt install xfce4
```

---

## other

###

```bash
debian:~ # apt install smartmontools
debian:~ # smartctl -a /dev/sd<X>

# Reallocated_Sector_Ct: 硬碟檢測到某個扇區出現物理損壞且無法正常讀寫時, 該扇區會被標記為 "壞扇區"
# 硬碟會將這個壞扇區的數據重新分配到一個保留的, 良好的備用扇區.
# Reallocated_Sector_Ct 就是已經發生這種重新分配的扇區數量
# 低值或0: 表示硬碟狀況良好, 沒有或僅有少量壞扇區
# 高值: 表示硬碟已有許多壞扇區
# Current_Pending_Sector: 硬碟上當前處於 "待處理" 狀態的扇區數量,
# 低值或0: 通常表示硬碟健康狀況良好
# 高值: 可能意味著硬碟正在失效
```

### ntfs

```bash
debian:~ # apt install ntfs-3g
debian:~ # mount -t ntfs-3g /dev/sd<X><n> /mnt

debian:~ # umount /mnt

debian:~ # ntfsfix /dev/sd<X><n>
```

### mtp / android phone

```bash
debian:~ # apt install jmtpfs
debian:~ # jmtpfs -l                                        # list device
debian:~ # jmtpfs [-device=<busnum>,<devnum>] <mount-point> # mount device
debian:~ # jmtpfs -u <mount-point>                          # umount device
```

```bash
debian:~ # apt install android-file-transfer
debian:~ # android-file-transfer            # gui
debian:~ # aft-mtp-mount <mount-point>      # mount device
debian:~ # fusermount -u <mount-point>      # umount device
```
