# isc-dhcp

## port

- dhcp: 67/udp

---

## server

### server - package

```bash
dhcp:~ # zypper in dhcp-server
dhcp:~ # zypper in yast2-dhcp-server
```

### server - config

- method 1 - by yast

```bash
dhcp:~ # yast dhcp-server
```

- method 2 - by manual

```bash
# config
dhcp:~ # vi /etc/dhcpd.conf
```

```conf
# /etc/dhcpd.conf
option domain-name "domain";
option domain-name-servers 8.8.8.8;
option routers 192.168.0.1;
default-lease-time 14400;
ddns-update-style none;
subnet 192.168.0.0 netmask 255.255.255.0 {
  range dynamic-bootp 192.168.0.101 192.168.0.150;
  default-lease-time 14400;
  max-lease-time 172800;
  host hpc1 {
    fixed-address 192.168.0.11;
    hardware ethernet 52:54:00:93:fb:f4;
  }
}

dhcp:~ # dhcpd -t -cf /etc/dhcpd.conf
```

### server - daemon

```bash
dhcp:~ # systemctl start dhcp-server
dhcp:~ # systemctl enable dhcp-server
```

### server - firewall

```bash
dhcp:~ # firewall-cmd --permanent --add-service=dhcp
dhcp:~ # firewall-cmd --permanent --add-service=dhcpv6-client
dhcp:~ # firewall-cmd --reload
```

---

## client

### client - package

```bash
sle:~ # zypper in dhcp-client
```

### client - config

- method 1 - by yast

```bash
sle:~ # yast lan
```

- method 2 - by manual

```bash
# config
sle:~ # vi /etc/sysconfig/network/ifcfg-eth0
BOOTPROTO='dhcp'
STARTMODE='auto'
ZONE=public

sle:~ # wicked ifup eth0
sle:~ # wicked show eth0
sle:~ # dhclient -v -r eth0
```
