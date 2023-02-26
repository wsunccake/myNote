# qemu-arm

```bash
qemu-system

mount
losetup --version

kpartx


which qemu-system-aarch64
which qemu-system-arm

```

## ubuntu

```bash
qemu-system-aarch64 -name guest=vm-aarch64,debug-threads=on -S -object secret,id=masterKey0,format=raw,file=/var/lib/libvirt/qemu/domain-5-vm-aarch64/master-key.aes -blockdev {"driver":"file","filename":"/usr/share/AAVMF/AAVMF_CODE.fd","node-name":"libvirt-pflash0-storage","auto-read-only":true,"discard":"unmap"} -blockdev {"node-name":"libvirt-pflash0-format","read-only":true,"driver":"raw","file":"libvirt-pflash0-storage"} -blockdev {"driver":"file","filename":"/var/lib/libvirt/qemu/nvram/vm-aarch64_VARS.fd","node-name":"libvirt-pflash1-storage","auto-read-only":true,"discard":"unmap"} -blockdev {"node-name":"libvirt-pflash1-format","read-only":false,"driver":"raw","file":"libvirt-pflash1-storage"} -machine virt-5.2,accel=tcg,usb=off,dump-guest-core=off,gic-version=2,pflash0=libvirt-pflash0-format,pflash1=libvirt-pflash1-format,memory-backend=mach-virt.ram -cpu cortex-a57 -m 1024 -object memory-backend-ram,id=mach-virt.ram,size=1073741824 -overcommit mem-lock=off -smp 1,sockets=1,cores=1,threads=1 -uuid fbef4025-fb99-46dd-b5cb-fdd28a6e833a -display none -no-user-config -nodefaults -chardev socket,id=charmonitor,fd=34,server,nowait -mon chardev=charmonitor,id=monitor,mode=control -rtc base=utc -no-reboot -boot strict=on -device pcie-root-port,port=0x8,chassis=1,id=pci.1,bus=pcie.0,multifunction=on,addr=0x1 -device pcie-root-port,port=0x9,chassis=2,id=pci.2,bus=pcie.0,addr=0x1.0x1 -device pcie-root-port,port=0xa,chassis=3,id=pci.3,bus=pcie.0,addr=0x1.0x2 -device pcie-root-port,port=0xb,chassis=4,id=pci.4,bus=pcie.0,addr=0x1.0x3 -device pcie-root-port,port=0xc,chassis=5,id=pci.5,bus=pcie.0,addr=0x1.0x4 -device pcie-root-port,port=0xd,chassis=6,id=pci.6,bus=pcie.0,addr=0x1.0x5 -device qemu-xhci,p2=15,p3=15,id=usb,bus=pci.2,addr=0x0 -device virtio-scsi-pci,id=scsi0,bus=pci.3,addr=0x0 -device virtio-serial-pci,id=virtio-serial0,bus=pci.4,addr=0x0 -blockdev {"driver":"file","filename":"/var/lib/libvirt/images/vm-aarch64.qcow2","node-name":"libvirt-2-storage","auto-read-only":true,"discard":"unmap"} -blockdev {"node-name":"libvirt-2-format","read-only":false,"driver":"qcow2","file":"libvirt-2-storage","backing":null} -device virtio-blk-pci,bus=pci.5,addr=0x0,drive=libvirt-2-format,id=virtio-disk0,bootindex=2 -blockdev {"driver":"file","filename":"/home/img/ubuntu-22.04.1-live-server-arm64.iso","node-name":"libvirt-1-storage","auto-read-only":true,"discard":"unmap"} -blockdev {"node-name":"libvirt-1-format","read-only":true,"driver":"raw","file":"libvirt-1-storage"} -device scsi-cd,bus=scsi0.0,channel=0,scsi-id=0,lun=0,device_id=drive-scsi0-0-0-0,drive=libvirt-1-format,id=scsi0-0-0-0,bootindex=1 -netdev tap,fd=36,id=hostnet0 -device virtio-net-pci,netdev=hostnet0,id=net0,mac=52:54:00:73:0f:51,bus=pci.1,addr=0x0 -chardev pty,id=charserial0 -serial chardev:charserial0 -chardev socket,id=charchannel0,fd=37,server,nowait -device virtserialport,bus=virtio-serial0.0,nr=1,chardev=charchannel0,id=channel0,name=org.qemu.guest_agent.0 -sandbox on,obsolete=deny,elevateprivileges=deny,spawn=deny,resourcecontrol=deny -msg timestamp=on
hsikai      9500  0.0  0.0   6180   720 pts/4    S+   20:36   0:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox aarch
```

## alpine - install mini root filesystem

