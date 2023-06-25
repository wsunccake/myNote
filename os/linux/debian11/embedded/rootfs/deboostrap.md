# deboostrap

## package

```bash
# install
debian:~ # apt install debootstrap
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
