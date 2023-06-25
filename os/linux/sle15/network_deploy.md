# network deploy

## apache2

```bash
# package
server:~ # zypper in apache2

# config
server:~ # cat << EOF >> /etc/apache2/conf.d/repo.conf
Alias /repo "/mnt"

<Directory /mnt>
  Require all granted
  Options +Indexes
</Directory>
EOF

# service
server:~ # systemctl start apache2
server:~ # systemctl enable apache2

# test
server:~ # curl -L http://localhost/repo
```

---

## dnsmasq

```bash
# package
server:~ # zypper in dnsmasq

# config
server:~ # grep -Ev '^#|^$' /etc/dnsmasq.conf
local-service
conf-dir=/etc/dnsmasq.d/,*.conf

server:~ # cat << EOF >> /etc/dnsmasq.d/dhcp.conf
interface=eth1
bind-interfaces
dhcp-range=192.168.10.100,192.168.10.150,12h
dhcp-option=1,255.255.255.0
dhcp-boot=pxelinux.0,192.168.10.10
EOF

server:~ # cat << EOF >> /etc/dnsmasq.d/pxe.conf
enable-tftp
tftp-root=/srv/tftpboot
EOF

# service
server:~ # systemctl start dnsmasq
server:~ # systemctl enable dnsmasq
```

---

## autoyast

```bash
# package
server:~ # zypper in autoyast2

# create autoinst.xml
server:~ # yast clone_system
server:~ # yast autoyast

server:~ # mkdir -p /srv/tftpboot/sle15/
server:~ # cp autoinst.xml /srv/tftpboot/sle15/.
server:~ # chmod +r /srv/tftpboot/sle15/autoinst.xml
```

---

## pxe

```bash
# mount SLE-15-SP4-Full-x86_64-GM-Media1.iso
server:~ # mount /dev/sr0 /mnt
server:~ # cp /mnt/boot/x86_64/loader/linux /srv/tftpboot/sle15/.
server:~ # cp /mnt/boot/x86_64/root /srv/tftpboot/sle15/.

# package
server:~ # zypper in syslinux
server:~ # cp /usr/share/syslinux/{pxelinux.0,vesamenu.c32,menu.c32} /srv/tftpboot/.

# config
server:~ # mkdir -p /srv/tftpboot/pxelinux.cfg
server:~ # cat << EOF >> /srv/tftpboot/pxelinux.cfg/default
default linux

# install
label linux
  ipappend 2
  kernel sle15/linux
  append initrd=sle15/initrd instsys=tftp://192.168.10.10/sle15/root install=http://192.168.10.10/repo autoyast=tftp://192.168.10.10/sle15/autoinst.xml

display  message
implicit 1
prompt  1
timeout  50
EOF
```
