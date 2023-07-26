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

ubuntu:~ # debootstrap \
  --arch arm64 \
  focal \
  $ROOTFS \
  http://ports.ubuntu.com/ubuntu-ports

ubuntu:~ # cp /usr/bin/qemu-aarch64-static $ROOTFS/usr/bin/
ubuntu:~ # echo -e "deb http://ports.ubuntu.com/ubuntu-ports/ focal main restricted\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal universe\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-backports main restricted universe multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-security main restricted\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-security multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-security universe\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-updates main restricted\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-updates multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-updates universe" >> $ROOTFS/etc/apt/sources.list

# chroot
ubuntu:~ # chroot $ROOTFS /bin/bash
~ # password
```
