# openvswitch

```bash
# ovs-vswitchd
centos:~ # ovs-vsctl --version
centos:~ # ovs-vsctl show

centos:~ # ovs-vsctl list-br
centos:~ # ovs-vsctl add-br <bridge>
centos:~ # ovs-vsctl del-br <bridge>

centos:~ # ovs-vsctl list-ports <bridge>
centos:~ # ovs-vsctl add-port <bridge> <port>
centos:~ # ovs-vsctl del-port <bridge> <port>
```

