# iptables

## iptables-persistent

```bash
ubuntu:~ # apt install iptables-persistent
ubuntu:~ # ls /etc/iptables
ubuntu:~ # cat /etc/iptables/rules.v4
ubuntu:~ # cat /etc/iptables/rules.v6

# update current iptable rule to iptables-persistent
ubuntu:~ # dpkg-reconfigure iptables-persistent         # method 1
ubuntu:~ # iptables-save > /etc/iptables/rules.v4       # method 2
```
