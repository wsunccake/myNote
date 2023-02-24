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

## alpine arm - iso

```bash
debian:~ # IMG_REPO=https://dl-cdn.alpinelinux.org/alpine/v3.17/releases
debian:~ # curl -k -LO $IMG_REPO/aarch64/alpine-standard-3.17.2-aarch64.iso
```

使用 virt-manager 安裝, 選用 local install media (ISO image or CDROM), architecture 選用 aarch64, machine 選用 virt

---

## other

```bash
# list qemu support
debian:~ # qemu-system-aarch64 -machine help
debian:~ # qemu-system-aarch64 -cpu help

# mount qemu image
debian:~ # losetup /dev/loop0 $VM_DISK
debian:~ # lsblk
debian:~ # kpartx -av /dev/loop0
debian:~ # ls /dev/mapper/loop0*
debian:~ # mount /dev/loop0p1 /mnt

# umount qemu image
debian:~ # umount /mnt
debian:~ # kpart -dv /dev/loop0
debian:~ # losetup -d /dev/loop0

# nbd
debian:~ # modprobe nbd max_part=8
debian:~ # lsmod nbd
```

---

## ref

[Debian on QEMU-emulated ARM-64 aarch64](https://phwl.org/2022/qemu-aarch64-debian/)
