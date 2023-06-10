# deboostrap

## package

```bash
# install
debian:~ # apt install debootstrap
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
