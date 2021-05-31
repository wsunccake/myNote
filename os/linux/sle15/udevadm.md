# udevadm

## sr-iov 

### nic

```bash
# check support
sle:~ # grep -E "(vmx|svm)" /proc/cpuinfo  # for intel -> vmx, for amd -> svm
sle:~ # dmesg | grep -e DMAR -e IOMMU      # for intel
sle:~ # dmesg | grep AMD-Vi                # for amd

# check device
sle:~ # lspci | grep -i ethernet
sle:~ # lspci -s <bus>:<device>.<func> -v | grep -i sr-iov
sle:~ # lspci -s 04:00.1 -v | grep -i sr-iov

# boot option
sle:~ # vi /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="splash=silent resume=/dev/md0p2 intel_pstate=disable intel_iommu=on iommu=pt mitigations=auto quiet crashkernel=202M,high crashkernel=72M,low"
...
# grub
sle:~ # grub2-mkconfig -o /boot/grub2/grub.cfg

# udev
sle:~ # vi /etc/udev/rules.d/69-persistent-net_vf_num.rules
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="ixgbe|i40e", ATTR{dev_id}=="0x0", ATTR{type}=="1", ATTR{device/sriov_numvfs}="8"

sle:~ # vi /etc/udev/rules.d/70-persistent-net.rules
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="ac:1f:6b:40:00:10", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="eth*", NAME="ixgbe0", RUN+="/bin/sh -c '/sbin/udevadm trigger --sysname-match=ixgbe0'"
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="ac:1f:6b:90:00:20", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="eth*", NAME="i40e0", RUN+="/bin/sh -c '/sbin/udevadm trigger --sysname-match=i40e0'"

sle:~ # vi /etc/udev/rules.d/72-persistent-net_vf_mac_addr.rules
SUBSYSTEM=="net", ACTION=="add|change", DRIVERS=="?*", KERNEL=="ixgbe0", RUN+="/bin/sh -c 'ip link set %k up; for num in {0..7}; do ip link set %k vf ${num} mac ac:1f:6b:40:0${num}:10; done'"
SUBSYSTEM=="net", ACTION=="add|change", DRIVERS=="?*", KERNEL=="i40e0", RUN+="/bin/sh -c 'ip link set %k up; for num in {0..7}; do ip link set %k vf ${num} mac ac:1f:6b:90:0${num}:20; done'"

sle:~ # rmmod ixgbe
sle:~ # modprobe ixgbe

sle:~ # udevadm control --reload
sle:~ # udevadm trigger
sle:~ # udevadm info /sys/class/net/ixgbe0
sle:~ # udevadm info -a /sys/class/net/ixgbe0
sle:~ # udevadm info -q path /sys/class/net/ixgbe0
sle:~ # udevadm test /sys/class/net/ixgbe0
sle:~ # ls /sys/class/net/ixgbe0/

sle:~ # ls -ld /sys/class/net/ixgbe0/device/virtfn*
/sys/class/net/ixgbe0/device/virtfn0 -> ../0000:06:10.0
/sys/class/net/ixgbe0/device/virtfn1 -> ../0000:06:10.2
...

sle:~ # lspci
06:10.0 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
06:10.1 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
06:10.2 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
...
```
