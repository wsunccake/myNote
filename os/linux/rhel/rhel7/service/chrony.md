# Chrony

## Service

```bash
centos:~ # systemctl enable chronyd
centos:~ # systemctl start chronyd

# config
centos:~ # vi /etc/chrony.conf
...
server time.stdtime.gov.tw  iburst
server clock.stdtime.gov.tw iburst
server watch.stdtime.gov.tw iburst
server tick.stdtime.gov.tw  iburst
server tock.stdtime.gov.tw  iburst
pool   tw.pool.ntp.org      iburst maxsources 3
pool   centos.pool.ntp.org  iburst maxsources 4


allow 192.168.0/24
deny  192.168.0.254
```


---

## Command

```bash
centos:~ # chronyc sources         # list ntp source
centos:~ # chronyc sources -v
centos:~ # chronyc sourcestats
centos:~ # chronyc tracking
centos:~ # chronyc activity

centos:~ # chronyc -a makestep
centos:~ # chronyc -a 'burst 4/4'       # sync time
```


---

## Other

```bash
centos:~ # date "+%Y%m%d"
centos:~ # date +%T
centos:~ # date -s "2000-1-1 00:00:00"
centos:~ # date -s "2000-1-1"
centos:~ # date -s "00:00:00"

centos:~ # hwclock -w

centos:~ # timedatectl
centos:~ # timedatectl set-time "2000-1-1 00:00:00"
centos:~ # timedatectl set-time "2000-1-1"
centos:~ # timedatectl set-time "00:00:00"
```
