# ubuntu 20

## network

netplan.io

```bash
[ubuntu:~ ] # dpkg -l netplan.io

[ubuntu:~ ] # vi /etc/netplan/00-installer-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens192:
      dhcp4: no
      addresses:
        - 192.168.1.11/24
      gateway4: 192.168.1.1
      nameservers:
         addresses:
           - 192.168.1.1
           - 8.8.8.8
    ens172:
      dhcp4: yes
      dhcp4-overrides:
        use-routes: false
    ens2: {}
  vlans:
    vlan100:
      id: 100
      link ens2

[ubuntu:~ ] # netplan try
[ubuntu:~ ] # netplan apply

[ubuntu:~ ] # ls /run/systemd/network/                  # auto generate systemd script
[ubuntu:~ ] # ls /usr/share/doc/netplan/examples/       # setup example
```


---

## development

### openjdk

```bash
[ubuntu:~ ] # apt install openjdk-11-jdk
```


---

## terminal

### zsh

```bash
[ubuntu:~ ] # apt install zsh
```

