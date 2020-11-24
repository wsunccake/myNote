# Munge


## Server

`package`

```bash
server:~ # zypper in munge
```

`secret key`

```bash
server:~ # echo "foo" > /etc/munge/munge.key
server:~ # echo -n "foo" | sha512sum | cut -d' ' -f1 >/etc/munge/munge.key
server:~ # dd if=/dev/random bs=1 count=1024 >/etc/munge/munge.key
server:~ # dd if=/dev/urandom bs=1 count=1024 >/etc/munge/munge.key
```

`daemon`

```bash
server:~ # systemctl start munge.servce
server:~ # systemctl enable munge.servce
```

`test`

```bash
server:~ # munge -n
server:~ # munge -n | unmunge
server:~ # munge -n | ssh <remote_ip> unmunge
```


---

## Client

`package`

```bash
client:~ # zypper in munge
```

`secret key`

```bash
server:~ # scp /etc/munge/munge.key root@<client>:/etc/munge/.
```

`daemon`

```bash
server:~ # systemctl start munge.servce
server:~ # systemctl enable munge.servce
```
