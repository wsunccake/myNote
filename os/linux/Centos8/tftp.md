# tftp

## install

```bash
server:~ # dnf install epel-release
server:~ # dnf makecache
server:~ # dnf install tftp-server

server:~ # systemctl enable tftp
server:~ # systemctl start tftp
```

```bash
client:~ # dnf install tftp
```


---

## config

```bash
server:~ # cat /lib/systemd/system/tftp.service
```


---

## firewall

```bash
server:~ # firewall-cmd --add-service=tftp --permanent
server:~ # firewall-cmd --reload
```


---

## test

```bash
server:~ # cd /var/lig/tftpboot
server:~ # date > /var/lig/tftpboot/<file>
```

```bash

client:~ # tftp <tftp_ip>
tftp> get <file>
tftp> quit
```
