# ubuntu 24.04

---

## content

---

## network

netplan.io

```bash
ubuntu:~ # dpkg -l netplan.io

ubuntu:~ # vi /etc/netplan/50-cloud-init.yaml
network:
    ethernets:
      ens192:
        dhcp4: no
        addresses:
          - 192.168.10.10/24
        nameservers:
          addresses:
            - 8.8.8.8
        routes:
          - to: 0.0.0.0/0
            via: 192.168.10.254
    version: 2

ubuntu:~ # netplan try
ubuntu:~ # netplan apply
ubuntu:~ # netplan ip leases ens192
```
