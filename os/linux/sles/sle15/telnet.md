# telnet

## port

- telnet : 23/tcp

---

## server

`package`

```bash
server:~ # zypper in telnet-server
```

`daemon`

```bash
server:~ # systemctl enable telnet
server:~ # systemctl start telnet
server:~ # systemctl status telnet
```

`firewall`

```bash
server:~ # firewall-cmd --permanent --add-service=telnet
server:~ # firewall-cmd --reload
```

---

## client

`package`

```bash
client:~ # zypper in telnet
```

`usage`

```bash
client:~ $ telnet <server>
```
