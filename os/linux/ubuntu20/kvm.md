# kvm


## virsh

```bash
host:~ # grep 'svm|vmx /proc/cpuinfo
host:~ # apt install qemu-kvm libvirt-daemon
```

```bash
host:~ # virsh
host:~ # virsh help
host:~ # virsh list --all
host:~ # virsh dumpxml <vm_id>|<vm_name>
host:~ # virsh create <vm>.xml
host:~ # virsh define <vm>.xml
host:~ # virsh edit <vm_id>|<vm_name>
host:~ # virsh undefine <vm_id>|<vm_name>

host:~ # virsh start <vm_id>|<vm_name>
host:~ # virsh destroy <vm_id>|<vm_name>
host:~ # virsh console <vm_id>|<vm_name>     # ctrl + ] to exit
```


### setup serial console

```bash
# for systemctl
guest:~ # systemctl enable serial-getty@ttyS0 --enable
```


---

## qemu

```bash
host:~ # qemu-img convert -f qcow2 -O raw image.qcow2 image.img    # qcow2 -> raw
host:~ # qemu-img convert -f vmdk -O raw image.vmdk image.img      # vmdk -> raw
host:~ # qemu-img convert -f raw -O qcow2 image.img image.qcow2    # raw -> qcow2
host:~ # qemu-img convert -f vmdk -O qcow2 image.vmdk image.qcow2  # vmdk -> qcow2
host:~ # qemu-img info image.qcow2  # disk info
```
