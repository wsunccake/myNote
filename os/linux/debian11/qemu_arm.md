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

## debian arm - netboot install

```bash
debian:~ # IMG_REPO=https://deb.debian.org/debian/dists/bullseye/main/installer-arm64/current/images/netboot

# download
debian:~ # wget $IMG_REPO/debian-installer/arm64/initrd.gz
debian:~ # wget $IMG_REPO/debian-installer/arm64/linux
debian:~ # curl -k -LO $IMG_REPO/mini.iso

# create disk
debian:~ # VM_DISK=debian-3607-aarch64.qcow2
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

---

## ref

[Debian on QEMU-emulated ARM-64 aarch64](https://phwl.org/2022/qemu-aarch64-debian/)
