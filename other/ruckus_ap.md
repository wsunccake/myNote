# Ruckus AP

## vAP on KVM

- Processor: 1+

- Memory: 1+ GB

- NIC: 1, virtio

- Disk: 1GB+, virtio

## list info

```bash
rkscli: get version
rkscli: get ipaddr wan
rkscli: get wlanlist

rkscli: get scg
rkscli: get tunnelmgr

rkscli: fw show all
```

---

## reboot & set factory

```bash
rkscli: reboot
rkscli: set factory
```

---

## set scg

```bash
rkscli: set scg ip <scg_control_ip>
rkscli: set scg config interval 30
rkscli: set scg status interval 30
rkscli: set scg getconf
```

---

## update fw

```bash
# by scg http
rkscli: fw set proto http
rkscli: fw set port 91
rkscli: fw set host <scg_control_ip>
rkscli: fw set control wsg/firmware/R300_3.4.0.0.139.rcks
rkscli: fw update

# by scg https
rkscli: fw set proto https
rkscli: fw set port 11443
rkscli: fw set host <scg_control_ip>
rkscli: fw set control wsg/firmware/R710_3.2.0.99.477.rcks
rkscli: fw update

# by tftp
rkscli: fw set proto tftp
rkscli: fw set port 69
rkscli: fw set host <tftp_ip>
rkscli: fw set control R710/rcks_fw.bl7
rkscli: fw update
```

---

## log

```bash
rkscli: set scg console 0xffff

# logread -f
```

---

## rfald

```bash
rkscli: set rfald disable
rkscli: set rfald peer <ue_ip>
rkscli: set rfald enable
rkscli: get rfald
```

---

## version

```bash
rkscli: get version

# cat /etc/version
```

## shell

```bash
rkscli: !v54!
rkscli: ruckus
```
