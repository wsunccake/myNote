# systemd-service

---

## content

- [analyze](#analyze)
- [timer](#timer)
- [rc-local](#rc-local)
- [systemd-tmpfiles](#systemd-tmpfiles)
- [systemd-resolved](#systemd-resolved)
- [systemd-logind](#systemd-logind)

---

## analyze

```bash
sle:~ # systemd-analyze blame
sle:~ # systemd-analyze critical-chain [docker.service]
sle:~ # systemd-analyze plot > boot_analysis.svg
```

---

## timer

```bash
sle:~ # systemctl list-timers --all

sle:~ # systemctl start <TIMER>.timer
sle:~ # systemctl restart <TIMER>.timer
sle:~ # systemctl stop <TIMER>.timer

sle:~ # systemctl enable <TIMER>.timer
sle:~ # systemctl disable <TIMER>.timer

sle:~ # systemctl cat <TIMER>.timer
sle:~ # systemctl status <TIMER>.timer
```

`example`

```bash
# /usr/local/bin/helloworld.sh
echo "hello world"
```

```bash
# /etc/systemd/system/helloworld.service
[Unit]
Description="Hello World script"

[Service]
ExecStart=/usr/local/bin/helloworld.sh
```

```bash
# /etc/systemd/system/helloworld.timer
[Unit]
Description="Run helloworld.service 5min after boot and every 24 hours relative to activation time"

[Timer]
OnBootSec=5min                      # monotonic timer
OnUnitActiveSec=24h                 # real-time timer
OnCalendar=Mon..Fri *-*-* 10:00:*   # real-time timer, DayOfWeek Year-Month-Day Hour:Minute:Second
Unit=helloworld.service

[Install]
WantedBy=multi-user.target
```

```bash
# service
sle:~ # systemd-analyze verify /etc/systemd/system/helloworld.*
sle:~ # systemctl start helloworld.timer
sle:~ # systemctl enable helloworld.timer

# log
sle:~ # journalctl -u  helloworld.timer -u helloworld.service
sle:~ # journalctl -u  helloworld.*

# transient timer
sle:~ # man 1 systemd-run
sle:~ # systemd-run --on-active="2hours" --unit="helloworld.service"
sle:~ # systemd-run --on-active="2hours" /usr/local/bin/helloworld.sh

#
sle:~ # systemd-analyze calendar "Tue,Sun *-*-* 01,03:00:00"
sle:~ # systemd-analyze calendar "Mon..Fri *-*-* 10:00" "Sat,Sun *-*-* 22:00"
sle:~ # systemd-analyze calendar --iterations 5 "Sun *-*-* 0/08:00:00"
```

---

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

## systemd-tmpfiles

```bash
# config
sle:~ # ls /etc/tmpfiles.d/*.conf
sle:~ # ls /usr/lib/tmpfiles.d/*.conf
sle:~ # ls /run/tmpfiles.d/*.conf

# man
sle:~ # man 5 tmpfiles.d

# command
sle:~ # systemd-tmpfiles --create|--clean|--remove

# service
sle:~ # systemctl status systemd-tmpfiles-setup
sle:~ # systemctl status systemd-tmpfiles-setup-dev
sle:~ # systemctl status systemd-tmpfiles-clean
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
