# qemu-arm

```bash
debian:~ # apt install net-tools
debian:~ # apt install bridge-utils
debian:~ # apt install uml-utilities

```

---

## alpine

```bash
qemu-img create -f qcow2 disk.qcow2 8G
qemu-system-aarch64 -smp 2 \
  -M virt -cpu cortex-a57 -m 1G \
  -initrd initramfs-lts \
  -kernel vmlinuz-lts \
  --append "console=ttyAMA0 ip=dhcp alpine_repo=http://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ modloop=http://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/aarch64/netboot/modloop-lts" \
  -hda disk.qcow2 \
  -netdev user,id=unet -device virtio-net-device,netdev=unet -net user \
  -nographic

# network block device
modprobe nbd max_part=8
lsmod | grep nbd
ls /dev/nbd*
qemu-nbd --connect=/dev/nbd0 disk.qcow2

qemu-nbd: Failed to connect to '0.0.0.0:10809': Connection refused
```

---

## ref

[Debian on QEMU-emulated ARM-64 aarch64](https://phwl.org/2022/qemu-aarch64-debian/)

---

## debian repo

1. repo server

```bash
# download iso
ISO_PATH=/var/www/html/iso
wget https://cdimage.debian.org/debian-cd/current/arm64/iso-cd/debian-11.6.0-arm64-netinst.iso

# mount iso
mkdir -p $ISO_PATH
mount -o loop `pwd`/debian-11.6.0-arm64-netinst.iso $ISO_PATH

# nginx


qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1G -kernel ./linux -initrd ./initrd.gz \
  -hda $VM_DISK -append "console=ttyAMA0" \
  -drive file=mini.iso,id=cdrom,if=none,media=cdrom \
  -device virtio-scsi-device -device scsi-cd,drive=cdrom -nographic

qemu-system-arm -M versatilepb -m 512 \
        -kernel ./install/vmlinuz-3.2.0-4-versatile \
        -initrd ./install/initrd.gz \
        -hda arm.img \
        -append "root=/dev/sda1"

qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1G -kernel ./linux -initrd ./initrd.gz \
  -hda $VM_DISK -append "console=ttyAMA0,root=/dev/sda1" \
  -nographic

```
