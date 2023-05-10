# systemd-service

## rc-local

```bash
sle:~ # cat /usr/lib/systemd/system/rc-local.service
sle:~ # echo "date" >> /etc/init.d/boot.local
sle:~ # chmod +x /etc/init.d/boot.local

sle:~ # systemctl enable rc-local --runtime
sle:~ # systemctl status rc-local
sle:~ # systemctl is-enabled rc-local
```

---

## analyze

```bash
sle:~ # systemd-analyze blame
sle:~ # systemd-analyze critical-chain [docker.service]
sle:~ # systemd-analyze plot > boot_analysis.svg
```

---

## resolve

```bash
sle:~ # systemd-resolve --status
sle:~ # resolcectl status
sle:~ # /run/systemd/resolve/resolv.conf
```
