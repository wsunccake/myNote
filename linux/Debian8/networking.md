
```
debian8:~ # vi /etc/network/interfaces

source /etc/network/interfaces.d/*
```


## Static IP

```
debian8:~ # vi /etc/network/interfaces.d/ifcfg-em1
auto em1
iface em1 inet static
address 192.168.0.10
gateway 192.168.0.1
netmask 255.255.255.0
dns-nameserver 8.8.8.8
dns-search site

debian8:~ # ifup em1
debian8:~ # ifdown em1
```

## DHCP/Dynamic IP

```
debian8:~ # vi /etc/network/interfaces.d/ifcfg-eth0
auto eth0
iface eth0 inet dhcp


debian8:~ # ifup eth0
debian8:~ # ifdown eth0
```