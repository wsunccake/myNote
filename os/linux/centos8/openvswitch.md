# openvswitch


## install


```bash
centos:~ # dnf install epel-release
centos:~ # dnf install centos-release-openstack-ussuri
centos:~ # dnf install openvswitch
centos:~ # systemctl enable openvswitch --now
```


---

## ovs-vswitchd

```bash
centos:~ # ovs-vsctl --version
centos:~ # ovs-vsctl show

# bridge
centos:~ # ovs-vsctl list-br
centos:~ # ovs-vsctl add-br <bridge>
centos:~ # ovs-vsctl del-br <bridge>

# port
centos:~ # ovs-vsctl list-ports <bridge>
centos:~ # ovs-vsctl add-port <bridge> <port>
centos:~ # ovs-vsctl del-port <bridge> <port>

# example
centos:~ # ovs-vsctl add-br br0
centos:~ # ovs-vsctl add-port br0 eth0
centos:~ # ip link set br0 up
centos:~ # ip addr add 192.168.0.10/24 dev br0
```


---

## config

### network-scripts

```bash
centos:~ # dnf install network-scripts
centos:~ # systemctl enable network --now
```

network manager don't support openvswitch config, network-script support.


### dhcp

```bash
centos:~ # cat /etc/sysconfig/network-scripts/ifcfg-br0
NAME=br0
DEVICE=br0
DEVICETYPE=ovs
TYPE=OVSBridge
OVSBOOTPROTO=dhcp
OVSDHCPINTERFACES=eth0
ONBOOT=yes
#NM_CONTROLLED=no
DEFROUTE=no

centos:~ # cat /etc/sysconfig/network-scripts/ifcfg-eth0
NAME=eth0
DEVICE=eth0
DEVICETYPE=ovs
TYPE=OVSIntPort
OVS_BRIDGE=br0
ONBOOT=yes
#NM_CONTROLLED=no
```


### static

```bash
centos:~ # cat /etc/sysconfig/network-scripts/ifcfg-br0
NAME=br0
DEVICE=br0
DEVICETYPE=ovs
TYPE=OVSBridge
BOOTPROTO=static
IPADDR=192.168.0.10
NETMASK=255.255.255.0
ONBOOT=yes
#NM_CONTROLLED=no
DEFROUTE=no

centos:~ # cat /etc/sysconfig/network-scripts/ifcfg-eth0
NAME=eth0
DEVICE=eth0
DEVICETYPE=ovs
TYPE=OVSIntPort
OVS_BRIDGE=br0
ONBOOT=yes
#NM_CONTROLLED=no
```


### none

```bash
centos:~ # cat /etc/sysconfig/network-scripts/ifcfg-br0
NAME=br0
DEVICE=br0
DEVICETYPE=ovs
TYPE=OVSBridge
BOOTPROTO=none
ONBOOT=yes
#NM_CONTROLLED=no
DEFROUTE=no

centos:~ # cat /etc/sysconfig/network-scripts/ifcfg-eth0
NAME=eth0
DEVICE=eth0
DEVICETYPE=ovs
TYPE=OVSIntPort
OVS_BRIDGE=br0
ONBOOT=yes
#NM_CONTROLLED=no
```


---

## ref

[Red Hat network scripts integration](https://github.com/openvswitch/ovs/blob/master/rhel/README.RHEL.rst)

