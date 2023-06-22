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
debian:~ # qemu-img
```
