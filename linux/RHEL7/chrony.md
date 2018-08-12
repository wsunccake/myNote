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


## Command

```bash
centos:~ # chronyc sources         # list ntp source
centos:~ # chronyc sourcestats
centos:~ # chronyc tracking
centos:~ # chronyc -a makestep     # sync time
```
