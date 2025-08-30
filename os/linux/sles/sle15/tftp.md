# tftp

## port

- tftp: 69/udp

---

## server

`package`

```bash
server:~ # zypper in tftp
server:~ # zypper in yast2-tftp-server
```

`config`

- method 1 - by yast

```bash
server:~ # yast tftp-server
```

- method 2 - by manual

```bash
server:~ # vi /usr/lib/systemd/system/tftp.service
server:~ # vi /etc/sysconfig/tftp
```

```conf
# /etc/sysconfig/tftp
TFTP_USER="tftp"

TFTP_OPTIONS=""

TFTP_DIRECTORY="/srv/tftpboot"
```

`daemon`

```bash
server:~ # systemctl start tftp
server:~ # systemctl enable tftp
server:~ # systemctl status tftp
```

`firewall`

```bash
server:~ # firewall-cmd --permanent --add-service=tftp
server:~ # firewall-cmd --reload
```

`test`

```bash
server:~ # hostname > /srv/tftpboot/hostname
```

---

## client

`package`

```bash
client:~ # zypper in tftp
```

`firewall`

```bash
client:~ # firewall-cmd --permanent --add-service=tftp
client:~ # firewall-cmd --reload
```

`usage`

```bash
client:~ # tftp <server>

tftp> get hostname
```
