# dnsmasq

## install

```bash
server:~ # sudo apt-get install dnsmasq
```

---

## configuaration

```bash
server:~ # cat /etc/dnsmasq.conf

# DHCP
bind-interfaces
interface=eth1
port=
# no-dhcp-interface=          # disable dhcp

dhcp-leasefile=/tmp/dnsmasq.leases
dhcp-range=192.168.0.101,192.168.0.150[,255.255.255.0],12h  # ip range, [netmask], release time
dhcp-host=aa:bb:cc:dd:ee:ff,192.168.111.50 # fixed ip

dhcp-option=1,255.255.255.0      # subnet mask
dhcp-option=28,192.168.0.255     # broadcast
dhcp-option=3,192.168.0.250      # default gateway
dhcp-option=6,192.168.0.251      # dns
...

#  TFTP
dhcp-boot=pxelinux.0,192.168.0.1 # tftp server ip
enable-tftp
tftp-root=/tfp
...

# DNS
# no-hosts                       # not read /etc/hosts
# addn-hosts=/etc/banner_add_hosts
address=/node11.com/192.168.0.11
...

server:~ # service dnsmasq start
```

---

## dns

```bash
server:~ # cat /etc/hosts
```

---

## pxe

```bash
server:~ # apt-get install syslinux
server:~ # cp /media/ubuntu14.04_tls/install/netboot/ubuntu-installer/amd64/{linux,initrd.gz,pxelinux.0} /tfp
server:~ # cp /usr/lib/syslinux/{pxelinux.0,menu.c32,vesamenu.c32} /tftp
server:~ # cat /tftp/pxelinux.cfg/default
DEFAULT vesamenu.c32

LABEL Ubuntu
  kerenl linux
  append initrd=initrd.gz netboot=nfs splash=silent showopts ramdisk_size=65536 install=nfs://192.168.0.1/ubuntu14
```

---

## nfs

```bash
server:~ # apt-get install nfs-kernel-server
server:~ # cat /etc/exports
/ubuntu14   192.168.0.0/24(ro)

server:~ # cp -r /media/ubuntu14.04_tls/* /ubuntu14
server:~ # service nfs-kernel-server restart
```

---

## personal repositpory

```bash
server:~ # apt-get install dpkg-dev
server:~ # mkdir -p /usr/local/mydebs

server:~ # cd /usr/local/mydebs
server:~ # dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
```
