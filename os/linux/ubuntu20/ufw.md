# ufw

```bash
# service
[ubuntu:~ ] # systemctl status         ufw
[ubuntu:~ ] # systemctl enable|disable ufw
[ubuntu:~ ] # systemctl  start|stop    ufw

# status
[ubuntu:~ ] # ufw status
[ubuntu:~ ] # ufw enable
[ubuntu:~ ] # ufw disable
[ubuntu:~ ] # ufw show raw
[ubuntu:~ ] # ufw default allow|deny|reject

# rule
[ubuntu:~ ] # ufw allow 53
[ubuntu:~ ] # ufw allow 53/tcp
[ubuntu:~ ] # ufw allow 53/udp
[ubuntu:~ ] # ufw deny 80/tcp
[ubuntu:~ ] # ufw delete deny 80/tcp

# service
[ubuntu:~ ] # cat /etc/services
[ubuntu:~ ] # ufw allow ssh
[ubuntu:~ ] # ufw deny ssh

# ip
[ubuntu:~ ] # ufw allow from 207.46.232.182
[ubuntu:~ ] # ufw allow from 192.168.1.0/24
[ubuntu:~ ] # ufw deny from 192.168.0.1 to any port 22

# app
[ubuntu:~ ] # ufw app list
[ubuntu:~ ] # ufw allow OpenSSH
[ubuntu:~ ] # ls /etc/ufw/applications

# logging
[ubuntu:~ ] # ufw logging on
[ubuntu:~ ] # ufw logging off
```
