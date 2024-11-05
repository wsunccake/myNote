# networking

## network interface naming

```bash
# udev device manage re-naming network interface
rocky:~ # ls /usr/lib/udev/rules.d/60-net.rules                 # using /usr/lib/udev/rename_device
rocky:~ # ls /usr/lib/udev/rules.d/71-biosdevname.rules         # on Dell, using biosdevname
rocky:~ # ls /usr/lib/udev/rules.d/75-net-description.rules
rocky:~ # ls /usr/lib/udev/rules.d/80-net-setup-link.rules

# network interface naming policy
rocky:~ # grep NamePolicy /usr/lib/systemd/network/99-default.link
NamePolicy=keep kernel database onboard slot path
# keep
# kernel
# database
# onboard
# slot
# path
# mac
```

```bash
# switch network interface naming scheme
rocky:~ # ip link show
ip link show
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:90:d6:15 brd ff:ff:ff:ff:ff:ff
rocky:~ # udevadm info --query=property --property=ID_NET_NAMING_SCHEME /sys/class/net/enp0s3
ID_NET_NAMING_SCHEME=rhel-9.0
rocky:~ # grubby --update-kernel=ALL --args=net.naming-scheme=rhel-9.4
ID_NET_NAMING_SCHEME=rhel-9.0
rocky:~ # reboot
rocky:~ # udevadm info --query=property --property=ID_NET_NAMING_SCHEME /sys/class/net/enp0s3
ID_NET_NAMING_SCHEME=rhel-9.4
```

```bash
# user-defined network interface name by udev rule
rocky:~ # ip link show
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:90:d6:15 brd ff:ff:ff:ff:ff:ff
rocky:~ # cat /sys/class/net/enp0s3/type
1
rocky:~ # vi /etc/udev/rules.d/70-persistent-net.rules
# SUBSYSTEM=="net",ACTION=="add",ATTR{address}=="<MAC_address>",ATTR{type}=="<device_type_id>",NAME="<new_interface_name>"
SUBSYSTEM=="net",ACTION=="add",ATTR{address}=="08:00:27:90:d6:15",ATTR{type}=="1",NAME="provider0"
rocky:~ # reboot
rocky:~ # ip link show
```

```bash
# user-defined network interface names by using systemd link files
rocky:~ # ip link show
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:90:d6:15 brd ff:ff:ff:ff:ff:ff
rocky:~ # mkdir -p /etc/systemd/network/
rocky:~ # vi /etc/systemd/network/70-provider0.link
[Match]
MACAddress=08:00:27:90:d6:15

[Link]
Name=provider0

rocky:~ # dracut -f
rocky:~ # reboot
rocky:~ # ip link show
```

---

## ethernet

### check network

```bash
rocky:~ # nmcli connection modify <connection-name> <setting> <value>
rocky:~ # nmcli connection up <connection-name>
rocky:~ # ip address show
rocky:~ # ip route show default
rocky:~ # ip -6 route show default
rocky:~ # cat /etc/resolv.conf
rocky:~ # ping <host-name-or-IP-address>
rocky:~ # ping -6 <host-name-or-IP-address>
```

### ethernet connection by nmcli

```bash
rocky:~ # nmcli connection show
rocky:~ # nmcli connection add con-name <connection-name> ifname <device-name> type ethernet
rocky:~ # nmcli connection show <connection-name>

# DHCP
rocky:~ # nmcli connection modify <connection-name> ipv4.method auto
rocky:~ # nmcli connection modify <connection-name> ipv4.method auto

# static IPv4
rocky:~ # nmcli connection modify <connection-name> ipv4.method manual ipv4.addresses 192.0.2.1/24 ipv4.gateway 192.0.2.254 ipv4.dns 192.0.2.200 ipv4.dns-search example.com

# SLAAC
rocky:~ # nmcli connection modify <connection-name> ipv6.method auto

# static IPv6
rocky:~ # nmcli connection modify <connection-name> ipv6.method manual ipv6.addresses 2001:db8:1::fffe/64 ipv6.gateway 2001:db8:1::fffe ipv6.dns 2001:db8:1::ffbb ipv6.dns-search example.com
```

### ethernet connection by nmcli interactive

```bash
rocky:~ # nmcli connection show
rocky:~ # nmcli connection edit type ethernet con-name "<connection-name>"
rocky:~ # nmcli connection edit con-name "<connection-name>"
nmcli> set connection.id <connection-name>
nmcli> print
nmcli> set connection.interface-name <device-name>

# DHCP
nmcli> set ipv4.method auto

# static IPv4
nmcli> ipv4.addresses 192.0.2.1/24
Do you also want to set 'ipv4.method' to 'manual'? [yes]: yes
nmcli> ipv4.gateway 192.0.2.254
nmcli> ipv4.dns 192.0.2.200
nmcli> ipv4.dns-search example.com

# SLAAC
nmcli> set ipv6.method auto

# static IPv6
nmcli> ipv6.addresses 2001:db8:1::fffe/64
Do you also want to set 'ipv6.method' to 'manual'? [yes]: yes
nmcli> ipv6.gateway 2001:db8:1::fffe
nmcli> ipv6.dns 2001:db8:1::ffbb
nmcli> ipv6.dns-search example.com

nmcli> save persistent
nmcli> quit
```

### ethernet connection by nmtui (tui)

```bash
rocky:~ # nmcli device status
rocky:~ # nmtui
```

### ethernet connection by control-center (gui)

```bash
rocky:~ # control-center
```

### ethernet connection by nm-connection-editor (gui)

