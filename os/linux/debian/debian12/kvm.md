# kam

## install

```bash
# check kernel module
debian:~ # lsmod | grep -E 'kvm-intel|kvm-amd'

# install package
debian:~ # apt install qemu-system libvirt-daemon-system virt-manager

# add user to group
debian:~ # adduser <user> libvirt
```

---

## usage

```bash
debian:~ # virsh            # cli
debian:~ # virt-manager     # gui
```

### virsh

```bash
debian:~ # virsh help
debian:~ # virsh list --all
debian:~ # virsh dumpxml <domain name>
debian:~ # virsh console <domain name>

# register / un-register vm
debian:~ # virsh define <xml>
debian:~ # virsh undefine <domain name> [--nvram]

# register and start vm
debian:~ # virsh create <xml>

# start / stop vm
debian:~ # virsh start <domain name>
debian:~ # virsh destroy <domain name>
```

### virt-

```bash
debian:~ # virt-install
debian:~ # virt-manager
```

### qemu-

```bash
# disk
debian:~ # qemu-img info image.qcow2                                     # disk info
debian:~ # qemu-img create  -f qcow2 image.qcow2 50G                     # create qcow2 image
debian:~ # qemu-img convert -f qcow2 -O raw   image.qcow2 image.img      # qcow2 -> raw
debian:~ # qemu-img convert -f vmdk  -O raw   image.vmdk  image.img      # vmdk -> raw
debian:~ # qemu-img convert -f raw   -O qcow2 image.img   image.qcow2    # raw -> qcow2
debian:~ # qemu-img convert -f vmdk  -O qcow2 image.vmdk  image.qcow2    # vmdk -> qcow2

# mount
debian:~ # modprobe nbd max_part=8
debian:~ # lsmod nbd
debian:~ # qemu-nbd -c /dev/nbd0 image.qcow2
debian:~ # fdis-l /dev/nbd0
debian:~ # lsblk
debian:~ # mount /dev/nbd0p1 /mnt
debian:~ # umount  /mnt
debian:~ # qemu-nbd -d /dev/nbd0
debian:~ # modprobe -r nbd
```
