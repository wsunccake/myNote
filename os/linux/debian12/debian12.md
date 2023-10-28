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

---

## wm

[i3](./i3.md)
