# chrony

## service

```bash
sle:~ # systemctl enable chronyd
sle:~ # systemctl start chronyd
```


## config

```bash
sle:~ # vi /etc/chrony.conf
sle:~ # ls /etc/chrony.d
```


## command

```bash
sle:~ # chronyc sources         # list ntp source
sle:~ # chronyc sources -v
sle:~ # chronyc sourcestats
sle:~ # chronyc tracking
sle:~ # chronyc activity

sle:~ # chronyc -a makestep
sle:~ # chronyc -a 'burst 4/4'       # sync time
```
