
# Networking

```
debian8:~ # systemctl start networking.service
debian8:~ # systemctl stop networking.service
debian8:~ # systemctl status networking.service

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
allow-hotplug eth0
iface eth0 inet dhcp

debian8:~ # ifup eth0
debian8:~ # ifdown eth0
```

## Bridge

```
# DHCP
debian:~# vi ifcfg-br0 
auto br0
iface br0 inet dhcp
  bridge_ports eth0
  up /usr/sbin/brctl stp br0 off

debian:~# vi /etc/network/interfaces.d/ifcfg-eth0
auto eth0
allow-hotplug eth0
iface eth0 inet manual
  pre-up ifconfig $IFACE up
  pre-down ifconfig $IFACE down
```

# NetworkManager