# systemd-logind

## service

```bash
sle:~ # cat /usr/lib/systemd/system/systemd-logind.service
sle:~ # systemd edit systemd-logind.service
sle:~ # systemd edit --full systemd-logind.service  # /etc/systemd/system/systemd-logind.service
...
[Service]
Environment=SYSTEMD_LOG_LEVEL=debug

sle:~ # vimdiff /etc/systemd/system/systemd-logind.service /usr/lib/systemd/system/systemd-logind.service

sle:~ # systemctl daemon-reload
sle:~ # systemctl restart systemd-logind
```

---

## loginctl

```bash
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


---

## other

### disale power key

```bash
sle:~ # udevadm trigger -v -n -g power-switch
sle:~ # udevadm trigger -v -n -g power-switch | xargs -i cat {}/../name

sle:~ # systemd-inhibit --list --mode=block
sle:~ # systemd-inhibit --list --mode=delay

sle:~ # vi /etc/systemd/logind.conf
HandlePowerKey=ignore
```
