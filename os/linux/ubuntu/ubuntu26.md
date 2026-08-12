# ubuntu 26.04

## network

### nic

```bash
ubuntu:~ # lspci -v
ubuntu:~ # ls -l /sys/class/net/
ubuntu:~ # ip link
```

### ip

`/etc/netplan/00-installer-config.yaml`

```yaml
network:
  ethernets:
    ens160:
      addresses:
        - 192.168.10.123/24
      match:
        macaddress: 00:11:22:33:44:55
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
        search: []
      routes:
        - to: default
          via: 192.168.10.254
      set-name: ens160
    ens192:
      dhcp4: true
      dhcp6: true
      accept-ra: true
    ens224:
      dhcp4: false
      dhcp6: false
      accept-ra: false
      link-local: [ ]
  version: 2
```

- ens160: up nic, static ip
- ens192: up nic, dhcp / dynamic ip
- ens224: up nic, no ip


```bash
ubuntu:~ # netplan try
ubuntu:~ # netplan apply
ubuntu:~ # ip addr
```
