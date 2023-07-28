# deboostrap

---

## content

- [package](#package)
- [prepare](#prepare)
- [usage](#usage)
  - [for debian](#for-debian)
  - [for ubuntu](#for-ubuntu)

---

## package

```bash
# install
debian:~ # apt install debootstrap
debian:~ # apt install arch-install-scripts
debian:~ # apt install qemu-user-static
```

---

## prepare

```bash
debian:~ # dpkg-architecture -L
debian:~ # dpkg --add-architecture armhf      # for armhf
debian:~ # dpkg --add-architecture arm64      # for arm64
debian:~ # dpkg --add-architecture amd64      # for amd64
debian:~ # dpkg --remove-architecture armhf
debian:~ # dpkg --print-architecture
debian:~ # dpkg --print-foreign-architectures

debian:~ # apt update
debian:~ # apt install qemu-system:armhf qemu-user:armhf qemu-user-static   # for armhf
debian:~ # apt install qemu-system:arm64 qemu-user:arm64 qemu-user-static   # for arm64
```

---

## usage

### for debian

```bash
debian:~ # debootstrap --arch <ARCH> <DISTRO> <DIRECTORY> <MIRROR>
# <ARCH>      : amd64, armhf, arm64, dpkg-architecture -L
# <DISTRO>    : bookworm, bulleye, buster
# <DIRECTORY>
# <MIRROR>    : http://ftp.tw.debian.org/debian

debian:~ # ROOTFS=/home/rootfs
debian:~ # ARCH=armhf             # amd64, armhf, arm64
debian:~ # RELEASE=bulleye        # bookworm, bulleye, buster
debian:~ # MIRROR=http://ftp.tw.debian.org/debian

debian:~ # debootstrap \
  --arch $ARCH \
  --foreign \
  --keyring=/usr/share/keyrings/debian-archive-keyring.gpg \
  --verbose \
  $RELEASE \
  $ROOTFS \
  $MIRROR

debian:~ # cp /usr/bin/qemu-arm-static $ROOTFS/usr/bin/       # for armhf -> arm
debian:~ # cp /usr/bin/qemu-aarch64-static $ROOTFS/usr/bin/   # for arm64 -> aarch64
debian:~ # cp /usr/bin/qemu-x86_64-static $ROOTFS/usr/bin/    # for amd64 -> x86_64

# chroot
debian:~ # chroot $ROOTFS /bin/bash
~ # /debootstrap/debootstrap --second-stage
~ # password
```

### for ubuntu

```bash
ubuntu:~ # ROOTFS=/home/rootfs
ubuntu:~ # ARCH=amd64             # amd64|armhf|arm64
ubuntu:~ # RELEASE=jammy          # jammy|focal|bonic
ubuntu:~ # VARIANT=minbase        # minbase|buildd|fakechroot
ubuntu:~ # MIRROR=                # https://ftp.ubuntu-tw.org/mirror/ubuntu/
                                  # http://ports.ubuntu.com/ubuntu-ports
                                  # https://mirror.leaseweb.com/ubuntu/

ubuntu:~ # debootstrap \
  --arch $ARCH \
  --variant $VARIANT \
  $RELEASE \
  $ROOTFS \
  $MIRROR

ubuntu:~ # cp /usr/bin/qemu-arm-static $ROOTFS/usr/bin/       # for armhf -> arm
ubuntu:~ # cp /usr/bin/qemu-aarch64-static $ROOTFS/usr/bin/   # for arm64 -> aarch64
ubuntu:~ # cp /usr/bin/qemu-x86_64-static $ROOTFS/usr/bin/    # for amd64 -> x86_64


ubuntu:~ # echo -e "deb http://ports.ubuntu.com/ubuntu-ports/ focal main restricted\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal multiverse\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal universe\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-backports main restricted universe multiverse\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-security main restricted\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-security multiverse\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-security universe\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-updates main restricted\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-updates multiverse\n
deb http://ports.ubuntu.com/ubuntu-ports/ focal-updates universe
" >> $ROOTFS/etc/apt/sources.list


release="jammy"

echo -e "deb http://archive.ubuntu.com/ubuntu/ ${release} main restricted universe\n
deb http://security.ubuntu.com/ubuntu/ ${release}-security main restricted universe\n
deb http://archive.ubuntu.com/ubuntu/ ${release}-updates main restricted universe\n
" > /mnt/etc/apt/sources.list

# chroot
ubuntu:~ # chroot $ROOTFS /bin/bash
target:~ # password
target:~ # apt install tzdata
target:~ # dpkg-reconfigure tzdata
target:~ # apt install locales
target:~ # dpkg-reconfigure locales
target:~ # apt install keyboard-configuration
target:~ # dpkg-reconfigure keyboard-configuration
target:~ # echo 'myhostname' > /etc/hostname
target:~ # cat << EOF >> /etc/hosts
127.0.0.1	localhost
::1		localhost
127.0.1.1	myhostname.localdomain	myhostname
EOF


# chroot
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot $ROOTFS

```
