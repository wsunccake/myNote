# firewalld

---

## service

```bash
fedora:~ # systemctl start firewalld
fedora:~ # systemctl stop firewalld
fedora:~ # systemctl status firewalld
```

---

## config

```bash
fedora:~ # firewall-cmd --reload
```

### zone

```bash
fedora:~ # firewall-cmd --list-all [--zone=public]
fedora:~ # firewall-cmd --get-default-zone
fedora:~ # firewall-cmd --get-active-zones
fedora:~ # firewall-cmd --get-zones
fedora:~ # firewall-cmd --set-default-zone=home  # 更改 default zone
```

### service

```bash
fedora:~ # firewall-cmd --list-services
fedora:~ # firewall-cmd [--permanent] --add-service=http,https
fedora:~ # firewall-cmd [--permanent] --remove-service=http
```

### port

```bash
fedora:~ # firewall-cmd --list-ports
fedora:~ # firewall-cmd [--permanent] --add-port=8000/tcp
fedora:~ # firewall-cmd [--permanent] --remove-port=8000/tcp
```
