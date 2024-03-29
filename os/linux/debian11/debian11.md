# debian 11

## system

```bash
# mount disk by uuid
debian:~ # lsblk
debian:~ # lsblk -pt
debian:~ # lsblk -pl
debian:~ # blkid
debian:~ # cat /etc/fstab
UUID=<disk uuid>   <mount point>   <fs type>  defaults,errors=remount-ro 0  0
debian:~ # mount -a

# intel wifi drvier
debian:~ # apt update
debian:~ # apt install firmware-iwlwifi

# repo
debian:~ # cat /etc/apt/sources.list
deb http://deb.debian.org/debian bullseye main contrib non-free
deb-src http://deb.debian.org/debian bullseye main contrib non-free

deb http://deb.debian.org/debian-security/ bullseye-security main contrib non-free
deb-src http://deb.debian.org/debian-security/ bullseye-security main contrib non-free

deb http://deb.debian.org/debian bullseye-updates main contrib non-free
deb-src http://deb.debian.org/debian bullseye-updates main contrib non-free

deb http://deb.debian.org/debian bullseye-backports main contrib non-free
deb-src http://deb.debian.org/debian bullseye-backports main contrib non-free

deb http://deb.debian.org/debian/ unstable main
deb-src http://deb.debian.org/debian/ unstable main

debian:~ # apt update
```

---

## develop

```bash
# build tool: gcc, g++, make
debian:~ # apt install build-essential

# openjdk
debian:~ # apt install openjdk-11-jdk

# python3
debian:~ # apt install python3 python3-pip3 python3-venv

# git
debian:~ # apt install git

# postgres
debian:~ # echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
debian:~ # wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
debian:~ # apt update
debian:~ # apt search postgresql               # server package
debian:~ # apt search postgresql-client        # clinet package
debian:~ # apt install postgresql              # install server
debian:~ # apt install postgresql-client       # install clinet

# kernel header
debian:~ # apt install linux-headers-`uname -r`
```

---

## cli

```bash
# curl
debian:~ # apt install curl

# zsh
debian:~ # apt install zsh

# oh-my-zsh
debian:~ $ chsh -s /bin/zsh
debian:~ $ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
debian:~ $ omz update

# oh-my-zsh config
debian:~ $ vi ~/.zshrc
ZSH_THEME="robbyrussell"    -> ZSH_THEME="agnoster"
plugins=()                  -> plugins=(git tmux)

# fzf
debian:~ $ git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
debian:~ $ ~/.fzf/install

# screen and tmux
debian:~ # apt install screen tmux

# locate
debian:~ # apt install mlocate

# lnav
debian:~ # apt install lnav

# wodim
debian:~ # apt install wodim
debian:~ # wodim -v -dao dev=/dev/cdrw <image>.iso

# rpm2cpio
debian:~ # apt install rpm2cpio

# freeradius-utils
debian:~ # apt install freeradius-utils
debian:~ $ radtest <radius server>:<port> <user> <pw> <nas number> <secret>

# ulimit
debian:~ # ulimit -a
-t: cpu time (seconds)              unlimited
-f: file size (blocks)              unlimited
-d: data seg size (kbytes)          unlimited
-s: stack size (kbytes)             8192
-c: core file size (blocks)         0
-m: resident set size (kbytes)      unlimited
-u: processes                       255781
-n: file descriptors                10000
-l: locked-in-memory size (kbytes)  8191205
-v: address space (kbytes)          unlimited
-x: file locks                      unlimited
-i: pending signals                 255781
-q: bytes in POSIX msg queues       819200
-e: max nice                        0
-r: max rt priority                 0
-N 15:                              unlimited
# -c: when executable lauch fail, core dump size
# -s: executable stack size
```

---

## gui

```bash
# vscode
debian:~ # apt install software-properties-common apt-transport-https curl
debian:~ # curl -sSL https://packages.microsoft.com/keys/microsoft.asc -o microsoft.asc
debian:~ # gpg --no-default-keyring --keyring ./ms_signing_key_temp.gpg --import ./microsoft.asc
debian:~ # gpg --no-default-keyring --keyring ./ms_signing_key_temp.gpg --export > ./ms_signing_key.gpg
debian:~ # mv ms_signing_key.gpg /etc/apt/trusted.gpg.d/
debian:~ # echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" | tee /etc/apt/sources.list.d/vscode.list
debian:~ # apt update
debian:~ # apt install code

# chrome
debian:~ # cat << EOF > /etc/apt/sources.list.d/google-chrome.list
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
EOF
debian:~ # wget -O- https://dl.google.com/linux/linux_signing_key.pub |gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg
debian:~ # apt update
debian:~ # apt install google-chrome-stable
```

---

## x-window

### i3wm

```bash
# i3wm
debian:~ # apt update
debian:~ # apt install i3
```

### vnc

```bash
# server
debian:~ # apt install tigervnc-standalone-server tigervnc-common
debian:~ # su - <user>
debian:~ $ vncpasswd

debian:~ $ vncserver -localhost no
debian:~ $ vncserver -list
debian:~ $ vncserver -kill :1


# client
debian:~ $ apt install tigervnc-viewer
```

---

## vm / container

```bash
### libvirt
debian:~ # apt install libvirt-clients
debian:~ # apt install virt-manager
debian:~ # apt install qemu-system
debian:~ # apt install libvirt-daemon-system

### docker
debian:~ # apt-get remove docker docker-engine docker.io containerd runc
debian:~ # apt-get update
debian:~ # apt-get install apt-transport-https ca-certificates \
    curl gnupg lsb-release
debian:~ # curl -fsSL https://download.docker.com/linux/debian/gpg \
    | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
debian:~ # echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null
debian:~ # apt-get update
debian:~ # apt-get install docker-ce docker-ce-cli containerd.io
debian:~ # apt-cache madison docker-ce
debian:~ # apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io

### minikube
debian:~ # curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
debian:~ # install minikube-linux-amd64 /usr/local/bin/minikube
debian:~ # minikube start --driver=docker --force
debian:~ # minikube kubectl <kube cmd>
```

---

## cloud

### gcp

```bash
debian:~ # apt-get install apt-transport-https ca-certificates gnupg
debian:~ # echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
debian:~ # curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
debian:~ # apt-get update && apt-get install google-cloud-sdk

debian:~ # gcloud init
```

---

## vpn

[global protect](./global_protect.md)

---

## im

### skype

```bash
debian:~ # wget https://go.skype.com/skypeforlinux-64.deb
debian:~ # dpkg -i skypeforlinux-64.deb
```

---

## input / keyin

### locale

```bash
debian:~ # dpkg-reconfigure locales
->
select
zh_TW.UTF-8     (required)
zh_TW BIG5      (optional)

# locale
debian:~ # localectl list-locales
debian:~ # localectl set-locale en_US.UTF-8
```

### font

```bash
## 文泉驛 字體
xfonts-wqy fonts-wqy-zenhei fonts-wqy-microhei

## 文鼎楷 字體
fonts-arphic-ukai fonts-arphic-uming

## 思源 字體
fonts-noto
```

### ibus

```bash
# install
debian:~ # apt install ibus
debian:~ # apt install ibus-chewing ibus-zhuyin

# setting gnome 3.x
debian:~ $ gnome-control-center
Region & Language -> Input Sources
```
