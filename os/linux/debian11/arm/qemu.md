# qemu-arm

## package

```bash
debian:~ # apt install qemu-system
debian:~ # qemu-system-aarch64 --version

debian:~ # apt install libguestfs-tools
debian:~ # virt-ls --version
```

---

## key

### graphic frontend

```text
Ctrl-Alt-f    Toggle full screen

Ctrl-Alt-+    Enlarge the screen

Ctrl-Alt--    Shrink the screen

Ctrl-Alt-u    Restore the screen’s un-scaled dimensions

Ctrl-Alt-n    Switch to virtual console ‘n’. Standard console mappings are:
         1    Target system display
         2    Monitor
         3    Serial port

Ctrl-Alt      Toggle mouse and keyboard grab.
```

### nographic backend

```text
Ctrl-a h      Print this help

Ctrl-a x      Exit emulator

Ctrl-a s      Save disk data back to file (if -snapshot)

Ctrl-a t      Toggle console timestamps

Ctrl-a b      Send break (magic sysrq in Linux)

Ctrl-a c      Rotate between the frontends connected to the multiplexer (usually this switches between the monitor and the console)

Ctrl-a Ctrl-a Send the escape character to the frontend
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

## ms-dos

download Microsoft MS-DOS 6.0 (Full) from [WinWorld MS-DOS 6.0](https://winworldpc.com/product/ms-dos/6x)

```bash
# create disk
debian:~ # qemu-img create -f qcow msdos.disk 2G

# install
debian:~ # qemu-system-i386 -hda msdos.disk -smp 1 -m 64M -fda Disk1.img -boot a [-L .]

# run
debian:~ # qemu-system-i386 -hda msdos.disk -smp 1 -m 64M -fda Disk1.img -boot c [-nographic]
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

[Keys in the graphical frontends](https://www.qemu.org/docs/master/system/keys.html)

[Keys in the character backend multiplexer](https://www.qemu.org/docs/master/system/mux-chardev.html)
