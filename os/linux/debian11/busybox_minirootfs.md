# busybox to rootfs on qemu

## prepare

```bash
debian:~ # apt install libncurses-dev flex bison
debian:~ # apt install libssl-dev bc dwarves

debian:~ # ROOTFS_DIR=/home/x64/rootfs
debian:~ # BZ_IMAGE=/home/x64/bzImage
debian:~ # INIT_RD=/home/x64/initrd.cpio
```

---

## kernel

```bash
# download
debian:~ # wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.170.tar.xz

debian:~ # tar Jxf linux-5.10.170.tar.xz
debian:~ # cd linux-5.10.170
debian:~/linux-5.10.170 # cp /boot/config-5.10.0-18-amd64 .config

debian:~/linux-5.10.170 # make menuconfig
General setup  --->
  [*] Initial RAM filesystem and RAM disk (initramfs/initrd) support

Device Drivers  --->
  [*] Block devices  --->
    <*>   RAM block device support
  <*> MMC/SD/SDIO card support  --->
    <*>   MMC block device driver

File systems  --->
  <*> The Extended 4 (ext4) filesystem

-*- Cryptographic API  --->
  Certificates for signature checking  --->
    () Additional X.509 keys for default system keyring

# check flag
debian:~/linux-5.10.170 # grep CONFIG_BLK_DEV_INITRD=y .config
debian:~/linux-5.10.170 # grep CONFIG_INITRAMFS_SOURCE="" .config
debian:~/linux-5.10.170 # grep CONFIG_BLK_DEV_RAM=y .config
debian:~/linux-5.10.170 # grep CONFIG_HOTPLUG=y .config
debian:~/linux-5.10.170 # grep CONFIG_PROC_FS=y .config
debian:~/linux-5.10.170 # grep CONFIG_SYSFS=y .config

# compile
debian:~/linux-5.10.170 # make [-j <cpu number>]
debian:~/linux-5.10.170 # make bzImage
debian:~/linux-5.10.170 # cp arch/x86/boot/bzImage $BZ_IMAGE
```

---

## busybox

```bash
# download
debian:~ # wget https://busybox.net/downloads/busybox-1.36.0.tar.bz2

debian:~ # tar jxf busybox-1.36.0.tar.bz2
debian:~ # cd busybox-1.36.0
debian:~/busybox-1.36.0 # make menuconfig
settings  --->
  [ ] Enable compatibility for full-blown desktop systems (8kb)
  [*] Build static binary (no shared libs)
  (./_install) Destination path for 'make install'

# check flag
debian:~/busybox-1.36.0 # grep CONFIG_DESKTOP=n .config
debian:~/busybox-1.36.0 # grep CONFIG_STATIC=y .config
debian:~/busybox-1.36.0 # grep CONFIG_PREFIX= .config

# compile
debian:~/busybox-1.36.0 # make LDFLAGS=--static
debian:~/busybox-1.36.0 # make CONFIG_PREFIX=$ROOTFS_DIR install
```

---

## init

```bash
# fhs
debian:~ # mkdir -p $ROOTFS_DIR/{bin,lib,dev,etc,mnt,proc,root,sbin,sys,tmp}
debian:~ # cd $ROOTFS_DIR/dev/

# /dev
debian:/home/x64/rootfs/dev # mknod ram0 b 1 0 # all one needs is ram0
debian:/home/x64/rootfs/dev # mknod ram1 b 1 1
debian:/home/x64/rootfs/dev # mknod initrd b 1 250
debian:/home/x64/rootfs/dev # mknod mem c 1 1
debian:/home/x64/rootfs/dev # mknod kmem c 1 2
debian:/home/x64/rootfs/dev # mknod null c 1 3
debian:/home/x64/rootfs/dev # mknod port c 1 4
debian:/home/x64/rootfs/dev # mknod zero c 1 5
debian:/home/x64/rootfs/dev # mknod core c 1 6
debian:/home/x64/rootfs/dev # mknod full c 1 7
debian:/home/x64/rootfs/dev # mknod random c 1 8
debian:/home/x64/rootfs/dev # mknod urandom c 1 9
debian:/home/x64/rootfs/dev # mknod aio c 1 10
debian:/home/x64/rootfs/dev # mknod kmsg c 1 11
debian:/home/x64/rootfs/dev # mknod sda b 8 0
debian:/home/x64/rootfs/dev # mknod tty0 c 4 0
debian:/home/x64/rootfs/dev # mknod ttyS0 c 4 64
debian:/home/x64/rootfs/dev # mknod ttyS1 c 4 65
debian:/home/x64/rootfs/dev # mknod tty c 5 0
debian:/home/x64/rootfs/dev # mknod console c 5 1
debian:/home/x64/rootfs/dev # mknod ptmx c 5 2
debian:/home/x64/rootfs/dev # mknod ttyprintk c 5 3

# /proc
debian:/home/x64/rootfs/dev # ln -s ram0 ramdisk
debian:/home/x64/rootfs/dev # ln -s ../proc/self/fd fd
debian:/home/x64/rootfs/dev # ln -s ../proc/self/fd/0 stdin # process i/o
debian:/home/x64/rootfs/dev # ln -s ../proc/self/fd/1 stdout
debian:/home/x64/rootfs/dev # ln -s ../proc/self/fd/2 stderr
debian:/home/x64/rootfs/dev # ln -s ../proc/kcore     kcore

# init
debian:~ # cat << EOF >> $ROOTFS_DIR/init
#!/bin/sh

/bin/mount -t proc none /proc
/bin/mount -t sysfs sysfs /sys
/sbin/mdev -s
# /sbin/ifconfig lo 127.0.0.1 netmask 255.0.0.0 up
# /sbin/ifconfig eth0 up 192.168.10.10 netmask 255.255.255.0 up
# /sbin/route add default gw 192.168.10.1

echo 'Enjoy your Linux system!'

/usr/bin/setsid /bin/cttyhack /bin/sh
exec /bin/sh
EOF
debian:~ # chmod 755 init

# create initrd
debian:~ # $ROOTFS_DIR
debian:/home/x64/rootfs # find . -print0 | cpio --null -ov --format=newc > $INIT_RD
```

---

## qemu

```bash
debian:~ # qemu-system-x86_64 \
  -smp 2 \
  -m 2G \
  -kernel $BZ_IMAGE \
  -initrd $INIT_RD \
  -append "root=/dev/ram0 init=init console=ttyS0 rootfstype=ramfs" \
  -nographic
```
