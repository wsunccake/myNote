# iptables

## package

```bash
rhel:~ # yum install iptables
```

---

## configuration

```bash
rhel:~ # ls /usr/lib/systemd/system/iptables.service

rhel:~ # cat /etc/sysconfig/iptables
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
COMMIT

*nat
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -j MASQUERADE
COMMIT
```

---

## serivce

```bash
rhel:~ # systemctl start iptables.service
rhel:~ # systemctl enable iptables.service
rhel:~ # systemctl status iptables.service

rhel:~ # iptables -S        # print all rule
rhel:~ # iptables -L -nv    # list all rule
```

---

## advance

```bash
# ssh ddos
rhel:~ # iptables -I INPUT -p tcp --dport 22 -m connlimit --connlimit-above 3 -j DROP
rhel:~ # iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH
rhel:~ # iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds  300 --hitcount 3 --name SSH -j DROP

# drop
rhel:~ # iptables -I OUTPUT -p udp --dport 53 -m string --string example.com -j DROP

# limit
rhel:~ # iptables -A INPUT -p icmp –icmp-type 8 -m limit --limit 6/m --limit-burst 10 -j ACCEPT
rhel:~ # iptables -A INPUT -p icmp –icmp-type 8 -j DROP
```
