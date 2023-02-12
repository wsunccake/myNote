# APC UPSD

## install

```bash
ubuntu:~ # apt-get install apcupsd
```

---

## configure

```bash
ubuntu:~ # vi /etc/default/apcupsd
# replace
ISCONFIGURED=no
->
ISCONFIGURED=yes
...

ubuntu:~ # ls /dev/usb/hiddev*
ubuntu:~ # vi /etc/apcupsd/apcupsd.conf

# add
UPSCABLE usb
...
UPSTYPE usb
DEVICE /dev/usb/hiddev0
...
BATTERYLEVEL 5 # 電池低於 n % 關機
...
MINUTES -1 # 電池續航時間低於 n 分鐘關機
...
TIMEOUT 0 # 跳電後 n 秒關機
...

ubuntu:~ # service apcupsd start
ubuntu:~ # service apcupsd stop
ubuntu:~ # service apcupsd status
```

---

## status

```bash
ubuntu:~ # apcaccess [ <server_ip>:<port> ]
APC      : 001,035,0915
DATE     : 2017-11-18 20:24:51 +0800
HOSTNAME : u1
VERSION  : 3.14.10 (13 September 2011) debian
UPSNAME  : u1
CABLE    : USB Cable
DRIVER   : USB UPS Driver
UPSMODE  : Stand Alone
STARTTIME: 2017-11-18 17:44:20 +0800
MODEL    : Back-UPS ES 500
STATUS   : ONLINE
LINEV    : 110.0 Volts
LOADPCT  :   0.0 Percent Load Capacity
BCHARGE  : 100.0 Percent
TIMELEFT :  43.5 Minutes
MBATTCHG : 5 Percent
MINTIMEL : 3 Minutes
MAXTIME  : 0 Seconds
SENSE    : High
LOTRANS  : 088.0 Volts
HITRANS  : 133.0 Volts
ALARMDEL : 30 seconds
BATTV    : 13.3 Volts
LASTXFER : No transfers since turnon
NUMXFERS : 1
XONBATT  : 2017-11-18 17:44:23 +0800
TONBATT  : 0 seconds
CUMONBATT: 9 seconds
XOFFBATT : 2017-11-18 17:44:32 +0800
STATFLAG : 0x07000008 Status Flag
SERIALNO : 4B1250P23673
BATTDATE : 2012-12-14
NOMINV   : 120 Volts
NOMBATTV :  12.0 Volts
FIRMWARE : 801.e6.D USB FW:e6
END APC  : 2017-11-18 20:25:09 +0800
```

LINEV, LOADPCT, BCHARGE, TIMELEFT are in-time value

MBATTCHG, MINTIMEL, MAXTIME are config value

---

## test

```bash
ubuntu:~ # apcupsd --killpower
ubuntu:~ # apccontrol killpower
ubunut:~ # vi /etc/apcupsd/apccontrol
```

---

## log

```bash
ubuntu:~ # tail /var/log/apcupsd.events
```

---

## web

```bash
ubuntu:~ # apt-get install apcupsd-cgi
ubuntu:~ # apt-get install apache2
http://localhost/cgi-bin/apcupsd/multimon.cgi
```

---

## ref

[apcupsd.conf 設置備忘](http://jamyy.us.to/blog/2015/05/7457.html)

[Setup APC UPS on Ubuntu Workstation using apcupsd](http://www.pontikis.net/blog/apc-ups-on-ubuntu-workstation)
