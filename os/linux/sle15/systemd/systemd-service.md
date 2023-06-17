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
# comamnd
sle:~ # systemd-resolve --status
sle:~ # systemd-resolve --interface <nic> --set-dns <dns_ip> --set-domain <domain name>
sle:~ # resolcectl status

# config
sle:~ # ls -l /etc/resolv.conf # -> /run/systemd/resolve/stub-resolv.conf
sle:~ # cat /run/systemd/resolve/resolv.conf

sle:~ # cat /etc/systemd/resolved.conf
[Resolve]
#DNS=

# service
sle:~ # systemctl status systemd-resolved
sle:~ # systemctl restart systemd-resolved

# log
sle:~ # journalctl -u systemd-resolved -f
```
