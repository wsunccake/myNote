# mrsh

## port

- mrshd: 21212/tcp
- mrlogind: 541/tcp

```bash
# firewall
sle:~ # firewall-cmd --add-port=21212/tcp --add-port=541/tcp --permanent
sle:~ # firewall-cmd --reload
```

---

## require

- setup [munge](./munge.md)
- setup [chrony](./chrony.md)

---

## server

```bash
server:~ # zypper in mrsh-server

# secure tty
server:~ # echo "mrsh" >> /etc/securetty
server:~ # echo "mrlogin" >> /etc/securetty

# service
server:~ # systemctl enable mrshd.socket mrlogind.socket
server:~ # systemctl start mrshd.socket mrlogind.socket
server:~ # systemctl status mrshd.socket mrlogind.socket

# log
server:~ # journalctl -u mrsh.socket -u mrlogind.socket -f
server:~ # journalctl -f

# firewall
server:~ # firewall-cmd --permanent --add-port=21212/tcp
server:~ # firewall-cmd --reload

# test
server:~ # mrsh localhost uptime
server:~ # mrlogin localhost

# port
server:~ # ss -lutnp | grep 21212       # mrsh
server:~ # ss -lutnp | 541              # mrlogin
```

---

## client

```bash
client:~ # zypper in mrsh

# firewall
client:~ # firewall-cmd --zone=trusted --add-source=<CIDR>|<IP> --permanent     # server ip or cidr
client:~ # firewall-cmd --reload

# item                                      ie
# CIDR / Classless Inter-Domain Routing:    192.168.33.0/24
# Network Address:                          192.168.33.0
# Subnet Mask:                              /24

# test
client:~ # mrsh server uptime
client:~ # mrlogin server
```
