# qemu-arm

## package

```bash
debian:~ # apt install qemu-system
debian:~ # qemu-system-aarch64 --version

debian:~ # apt install libguestfs-tools
debian:~ # virt-ls --version
```

---

## cross-build toolchain

```bash
debian:~ # apt install crossbuild-essential-arm64   # for arm64
debian:~ # apt install crossbuild-essential-armel   # for arm32
debian:~ # apt install crossbuild-essential-armhf

debian:~ # cat << EOF >> hello.c
#include <stdio.h>

int main() {
  printf("hello\n");
}
EOF

debian:~ # aarch64-linux-gnu-gcc -c hello.c -o hello-aarch64
debian:~ # file hello-aarch64
```

---

## debian arm64 - netboot install

```bash
debian:~ # IMG_REPO=https://deb.debian.org/debian/dists/bullseye/main/installer-arm64/current/images/netboot
debian:~ # VM_DISK=debian-aarch64.qcow2

# download
debian:~ # wget $IMG_REPO/debian-installer/arm64/initrd.gz
debian:~ # wget $IMG_REPO/debian-installer/arm64/linux
debian:~ # wget $IMG_REPO/mini.iso

# create disk
debian:~ # qemu-img create -f qcow2 $VM_DISK 32G

# install
debian:~ # qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1G -kernel ./linux -initrd ./initrd.gz \
  -hda $VM_DISK -append "console=ttyAMA0" \
  -drive file=mini.iso,id=cdrom,if=none,media=cdrom \
  -device virtio-scsi-device -device scsi-cd,drive=cdrom -nographic

# copy kernel
debian:~ # virt-ls -l -a $VM_DISK /boot/
debian:~ # virt-copy-out -a $VM_DISK /boot/vmlinuz /boot/initrd.img .

# run
debian:~ # qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1G -initrd initrd.img \
  -kernel vmlinuz -append "root=/dev/vda2 console=ttyAMA0" \
  -drive if=virtio,file=$VM_DISK,format=qcow2,id=hd \
  -net user,hostfwd=tcp::10022-:22 -net nic \
  -device intel-hda -device hda-duplex -nographic
```

ps $VM_DISK 可以用 virt-manager 直接使用

---

## sd card

```bash
debian:~ # SD_DISK=sd.img
debian:~ # LOOP_DEVICE=/dev/loop0
debian:~ # MAP_LOOP_DEVICE=/dev/map/loop0

# create virtual sd card
debian:~ # dd if=/dev/zero of=$SD_DISK bs=1G count=2
debian:~ # file $SD_DISK
debian:~ # hexdump $SD_DISK

# partition device
debian:~ # losetup $LOOP_DEVICE $SD_DISK
debian:~ # parted -s $LOOP_DEVICE mklabel msdos
debian:~ # parted -s $LOOP_DEVICE mkpart primary fat32 0% 128MiB   # 0% -> 512 * 2048 = 1049kB = 1047552
debian:~ # parted -s $LOOP_DEVICE set 1 lba off
# debian:~ # parted -s $LOOP_DEVICE mkpart primary ext4 128MiB 100%
debian:~ # parted -s $LOOP_DEVICE print
debian:~ # fdisk -l $LOOP_DEVICE

# load partition table
debian:~ # kpart -av $LOOP_DEVICE
debian:~ # kpart -lv $LOOP_DEVICE

# format file system
debian:~ # mkfs -t msdos ${MAP_LOOP_DEVICE}p1
debian:~ # mkfs -t ext4 ${MAP_LOOP_DEVICE}p2

# mount device
debian:~ # mkdir -p /sd1 /sd2
debian:~ # mount ${MAP_LOOP_DEVICE}p1 /sd1
debian:~ # mount ${MAP_LOOP_DEVICE}p2 /sd2

## clean
debian:~ # umount /sd1
debian:~ # umount /sd1
debian:~ # kpart -dv $LOOP_DEIVCE
debian:~ # losetup -d $LOOP_DEVICE
```

---

## other

```bash
# list qemu support
debian:~ # qemu-system-aarch64 -machine help
debian:~ # qemu-system-aarch64 -cpu help

# nbd
debian:~ # modprobe nbd max_part=8
debian:~ # lsmod nbd
```

---

## ref

[Debian on QEMU-emulated ARM-64 aarch64](https://phwl.org/2022/qemu-aarch64-debian/)
