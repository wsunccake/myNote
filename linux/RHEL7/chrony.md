# Chrony

## Service

```bash
centos:~ # systemctl enable chronyd
centos:~ # systemctl start chronyd

# config
centos:~ # vi /etc/chrony.conf
```


## Command

```bash
centos:~ # chronyc sources
centos:~ # chronyc sourcestats
centos:~ # chronyc tracking
centos:~ # chronyc -a makestep
```
