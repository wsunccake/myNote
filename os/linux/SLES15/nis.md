# NIS


## Server

`package`

```bash
ypserv:~ # zypper in ypserv
```

`config`

```bash
ypserv:~ # vi /etc/ypserv.conf

ypserv:~ # vi /var/yp/securenets

ypserv:~ # vi /var/yp/Makefile

ypserv:~ # cd /var/yp; make

ypserv:~ # nisdomainname <nisdomainname>
```

`daemon`

```bash
ypserv:~ # systemctl start ypserv
ypserv:~ # systemctl enable ypserv
```

---

## Client

`package`

```bash
yp:~ # zypper in ypbind
```

`config`

```bash
yp:~ # vi /etc/yp.conf
ypserver <ypserv_ip>
domain <nisdomainname> [broadcast]

yp:~ # vi /etc/passwd
...
+:::::::

yp:~ # vi /etc/group
...
+:::

yp:~ # vi /etc/shadow
...
+

yp:~ # vi /etc/nsswitch.conf
...
passwd: compat
group:  compat
shadow: compat
...

yp:~ # nisdomainname <nisdomainname>
```

`daemon`

```bash
yp:~ # systemctl start ypbind
yp:~ # systemctl enable ypbind
```

`test`

```bash
yp:~ # getent passwd
```
