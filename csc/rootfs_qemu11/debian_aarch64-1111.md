# debina - rootfs

## sd card

```bash
debian:~ # SD_IMG=sdcard.img
debian:~ # LOOP_DEV=loop0
debian:~ # SD1=/mnt/sd1
debian:~ # SD2=/mnt/sd2

debian:~ # dd if=/dev/zero of=$SD_IMG bs=1G count=1
debian:~ # file $SD_IMG
debian:~ # hexdump $SD_IMG

debian:~ # parted -s $SD_IMG mklabel msdos
debian:~ # parted -s $SD_IMG mkpart primary fat32 1Mib 81MiB
debian:~ # parted -s $SD_IMG set 1 lba off
debian:~ # parted -s $SD_IMG mkpart primary ext4 81MiB 100%
debian:~ # parted -s $SD_IMG print
debian:~ # fdisk -l $SD_IMG

# attach
debian:~ # losetup /dev/$LOOP_DEV $SD_IMG
debian:~ # losetup
debian:~ # kpartx -av /dev/$LOOP_DEV
debian:~ # kpartx -lv /dev/$LOOP_DEV
debian:~ # mkfs -t msdos /dev/mapper/${LOOP_DEV}p1
debian:~ # mkfs -t ext4 -F /dev/mapper/${LOOP_DEV}p2
debian:~ # mount /dev/mapper/${LOOP_DEV}p1 $SD1
debian:~ # mount /dev/mapper/${LOOP_DEV}p2 $SD2

# detach
debian:~ # umount $SD1
debian:~ # umount $SD2
debian:~ # kpartx -dv /dev/$LOOP_DEV
debian:~ # losetup -dv /dev/$LOOP_DEV
```

---

## rootfs

```bash
debian:~ # apt install qemu qemu-user-static
debian:~ # apt install debian-archive-keyring debootstrap
debian:~ # apt install binfmt-support

debian:~ # debootstrap \
  --arch=arm64 \
  --keyring=/usr/share/keyrings/debian-archive-keyring.gpg \
  --verbose \
  --foreign \
  bullseye \
  /mnt/sd2 \
  http://ftp.tw.debian.org/debian

debian:~ # cp /usr/bin/qemu-aarch64-static $SD2/usr/bin/
debian:~ # chroot $SD2 /bin/bash

# chroot
~ # /debootstrap/debootstrap --second-stage
~ # exit

debian:~ # uname -m
x86_64

# re-chroot
debian:~ # chroot $SD2 /bin/bash

~ # uname -m
aarch64

# run detach
```

---

## u-boot

```bash
debian:~ # wget https://ftp.denx.de/pub/u-boot/u-boot-2023.01.tar.bz2
debian:~ # tar jxf u-boot-2023.01.tar.bz2
debian:~ # cd u-boot-2023.01
debian:~/u-boot-2023.01 # ls configs/qemu_arm64_defconfig

debian:~/u-boot-2023.01 # make qemu_arm64_defconfig
debian:~/u-boot-2023.01 # make menuconfig
debian:~/u-boot-2023.01 # CROSS_COMPILE=aarch64-linux-gnu- make
debian:~/u-boot-2023.01 # ls u-boot

debian:~/u-boot-2023.01 # qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a57 \
  -smp 2\
  -m 1G \
  -kernel u-boot \
  -nographic
u-boot => help
u-boot => bdinfo
boot_params = 0x0000000000000000
DRAM bank   = 0x0000000000000000
-> start    = 0x0000000040000000
-> size     = 0x0000000040000000
flashstart  = 0x0000000000000000
flashsize   = 0x0000000004000000
flashoffset = 0x00000000000e8148
...

DRAM bank   = 0x0000000000000000
-> start    = 0x0000000040000000
-> size     = 0x0000000040000000
# -> 1,073,741,824 byte (B) = 1,073,741,824 B / 1,024 =
# 1,048,576 KiB = 1,048,576 KiB / 1,024 =
# 1,024 MiB = 1,024 MiB / 1,024 =
# 1 GiB
u-boot => mmcinfo

qemu-system-aarch64 -machine virt -cpu cortex-a57 -bios u-boot.bin -nographic

```

---

## kernel

```bash
debian:~ # wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.170.tar.xz

debian:~ # tar Jxf linux-5.10.170.tar.xz
debian:~ # cd linux-5.10.170

debian:~/linux-5.10.170 # ls arch/arm64/configs/
debian:~/linux-5.10.170 # ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make defconfig
debian:~/linux-5.10.170 # ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make menuconfig
debian:~/linux-5.10.170 # ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make Image
```
