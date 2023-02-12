# apparmor

## service

```bash
sle:~ # systemctl status apparmor
```

---

## profile

```bash
sle:~ # apparmor_status
sle:~ # ls /etc/apparmor.d
sle:~ # aa-status

# enforce/complain
sle:~ # aa-complain /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # aa-enforce /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # ps auxZ

# enable/disable
sle:~ # aa-disable /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # ls -l /etc/apparmor.d/disable/*
sle:~ # aa-enabled /etc/apparmor.d/usr.sbin.dnsmasq
sle:~ # ls -l /etc/apparmor.d/disable/*
```
