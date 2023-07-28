# user-mode linux

---

## content

- [environment](#environment)
- [build user-mode linux from kernel](#build-user-mode-linux-from-kernel)
- [build rootfs from debootstrap](#build-rootfs-from-debootstrap)
- [startup user-mode linux](#startup-user-mode-linux)
- [develop kernel module](#develop-kernel-module)
- [debug / trace module](#debug--trace-module)

## environment

```text
OS: Ubuntu 22.04.2 LTS
User-Mode Linux: Ubuntu 22
```

---

## build user-mode linux from kernel

```bash
# package
ubuntu:~ # apt install build-essential flex bison bc dwarves
ubuntu:~ # apt install libncurses-dev libssl-dev ca-certificates
ubuntu:~ # apt install xz-utils wget curl fakeroot

# download kernel
ubuntu:~ # KERNEL_URL=https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.42.tar.xz
ubuntu:~ # KERNEL_XZ=${KERNEL_URL##*/}
ubuntu:~ # KERNEL_DIR=${KERNEL_XZ%.tar.xz}

# un-compress tarball
ubuntu:~ # uname -a
ubuntu:~ # wget $KERNEL_URL
ubuntu:~ # tar Jxf $KERNEL_XZ
ubuntu:~ # cd $KERNEL_DIR
ubuntu:~ # ln -s $KERNEL_DIR linux

# compile user-mode linux
ubuntu:~ # cd linux
ubuntu:~/linux # make mrproper
ubuntu:~/linux # make defconfig ARCH=um SUBARCH=x86_64
ubuntu:~/linux # make menuconfig ARCH=um SUBARCH=x86_64
ubuntu:~/linux # make linux ARCH=um SUBARCH=x86_64 -j `nproc`
ubuntu:~/linux # file linux
ubuntu:~/linux # ./linux --help
```

---

## build rootfs from debootstrap

```bash
ubuntu:~ # ROOTFS=/root/amd64-jammy

ubuntu:~ # debootstrap \
  --arch amd64 \
  --variant minbase \
  jammy \
  $ROOTFS \
  https://ftp.ubuntu-tw.org/mirror/ubuntu/
```

---

## startup user-mode linux

```bash
# run user-mode linux
debian:~ # ./linux/linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=$ROOTFS \
  rw mem=64M init=/bin/sh ubd0=/dev/null hostname=uml \
  quiet

user-mode-linux # stty sane
user-mode-linux # mount -t proc none /proc
user-mode-linux # cat /proc/cpuinfo
```

---

## develop kernel module

---

## debug / trace module
