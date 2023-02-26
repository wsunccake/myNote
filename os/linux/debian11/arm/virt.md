# virt

## package

```bash
debian:~ # apt intall libvirt-clients
debian:~ # apt intall apt install virt-manager virtinst
debian:~ # apt intall libguestfs-tools
```

---

## virt-builder

```bash
debian:~ # virt-builder --list                                  # list support os
debian:~ # virt-builder --arch aarch64 --size 10G fedora-35     # download image
```

---

## install linux (aarch64) - iso

```bash
# for alpine 3.17.2
debian:~ # VM_NAME=alpine-3.17.2-aarch64
debian:~ # VM_DISK=$VM_NAME-vm.qcow2
debian:~ # ISO_FILE=alpine-standard-3.17.2-aarch64.iso
debian:~ # ISO_URL=https://dl-cdn.alpinelinux.org/alpine/v3.17/releases/aarch64/$ISO_FILE

# for debian 11
debian:~ # VM_NAME=debian-11-aarch64
debian:~ # VM_DISK=$VM_DISK-vm.qcow2
debian:~ # ISO_FILE=debian-11.6.0-arm64-DVD-1.iso
debian:~ # ISO_URL=https://cdimage.debian.org/debian-cd/current/arm64/iso-dvd/$ISO_FILE

# for debian 11 net install
debian:~ # ISO_FILE=mini.iso
debian:~ # ISO_URL=http://ftp.debian.org/debian/dists/bullseye/main/installer-arm64/current/images/netboot/$ISO_FILE

# for fedora 37
debian:~ # VM_NAME=fedora-37-aarch64
debian:~ # VM_DISK=$VM_DISK-vm.qcow2
debian:~ # ISO_FILE=Fedora-Server-dvd-aarch64-37-1.7.iso
debian:~ # ISO_URL=https://download.fedoraproject.org/pub/fedora/linux/releases/37/Server/aarch64/iso/$ISO_FILE

# for ubuntu 22.04
debian:~ # VM_NAME=ubuntu-22.04-aarch64
debian:~ # VM_DISK=$VM_DISK-vm.qcow2
debian:~ # ISO_FILE=ubuntu-22.04.2-live-server-arm64.iso
debian:~ # ISO_URL=https://cdimage.ubuntu.com/releases/22.04/release/$ISO_FILE
```

```bash
debian:~ # wget $ISO_URL
debian:~ # qemu-img create -f qcow2 $VM_DISK 20G

debian:~ # virt-install -v --name $VM_NAME \
  --arch aarch64 \
  --vcpus 4 \
  --ram 4096 \
  --disk path=$VM_DISK,bus=virtio \
  --boot uefi \
  --cdrom $ISO_FILE \
  --import \
  --nographics
```

---

## install linux (aarch64) - raw

```bash
# for fedora 37
debian:~ # VM_NAME=fedora-37-aarch64
debian:~ # VM_DISK=Fedora-Server-37-1.7.aarch64.raw
debian:~ # ISO_URL=https://download.fedoraproject.org/pub/fedora/linux/releases/37/Server/aarch64/iso/$VM_DISK.xz

debian:~ # wget $ISO_URL
debian:~ # xz -d $VM_DISK.xz

# for ubuntu 22.04
debian:~ # VM_NAME=ubuntu-22.04-aarch64
debian:~ # VM_DISK=jammy-server-cloudimg-arm64.img
debian:~ # ISO_URL=http://cloud-images.ubuntu.com/jammy/current/$VM_DISK

debian:~ # wget $ISO_URL
```

```bash
debian:~ # qemu-img create -f qcow2 $VM_DISK 20G

debian:~ # virt-install -v --name $VM_NAME \
  --arch aarch64 \
  --machine virt \
  --vcpus 4 \
  --ram 4096 \
  --disk path=$VM_DISK,bus=virtio \
  --boot uefi \
  --import \
  --nographics
```

---

## install linux (aarch64) - net

```bash
# for alpine 3.17.2
debian:~ # wget https://dl-cdn.alpinelinux.org/alpine/v3.17/releases/aarch64/alpine-netboot-3.17.2-aarch64.tar.gz
debian:~ # tar zxf alpine-netboot-3.17.2-aarch64.tar.gz
debian:~ # KERNEL=boot/vmlinuz-lts
debian:~ # INITRD=boot/initramfs-lts
debian:~ # KERNEL_ARG="console=ttyAMA0 ip=dhcp alpine_repo=http://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ modloop=http://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/aarch64/netboot/modloop-lts"

# for debian 11
debian:~ # wget http://ftp.debian.org/debian/dists/bullseye/main/installer-arm64/current/images/netboot/netboot.tar.gz
debian:~ # tar zxf netboot.tar.gz
debian:~ # KERNEL=debian-installer/arm64/linux
debian:~ # INITRD=debian-installer/arm64/initrd.gz
debian:~ # KERNEL_ARG=""
```

```bash
debian:~ # qemu-img create -f qcow2 $VM_DISK 8G

debian:~ # virt-install -v --name $VM_NAME \
  --arch aarch64 \
  --machine virt \
  --vcpus 4 \
  --ram 4096 \
  --disk path=$VM_DISK,bus=virtio \
  --boot uefi,kernel=$KERNEL,initrd=$INITRD,kernel_args="$KERNEL_ARG" \
  --import \
  --nographics
```

---

## other command

```bash
# list folder
debian:~ # virt-ls -l -a $VM_DISK /boot/

# copy file
debian:~ # virt-copy-out -a $VM_DISK /boot/vmlinuz /boot/initrd.img .

# set password
debian:~ # virt-customize -a $VM_DISK --root-password password:
```
