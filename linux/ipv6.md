# IPv6


## Status

```
  +-------------------+-------------------------+
  RA                  DHCPv6                   Client
eth0 ipv6 2001::1/64  eth0 ipv6 2001::2/64     eth0 ipv6
```


## port

`DHCPv6`

server 547/udp

client 546/udp

## package

`RA`

```bash
ra:~ # yum install radvd
```

`DHCPv6`

```bash
dhcp:~ # yum install dhcp
```


## Only RA

`ra`

```bash
ra:~ # sysctl -w net.ipv6.conf.all.forwarding=1

ra:~ # vi /etc/radvd.conf
interface eth0
{
        AdvSendAdvert on;
        MinRtrAdvInterval 30;
        MaxRtrAdvInterval 100;

        AdvManagedFlag off;
        AdvOtherConfigFlag off;

        prefix 2001::/64
        {
                AdvOnLink on;
                AdvAutonomous on;
                AdvRouterAddr off;
        };

        RDNSS 2001::a
        {
                AdvRDNSSLifetime 30;
        };

};

ra:~ # systemctl start radvd.service
ra:~ # systemctl enable radvd.service
```

`client`

```bash
client:~ # ip addr show dev eth0    # check ip
client:~ # ip -6 route show         # check route
client:~ # cat /etc/resovl.conf     # check dns
client:~ # ping6 2001::1            # check traffic
```

prefix mask must be /64, prefix:host_mac


---

## Stateless DHCPv6

`ra`

```bash
ra:~ # sysctl -w net.ipv6.conf.all.forwarding=1

ra:~ # vi /etc/radvd.conf
interface eth0
{
        AdvSendAdvert on;
        MinRtrAdvInterval 30;
        MaxRtrAdvInterval 100;

        AdvManagedFlag off;
        AdvOtherConfigFlag on;

        prefix 2001::/64
        {
                AdvOnLink on;
                AdvAutonomous on;
                AdvRouterAddr off;
        };
};

ra:~ # systemctl start radvd.service
ra:~ # systemctl enable radvd.service
```

`dhcp`

```bash
dhcp:~ # vi /etc/dhcp/dhcpd6.conf
option dhcp6.name-servers 2001::a;

dhcp:~ # systemctl start dhcpd6.service
dhcp:~ # systemctl enable dhcpd6.service
```


## Stateful DHCPv6

`ra`

```bash
ra:~ # sysctl -w net.ipv6.conf.all.forwarding=1

ra:~ # vi /etc/radvd.conf
interface eth0
{
        AdvSendAdvert on;
        MinRtrAdvInterval 30;
        MaxRtrAdvInterval 100;

        AdvManagedFlag on;
        AdvOtherConfigFlag on;

        prefix 2001::/64
        {
                AdvOnLink on;
                AdvAutonomous off;
                AdvRouterAddr on;
        };
};

ra:~ # systemctl start radvd.service
ra:~ # systemctl enable radvd.service
```

`dhcp`

```bash
dhcp:~ # vi /etc/dhcp/dhcpd6.conf
subnet6 2001::/64 {
    interface eth1;
    range6 2000::100 2000::200;
    default-lease-time 345600;
    max-lease-time 518400;
}


dhcp:~ # systemctl start dhcpd6.service
dhcp:~ # systemctl enable dhcpd6.service
```


---

