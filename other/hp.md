# switch

## Basic

baud rate: 38400

ctrl^h: delete

?: completion

default password: 512900

### enable privilege

```bash
<HP> _cmdline-mode on
<HP> system-view
[HP]
```

### common

```bash
<HP> quit
```

### list

```bash
[HP] summary
[HP] display logbuffer [reverse] | incliude DOWN   # 顯示 log
[HP] display current-configuration
```

### setup IP

```bash
# for DHCP / dynamic IP
[HP] ipsetup dhcp
[HP] ipsetup ipv6 auto

# for static IP
[HP] ipsetup ip-address <ip> <netmask> default-gateway <gw>
[HP] ipsetup ipv6 address <ip> <netmask> default-gateway <gw>

# test
[HP] ping <ip>
[HP] ping ipv6 <ip>
```

### interface config

```bash
[HP] display interface [brief]   # 顯示 interface

[HP] interface <interface>       # 進入 interface 設定
[HP-<interface>] undo shutdown   # 開啟 interface
[HP-<interface>] shutdown        # 關閉 interface
```
