# KERNEL CRASH DUMP GUIDE

## Record Kernel Core Dump

### install

```bash
linux:~ # yum install kexec-tools
linux:~ # systemctl start kdump.service
linux:~ # systemctl enable kdump.service
```

### config

```bash
linux:~ # vi /etc/kdump.conf
```

### test

```bash
linux:~ # echo 1 > /proc/sys/kernel/sysrq
linux:~ # echo c > /proc/sysrq-trigger
```


---

## Analyzing

### install

```bash
linux:~ # yum install crash
linux:~ # yum install kernel kernel-debug kernel-debuginfo kernel-debuginfo-common
```

### command

```bash
crash /usr/lib/debug/lib/modules/<kernel>/vmlinux \ /var/crash/<timestamp>/vmcore
crash> sys
crash> log
crash> bt
crash> ps
crash> vm
crash> files
```

### ex

```bash
crash> sys
crash> log
crash> dis -l <addr>
```