```bash
debian:~ # IMG_REPO=https://dl-cdn.alpinelinux.org/alpine/v3.17/releases/aarch64
debian:~ # UBOOT_TGZ=alpine-uboot-3.17.2-aarch64.tar.gz
debian:~ # ROOTFG_TGZ=alpine-minirootfs-3.17.2-aarch64.tar.gz
debian:~ # VM_DISK=alpine-aarch64.img

# download
debian:~ # wget $IMG_REPO/$UBOOT_TGZ
debian:~ # curl -k -LO $IMG_REPO/$ROOTFG_TGZ

# create image file
debian:~ # qemu-img create -f raw $VM_DISK 512M

# mount image to loop
debian:~ # losetup /dev/loop0 $VM_DISK
debian:~ # lsblk
debian:~ # fdisk /dev/loop0

# add partition table mapper
debian:~ # kpartx -av /dev/loop0
debian:~ # ls /dev/mapper/loop0*

# format filesystem
debian:~ # mkfs.ext4 /dev/mapper/loop0p1
debian:~ # mount -t ext4 /dev/mapper/loop0p1 /mnt

# copy file to mount point
debian:~ # tar zxf $UBOOT_TGZ -C /mnt/
debian:~ # tar zxf $ROOTFG_TGZ -C /mnt/
debian:~ # cp /mnt/boot/initramfs-lts .
debian:~ # cp /mnt/boot/vmlinuz-lts .

debian:~ # umount /mnt
debian:~ # kpartx -dv /dev/loop0
debian:~ # losetup -d /dev/loop0



qemu-system-arm -sd sd.img -m 256 -M vexpress-a9 -dtb boot/dtbs/vexpress-v2p-ca9.dtb -kernel boot/vmlinuz-hardened -initrd boot/initramfs-hardened -append "modules=loop,squashfs,sd-mod,usb-storage,ext4 modloop=/boot/modloop-hardened root=/dev/mmcblk0 console=ttyAMA0" -nographic


qemu-system-aarch64 -machine

qemu-system-aarch64 -sd $VM_DISK -m 256 -M vexpress-a9 \
  -dtb vexpress-v2f-1xv7-ca53x2.dtb \
  -kernel vmlinuz-lts \
  -initrd initramfs-lts \
  -append "modules=loop,squashfs,sd-mod,usb-storage,ext4 modloop=/boot/modloop-hardened root=/dev/mmcblk0 console=ttyAMA0" \
  -drive format=raw,file=$VM_DISK \
  -nographic

qemu-system-aarch64 -sd $VM_DISK -smp 2 \
  -M virt -cpu cortex-a57 -m 1G \
  -kernel vmlinuz-lts \
  -initrd initramfs-lts \
  -append "console=ttyAMA0 root=/dev/vda3 rw rootfstype=ext4" \
  -nographic


qemu-system-aarch64 -smp 2 \
  -M virt -cpu cortex-a57 -m 1G \
  -initrd initramfs-lts.img \
  -kernel vmlinuz-lts.img \
  --append "console=ttyAMA0 root=/dev/vda3 rw rootfstype=ext4" \
  -hda disk.qcow2 \
  -device e1000,netdev=net0 \
  -net nic -netdev user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
  -nographic
```

---

## alpine arm64 - netboot install

```bash
debian:~ # IMG_REPO=dl-cdn.alpinelinux.org/alpine/latest-stable/releases/aarch64/netboot
debian:~ # PKG_REPO=dl-cdn.alpinelinux.org/alpine/latest-stable/main
debian:~ # VM_DISK=alpine-aarch64.qcow2

# download
debian:~ # curl -k -LO https://$IMG_REPO/vmlinuz-lts
debian:~ # curl -k -LO https://$IMG_REPO/initramfs-lts

# create disk
debian:~ # qemu-img create -f qcow2 $VM_DISK 8G

# install
debian:~ # qemu-system-aarch64 -smp 2 \
  -M virt -cpu cortex-a57 -m 1G \
  -initrd initramfs-lts \
  -kernel vmlinuz-lts \
  --append "console=ttyAMA0 ip=dhcp alpine_repo=http://$PKG_REPO/ modloop=http://$IMG_REPO/modloop-lts" \
  -hda $VM_DISK \
  -netdev user,id=unet -device virtio-net-device,netdev=unet -net user \
  -nographic

# install alpine
(alpine):~ # setup-alpine
...

debina:~ # mkdir netboot
debian:~ # mv initramfs-lts vmlinuz-lts netboot/.
debian:~ # virt-ls -l -a $VM_DISK /boot
debian:~ # virt-copy-out -a $VM_DISK /boot/initramfs-lts /boot/vmlinuz-lts .

debian:~ # qemu-system-aarch64 -smp 2 \
  -M virt -cpu cortex-a57 -m 1G \
  -initrd initramfs-lts \
  -kernel vmlinuz-lts \
  --append "console=ttyAMA0 root=/dev/vda3 rw rootfstype=ext4" \
  -hda $VM_DISK \
  -device e1000,netdev=net0 \
  -net nic -netdev user,hostfwd=tcp:127.0.0.1:2222-:22,id=net0 \
  -nographic



#
qemu-system-aarch64 -smp 2 \
  -M virt -cpu cortex-a57 -m 1G \
  -initrd initramfs-lts \
  -kernel vmlinuz-lts \
  --append "console=ttyAMA0 ip=dhcp alpine_repo=http://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ modloop=http://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/aarch64/netboot/modloop-lts" \
  -hda disk.qcow2 \
  -netdev user,id=unet -device virtio-net-device,netdev=unet -net user \
  -nographic
```

[Run Alpine on QEMU aarch64 Virtual Machine](https://hackmd.io/@starnight/Run_Alpine_on_QEMU_aarch64_Virtual_Machine)

[Build Alpine’s Root Filesystem (Bootstrap)](https://hackmd.io/@starnight/Build_Alpines_Root_Filesystem_Bootstrap)

[Deploy an ARM64 Fedora VM on your PC: 3 steps](https://www.redhat.com/sysadmin/vm-arm64-fedora)

```
qemu-system-aarch64 -nographic -m 4096M -cpu cortex-a57 -smp 4 \
	-netdev user,id=unet -device virtio-net-pci,netdev=unet \
    -drive file=f36 -M virt \
    -bios /usr/share/edk2/aarch64/QEMU_EFI.fd

  edk2-aarch64 package to have QEMU_EFI.fd
```
