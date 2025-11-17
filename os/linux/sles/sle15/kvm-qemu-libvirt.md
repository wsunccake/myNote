# kvm - qemu - libvirt

- KVM (Kernel-based Virtual Machine): 提供核心的虛擬化硬體加速基礎結構。
- QEMU (Quick Emulator): 負責模擬硬體並管理虛擬機進程。
- Libvirt: 透過提供統一的 API 和工具，充當管理階層，控制和協調 KVM 和 QEMU 等虛擬化組件。

## install

```bash
sle:~ # zypper in qemu-kvm libvirt virt-install

sle:~ # grep -E 'svm|vmx' /proc/cpuinfo
sle:~ # lsmod | grep kvm

sle:~ # systemctl start  libvirtd
sle:~ # systemctl enable libvirtd
sle:~ # systemctl status libvirtd
```

---

## setup

### nic

```bash
# create bridge
# 1. by yast
sle:~ # ysat lan

# 2. by edit
sle:~ # mv /etc/sysconfig/network/ifcfg-eth0 /etc/sysconfig/network/ifcfg-br0
sle:~ # cat << EOF >> /etc/sysconfig/network/ifcfg-br0
BRIDGE='yes'
BRIDGE_FORWARDDELAY='0'
BRIDGE_PORTS='eth0'
BRIDGE_STP='off'
sle:~ # echo "default <default gateway> - <br>" > /etc/sysconfig/network/routes
sle:~ # systemctl restart wickedd wicked
sle:~ # ip addr
```

---

## usage

### gui

```bash
sle:~ # zypper in virt-manager
sle:~ # virt-manager
```

### cli

```bash
sle:~ # zypper in libvirt-client
sle:~ # virsh
sle:~ # virsh help

sle:~ # virsh [-c qemu:///system] uri
sle:~ # virsh [-c qemu+ssh://<user>@<ip>/system] uri
sle:~ # virsh list [--all]

sle:~ # virsh dumpxml <domain name>
sle:~ # virsh console <domain name>

# register / un-register vm
sle:~ # virsh define <xml>
sle:~ # virsh undefine <domain name> [--nvram]
sle:~ # virsh undefine <domain name> --storage /path/vdisk.qcow2 --wipe-storage|

# register and start vm
sle:~ # virsh create <xml>

# start / stop vm
sle:~ # virsh start <domain name> [--console]
sle:~ # virsh destroy <domain name>
sle:~ # virsh autostart [--disable] <domain name>

sle:~ # virsh vol-create-as --pool default <vdisk> 120M --format qcow2
sle:~ # virsh vol-upload --pool default <vdisk> <img>
```

```bash
# create a Storage Pool directory
sle:~ # mkdir -p /var/kvm/images
sle:~ # virt-install \
--name sle15 \
--ram 4096 \
--disk path=/var/kvm/images/sle15.img,size=30 \
--vcpus 2 \
--os-type linux \
--os-variant sle15 \
--network bridge=br0 \
--graphics none \
--console pty,target_type=serial \
--location /tmp/SLE-15-Installer-DVD-x86_64-GM-DVD1.iso \
--extra-args 'console=ttyS0,115200n8 serial'
Starting install...     # installation starts

linux-6am4:~ #          # Ctrl + ] key
```

---

## SPICE / Simple Protocol for Independent Computing Environment

```bash
sle:~ # zypper in libspice-server1

sle:~ # virsh dumpxml <domain name>
...
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
...

sle:~ # virsh edit <domain name>
...
    <graphics type='spice' port='5900' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
...
```

```bash
sle:~ # virt-viewer [-c qemu:///system] [domain name]
```

```bash
sle:~ $ sudo virt-viewer
Could not connect: Connection refused
(virt-viewer:1067269): Gtk-WARNING **: 02:37:07.414: cannot open display: :1.0

sle:~ $ xhost
sle:~ $ xhost +si:localuser:root
sle:~ $ xhost -si:localuser:root
```
