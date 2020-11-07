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

