# ufw

## content

- [daemon](#daemon)
- [status](#status)
- [rule](#rule)
  - [default](#default)
  - [port and protocol](#port-and-protocol)
  - [service](#service)
  - [ip](#ip)
  - [app](#app)
- [logging](#logging)
- [limit](#limit)
- [config](#config)

## daemon

```bash
# service
[ubuntu:~ ] # systemctl status         ufw
[ubuntu:~ ] # systemctl enable|disable ufw
[ubuntu:~ ] # systemctl  start|stop    ufw
```

---

## status

```bash
# status
[ubuntu:~ ] # ufw status [numbered|verbose]
[ubuntu:~ ] # ufw enable|disable
[ubuntu:~ ] # ufw show raw
```

---

## rule

### default

```bash
[ubuntu:~ ] # ufw default allow|deny|reject
```

### port and protocol

```bash
# rule
[ubuntu:~ ] # ufw allow 53
[ubuntu:~ ] # ufw allow 53/tcp
[ubuntu:~ ] # ufw allow 53/udp
[ubuntu:~ ] # ufw deny 80/tcp
[ubuntu:~ ] # ufw delete deny 80/tcp
```

### service

```bash
[ubuntu:~ ] # cat /etc/services
[ubuntu:~ ] # ufw allow ssh
[ubuntu:~ ] # ufw deny ssh
```

### ip

```bash
[ubuntu:~ ] # ufw allow from 207.46.232.182
[ubuntu:~ ] # ufw allow from 192.168.1.0/24
[ubuntu:~ ] # ufw deny from 192.168.0.1 to any port 22
```

### app

```bash

[ubuntu:~ ] # ufw app list
[ubuntu:~ ] # ufw allow OpenSSH
[ubuntu:~ ] # ls /etc/ufw/applications
```

---

## logging

```bash
[ubuntu:~ ] # ufw logging on
[ubuntu:~ ] # ufw logging off
```

---

## limit

```bash
[ubuntu:~ ] # ufw limit ssh/tcp
[ubuntu:~ ] # ufw limit in on eth0 proto tcp from 192.168.11.0/24 port 22
```

---

## config

```bash
[ubuntu:~ ] # cat /etc/default/ufw
```
