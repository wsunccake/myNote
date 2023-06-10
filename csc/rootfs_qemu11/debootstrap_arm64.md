# deboostrap to rootfs on arm

## prepare

```bash
# for toolchain
debian:~ # dpkg-architecture -L
debian:~ # dpkg --add-architecture arm64
debian:~ # dpkg --print-foreign-architectures
debian:~ # apt update
debian:~ # apt install qemu-system:arm64 qemu-user:arm64 qemu-user-static
debian:~ # apt install crossbuild-essential-arm64

# for sd card
debian:~ # apt install kpartx

# for deboostrap
debian:~ # apt install debootstrap

# for kernel
debian:~ # apt install libncurses-dev flex bison
debian:~ # apt install libssl-dev bc dwarves
debian:~ # apt-get install u-boot-tools

# env var
debian:~ # SD_IMG=/home/arm64/sd.img
debian:~ # LOOP=loop0
debian:~ # SD1=/home/arm64/sd1
debian:~ # SD2=/home/arm64/sd2
debian:~ # IMG=/home/arm64/Image


debian:~ # ROOTFS_DIR=/home/arm64/rootfs
debian:~ # BZ_IMAGE=/home/arm64/bzImage
debian:~ # INIT_RD=/home/arm64/initrd.cpio
debian:~ # ROOTFS_IMG=/home/arm64/rootfs.img
```

---

## toolchain

```bash
debian:~ # aarch64-linux-gnu-gcc -v

# test
debian:~ # cat << EOF >> hello.c
#include <stdio.h>

int main() {
  printf("hello\n");
}
EOF

debian:~ # aarch64-linux-gnu-gcc -c hello.c -o hello.aarch64
debian:~ # file hello.aarch64
debian:~ # hello.aarch64
```

---

## sd card

```bash
# create
debian:~ # dd if=/dev/zero of=$SD_IMG bs=1G count=2
debian:~ # file $SD_IMG
debian:~ # hexdump $SD_IMG

# partition
debian:~ # parted -s $SD_IMG mklabel msdos
debian:~ # parted -s $SD_IMG mkpart primary fat32 1MiB 81MiB
debian:~ # parted -s $SD_IMG set 1 lba off
debian:~ # parted -s $SD_IMG mkpart primary ext4 81MiB 100%
debian:~ # parted -s $SD_IMG print
debian:~ # fdisk -l $SD_IMG

# attach
debian:~ # losetup /dev/$LOOP $SD_IMG
debian:~ # losetup
debian:~ # kpartx -av /dev/$LOOP
debian:~ # kpartx -lv /dev/$LOOP

# format
debian:~ # mkfs -t msdos /dev/${LOOP}p1
debian:~ # mkfs -t ext4 -F /dev/${LOOP}p2

# mount
debian:~ # mkdir -p $SD1
debian:~ # mkdir -p $SD2
debian:~ # mount /dev/mapper/${LOOP}p1 $SD1
debian:~ # mount /dev/mapper/${LOOP}p2 $SD2
debian:~ # lsblk

# umount
debian:~ # umount $SD1
debian:~ # umount $SD2

# detach
debian:~ # kpartx -dv /dev/$LOOP
debian:~ # losetup -d /dev/$LOOP
```

---

## rootfs - debootstrap

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
  $SD2 \
  http://ftp.tw.debian.org/debian

debian:~ # cp /usr/bin/qemu-aarch64-static $SD2/usr/bin/
debian:~ # uname -m
x86_64

# chroot
debian:~ # chroot $SD2 /bin/bash
~ # /debootstrap/debootstrap --second-stage
~ # uname -m
aarch64

~ # passwd
~ # exit
```

---

## kernel

```bash
debian:~ # wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.172.tar.xz

debian:~ # tar Jxf linux-5.10.172.tar.xz
debian:~ # cd linux-5.10.172

debian:~/linux-5.10.172 # ls arch/arm64/configs/
debian:~/linux-5.10.172 # ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make defconfig
debian:~/linux-5.10.172 # ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make menuconfig

debian:~/linux-5.10.172 # ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make [-j <cpu number>]
debian:~/linux-5.10.172 # cp arch/arm64/boot/Image $IMG
```

---

## uboot

## qemu

```bash
debian:~ # qemu-system-aarch64 \
  -machine raspi3b \
  -dtb bcm2837-rpi-3-b.dtb \
  -smp 4 \
  -m 1024M \
  -kernel Image \
  -append "console=ttyAMA0" \
  -nographic

qemu-system-aarch64 \
  -machine raspi3b \
  -dtb bcm2837-rpi-3-b.dtb \
  -smp 4 \
  -m 1024M \
  -kernel Image \
  -append "root=/dev/mmcblk0p2 rw console=ttyAMA0" \
  -serial mon:stdio -display none -sd sd.img


qemu-system-aarch64 \
  -machine raspi3b \
  -dtb bcm2837-rpi-3-b.dtb \
  -smp 4 \
  -m 1G \
  -kernel Image \
  -append "root=/dev/mmcblk0p2 rw console=ttyAMA0" \
  -nographic -sd sd.img


qemu-system-aarch64 \
  -machine raspi3b \
  -dtb bcm2837-rpi-3-b.dtb \
  -smp 4 \
  -m 1G \
  -kernel Image \
  -append "root=/dev/mmcblk0p2 rw console=ttyAMA0" \
  -nographic \
  -drive file=sd.img,if=sd,format=raw,index=0


qemu-system-aarch64 \
  -machine raspi3b \
  -dtb bcm2837-rpi-3-b.dtb \
  -smp 4 \
  -m 1G \
  -kernel Image \
  -append "root=/dev/mmcblk0p2 rw console=ttyAMA0" \
  -device sdhci-pci \
  -device sd-card,drive=mydrive \
  -drive id=mydrive,if=none,format=raw,file=sd.img \
  -nographic \

```
