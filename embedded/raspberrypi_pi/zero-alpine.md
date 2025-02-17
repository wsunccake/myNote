# zero - alpine 3.21

## content

- [setup](#setup)
  - [system](#system)
  - [wireless network](#wireless-network)
  - [ntp](#ntp)
- [basic](#basic)
  - [common](#common)
  - [diskless](#diskless)
  - [service](#service)
  - [package manager](#package-manager)

---

## setup

### system

```bash
# setup system
alpine:~ # setup-alpine
...
```

### wireless network

```bash
# setup network
alpine:~ # setup-interfaces

# command to setup wlan
alpine:~ # wpa_passphrase <ssid> [<passphrase>] > /etc/wpa_supplicant/wpa_supplicant.conf
alpine:~ # wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
alpine:~ # udhcpc wlan0
```

### ntp

```bash
# setup ntp
alpine:~ # setup-ntp

# service
alpine:~ # rc-service chronyd status

# chrony config
alpine:~ # cat /etc/chrony/chrony.conf

# chrony command
alpine:~ # chronyc sources
alpine:~ # chronyc sourcestats
alpine:~ # chronyc tracking
alpine:~ # chronyc makestep
```

---

## basic

### common

```bash
alpine:~ # reboot
alpine:~ # poweroff

alpine:~ # lbu commit -d
```

### diskless

```bash
alpine:~ # df -h
# if / is tmpfs, system is diskless
```

```bash
alpine:~ # cat /etc/lbu/lbu.conf
...
LBU_MEDIA=mmcblk0p1
...

# default backup file
alpine:~ # ls /media/mmcblk0p1/$(hostname).apkovl.tar.gz

alpine:~ # lbu list             # 顯示改變檔案
alpine:~ # lbu include <path>   # 添加文件到備份
alpine:~ # lbu exclude <path>   # 從備份移除文件
alpine:~ # lbu commit           # 保存系統當前的變更
```

### service

```bash
alpine:~ # rc-service --list
alpine:~ # rc-service <service> stop
alpine:~ # rc-service <service> status
alpine:~ # rc-service <service> start
alpine:~ # rc-update add <service>
alpine:~ # rc-update del <service>
```

### package manager

```bash
alpine:~ # apk search <package>
alpine:~ # apk info [[-L] <package>]

alpine:~ # apk add <package>
alpine:~ # apk del <package>

alpine:~ # apk cache clean
alpine:~ # apk update
alpine:~ # apk upgrade
```

---
