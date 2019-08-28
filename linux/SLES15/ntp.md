# date

## command

```bash
sle:~ # date
sle:~ # date "+%Y%m%d"
sle:~ # date "+T"
sle:~ # date -s "YYYY/mm/dd HH:MM:SS"

sle:~ # hwclock -s
sle:~ # hwclock -w
```


---

# timedatectl

```bash
sle:~ # timedatectl status
sle:~ # timedatectl list-timezones
sle:~ # timedatectl set-timezone UTC
sle:~ # timedatectl set-time "YYYY/mm/dd HH:MM:SS"
sle:~ # timedatectl set-local-rtc no
sle:~ # timedatectl set-local-rtc yes
sle:~ # timedatectl set-ntp no
sle:~ # timedatectl set-ntp yes
```


---

# ntp


## Server

`package`

```bash
server:~ # zypper install ntp
```


`config`

```bash
server:~ # vi /etc/ntp.conf
...
server tw.pool.ntp.org

...
restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery
restrict 127.0.0.1
restrict ::1
restrict 192.168.0.0 mask 255.255.255.0 nomodify
...
```


`service`

```bash
server:~ # systemctl enable ntpd
server:~ # systemctl start ntpd
```


---

## Client

`package`

```bash
client:~ # zypper install ntp
```

`config`

```bash
client:~ # vi /etc/ntp.conf
...
server <ntp_server>
...
```


`service`

```bash
client:~ # systemctl enable ntpd
client:~ # systemctl start ntpd
```


`usage`

```bash
client:~ # ntpq -p
client:~ # ntpdate -uv <ntp_server>
```


---

# chrony


## Server

`package`

```bash
server:~ # zypper install chrony
```


`config`

```bash
server:~ # vi /etc/chrony.conf
...
server tw.pool.ntp.org
...

allow 192.168.0/24
deny  192.168.0.254
```


`service`

```bash
server:~ # systemctl enable chronyd
server:~ # systemctl start chronyd
```



## Client

`package`

```bash
client:~ # zypper install ntp
```

`config`

```bash
client:~ # vi /etc/chrony.conf
...
server <ntp_server>
...
```


`service`

```bash
client:~ # systemctl enable chronyd
client:~ # systemctl start chronyd
```


`usage`

```bash
client:~ # chronyc sources
client:~ # chronyc burst 4/4

client:~ # chronyc makestep
```
