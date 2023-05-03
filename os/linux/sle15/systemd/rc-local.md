# rc-local

```bash
sle:~ # cat /usr/lib/systemd/system/rc-local.service
sle:~ # echo "date" >> /etc/init.d/boot.local
sle:~ # chmod +x /etc/init.d/boot.local

sle:~ # systemctl enable rc-local --runtime
sle:~ # systemctl status rc-local
sle:~ # systemctl is-enabled rc-local
```
