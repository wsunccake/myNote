# dnsmasq

## install

```bash
sle:~ # zypper in dnsmasq
sle:~ # vi /etc/dnsmasq.conf
...
conf-dir=/etc/dnsmasq.d/,*.conf

sle:~ # ls /etc/dnsmasq.d
sle:~ # dnsmasq --test

sle:~ # systemctl enable dnsmasq
sle:~ # systemctl start dnsmasq
```

---

## dhcp

```bash
sle:~ # vi /etc/dnsmasq.d/dhcp.conf
# port=0                                    # 0: disable dhcp
listen-address=127.0.0.1,192.168.0.1        # multi ip
bind-interfaces
interface=eth1                              # multi nic
dhcp-leasefile=/var/lib/misc/dnsmasq.leases
dhcp-range=192.168.0.200,192.168.0.230,12h  # dymanic ip
dhcp-host=11:22:33:aa:bb:cc,192.168.0.201   # static ip
dhcp-option=1,255.255.255.0                 # subnet mask
dhcp-option=28,192.168.0.255                # broadcast
dhcp-option=3,192.168.0.250                 # default gateway
dhcp-option=6,192.168.0.251                 # dns

sle:~ # firewall-cmd --add-service=dhcp --permanent
sle:~ # firewall-cmd --add-service=dhcp

sle:~ # ss -lutnp | grep 67
```

---

## dns

```bash
sle:~ #  vi /etc/dnsmasq.d/dns.conf
# no-hosts                          # disable /etc/hosts
# addn-hosts=

no-resolv                           # disable /etc/resolv.conf
# resolv-file

sle:~ # firewall-cmd --add-service=dns --permanent
sle:~ # firewall-cmd --add-service=dns

sle:~ # ss -lutnp | grep 53
```

---

## tftp

```bash
sle:~ #  vi /etc/dnsmasq.d/tftp.conf
enable-tftp
tftp-root=/srv/tftpboot

sle:~ # firewall-cmd --add-service=tftp --permanent
sle:~ # firewall-cmd --add-service=tftp

sle:~ # ss -lutnp | grep 69
```
