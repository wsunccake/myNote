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

## systemd-resolved

```bash
sle:~ # systemd-resolve --status
sle:~ # systemd-resolve --interface <nic> --set-dns <dns_ip> --set-domain <domain name>

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

# command
sle:~ # resolvectl status
sle:~ # resolvectl query <host>|<ip>
sle:~ # resolvectl statistics
sle:~ # resolvectl flush-caches
```

---

## systemd-logind

```bash
sle:~ # cat /usr/lib/systemd/system/systemd-logind.service
sle:~ # systemd edit systemd-logind.service
sle:~ # systemd edit --full systemd-logind.service  # /etc/systemd/system/systemd-logind.service
...
[Service]
Environment=SYSTEMD_LOG_LEVEL=debug

sle:~ # vimdiff /etc/systemd/system/systemd-logind.service /usr/lib/systemd/system/systemd-logind.service

# service
sle:~ # systemctl daemon-reload
sle:~ # systemctl restart systemd-logind

# command
sle:~ # loginctl list-users
sle:~ # user-status <user>
sle:~ # show-user <user>

sle:~ # loginctl list-sessions
sle:~ # loginctl session-status <session id>
sle:~ # loginctl show-session <session id>

sle:~ # loginctl list-seats
sle:~ # loginctl seat-status <seat>
sle:~ # loginctl show-seat <seat>
```
