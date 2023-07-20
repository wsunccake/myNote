# deboostrap

## package

```bash
# install
debian:~ # apt install debootstrap
debian:~ # apt install qemu-user-static
```

---

## x86_64

---

## arm

```bash
# debootstrap --arch <ARCH> <DISTRO> <DIRECTORY>  <MIRROR>
# debootstrap --second-stage

debian:~ # ROOTFS=/home/rootfs

debian:~ # debootstrap \
  --arch armhf \
  --foreign \
  --keyring=/usr/share/keyrings/debian-archive-keyring.gpg \
  --verbose \
  bullseye \
  $ROOTFS \
  http://ftp.tw.debian.org/debian

debian:~ # cp /usr/bin/qemu-arm-static $ROOTFS/usr/bin/

# chroot
debian:~ # chroot $ROOTFS /bin/bash
~ # /debootstrap/debootstrap --second-stage
~ # password
```

---

## arm64

```bash
debian:~ # ROOTFS=/home/rootfs

debian:~ # debootstrap \
  --arch arm64 \
  focal \
  $ROOTFS \
  http://ports.ubuntu.com/ubuntu-ports

debian:~ # cp /usr/bin/qemu-aarch64-static $ROOTFS/usr/bin/
debian:~ # echo -e "deb http://ports.ubuntu.com/ubuntu-ports/ focal main restricted\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal universe\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-backports main restricted universe multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-security main restricted\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-security multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-security universe\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-updates main restricted\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-updates multiverse\ndeb http://ports.ubuntu.com/ubuntu-ports/ focal-updates universe" >> $ROOTFS/etc/apt/sources.list

# chroot
debian:~ # chroot $ROOTFS /bin/bash
~ # /debootstrap/debootstrap --second-stage
~ # password
```