```bash
rocky:~ # nm-connection-editor
```

### ethernet connection by nmstatectl

```bash
# with a static IP address
rocky:~ # nmstatectl apply static-ip.yml

# with a dynamic IP address
rocky:~ # nmstatectl apply dynamic-ip.yml

rocky:~ # nmstatectl show enp1s0
```

```yaml
# static-ip.yml
---
interfaces:
  - name: enp1s0
    type: ethernet
    state: up
    ipv4:
      enabled: true
      address:
        - ip: 192.0.2.1
          prefix-length: 24
      dhcp: false
    ipv6:
      enabled: true
      address:
        - ip: 2001:db8:1::1
          prefix-length: 64
      autoconf: false
      dhcp: false
routes:
  config:
    - destination: 0.0.0.0/0
      next-hop-address: 192.0.2.254
      next-hop-interface: enp1s0
    - destination: ::/0
      next-hop-address: 2001:db8:1::fffe
      next-hop-interface: enp1s0
dns-resolver:
  config:
    search:
      - example.com
    server:
      - 192.0.2.200
      - 2001:db8:1::ffbb
```

```yaml
# dynamic-ip.yml
---
interfaces:
  - name: enp1s0
    type: ethernet
    state: up
    ipv4:
      enabled: true
      auto-dns: true
      auto-gateway: true
      auto-routes: true
      dhcp: true
    ipv6:
      enabled: true
      auto-dns: true
      auto-gateway: true
      auto-routes: true
      autoconf: true
      dhcp: true
```

---

## network bond

| bond mode         | switch configure                                         |
| ----------------- | -------------------------------------------------------- |
| 0 - balance-rr    | require static EtherChannel enabled, not -negotiated     |
| 1 - active-backup | no configuration                                         |
| 2 - balance-xor   | require static EtherChannel enabled, not LACP-negotiated |
| 3 - broadcast     | require static EtherChannel enabled, not LACP-negotiated |
| 4 - 802.3ad       | require LACP-negotiated EtherChannel enabled             |
| 5 - balance-tlb   | no configuration                                         |
| 6 - balance-alb   | no configuration                                         |

LACP / Link Aggregation Control Protocol

### network bond by nmcli

```bash
rocky:~ # nmcli connection add type bond con-name bond0 ifname bond0 bond.options "mode=active-backup,miimon=1000"

rocky:~ # nmcli device status
DEVICE   TYPE      STATE         CONNECTION
enp7s0   ethernet  disconnected  --
enp8s0   ethernet  disconnected  --
bridge0  bridge    connected     bridge0
bridge1  bridge    connected     bridge1

# no configure
rocky:~ # nmcli connection add type ethernet port-type bond con-name bond0-port1 ifname enp7s0 controller bond0
rocky:~ # nmcli connection add type ethernet port-type bond con-name bond0-port2 ifname enp8s0 controller bond0

# existing connection profile
rocky:~ # nmcli connection modify bridge0 controller bond0
rocky:~ # nmcli connection modify bridge1 controller bond0
rocky:~ # nmcli connection up bridge0
rocky:~ # nmcli connection up bridge1
```

```bash
# as other device enter
rocky:~ # nmcli connection modify bond0 ipv4.method disabled

# DHCP, no action is required

# static IPv4
rocky:~ # nmcli connection modify bond0 ipv4.addresses '192.0.2.1/24' ipv4.gateway '192.0.2.254' ipv4.dns '192.0.2.253' ipv4.dns-search 'example.com' ipv4.method manual

# as other device enter
rocky:~ # nmcli connection modify bond0 ipv6.method disabled

# SLAAC, no action is required

# static IPv6
rocky:~ # nmcli connection modify bond0 ipv6.addresses '2001:db8:1::1/64' ipv6.gateway '2001:db8:1::fffe' ipv6.dns '2001:db8:1::fffd' ipv6.dns-search 'example.com' ipv6.method manual

rocky:~ # nmcli connection up bond0
rocky:~ # nmcli device
DEVICE   TYPE      STATE      CONNECTION
...
enp7s0   ethernet  connected  bond0-port1
enp8s0   ethernet  connected  bond0-port2

rocky:~ # cat /proc/net/bonding/bond0
```

### network bond by web console / cockpit (web)

### network bond by nmtui (tui)

```bash
rocky:~ # nmtui
```

### network bond by nm-connection-editor (gui)

```bash
rocky:~ # nm-connection-editor
```

### network bond by nmstatectl

```yaml
# bond.yml
---
interfaces:
  - name: bond0
    type: bond
    state: up
    ipv4:
      enabled: true
      address:
        - ip: 192.0.2.1
          prefix-length: 24
      dhcp: false
    ipv6:
      enabled: true
      address:
        - ip: 2001:db8:1::1
          prefix-length: 64
      autoconf: false
      dhcp: false
    link-aggregation:
      mode: active-backup
      port:
        - enp1s0
        - enp7s0
  - name: enp1s0
    type: ethernet
    state: up
  - name: enp7s0
    type: ethernet
    state: up

routes:
  config:
    - destination: 0.0.0.0/0
      next-hop-address: 192.0.2.254
      next-hop-interface: bond0
    - destination: ::/0
      next-hop-address: 2001:db8:1::fffe
      next-hop-interface: bond0

dns-resolver:
  config:
    search:
      - example.com
    server:
      - 192.0.2.200
      - 2001:db8:1::ffbb
```

```bash
rocky:~ # nmstatectl apply bond.yml
```

---

## nic team
