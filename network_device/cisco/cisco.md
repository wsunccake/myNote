# CISCO

## Basic

baud rate: 9600

### Enable Privilege

```bash
# privilege mode
CISCO> enable
CISCO#

# config mode
CISCO# configure terminal
CISCO(config)#
```

### Common

```bash
# 設定 hostname
CISCO(config)# hostname <hostname>

# 設定游標
CISCO(config) # line console 0
CISCO(config-line) # logging synchronous

# 關閉 DNS 查詢, 避免輸入錯誤命令時, iOS 向 DNS 伺服器進行查詢
CISCO(config)# no ip domain-lookup
```

### NVRAM & Flash

```bash
CISCO# dir nvram:   # startup-config 存放位置
CISCO# dir flash:   # config.text 存放位置
CISCO# rename flash:config.text flash:config.text.old   # 移動檔案
CISCO# delete flash:config.text                         # 刪除檔案
CISCO# copy flash:config.text.old flash:config.text     # 複製檔案
```

### Set Factory

1. 拔掉電源線，並長按 "mode" button, 然後開機

2.

```bash
The system has been interrupted prior to initializing the
flash filesystem.  The following commands will initialize
the flash filesystem, and finish loading the operating
system software:

    flash_init
    load_helper
    boot

switch: flash_init
switch: dir flash:
switch: rename flash:config.text flash:config.text.old # 備份設定檔, 不備份不需要此步驟
switch: delete flash:config.text                       # 移除設定檔, 系統開啟時會成出廠設定
switch: boot                                           # 重開機
```

### Setup Login

```bash
# 設定 console login 帳號密碼
CISCO(config) # username <account> password <password>  # 設定登入的帳號密碼 (明碼)
CISCO(config) # username <account> secret   <password>  # 設定登入的帳號密碼 (暗碼)

# 設定 privilege mode 密碼
CISCO(config) # enable password <password> # 設定 enable password(明碼)
CISCO(config) # enable secret <password>   # 設定 enable password(暗碼)

# 設定 console login 密碼
CISCO(config) # line console 0
CISCO(config-line) # password <password>  # 設定login password

# 切換 console 登入方式
CISCO(config-line) # login                # 啟用 console login 設定 (僅須密碼, 不用帳號)
CISCO(config-line) # login local          # 啟用 console login 設定 (須帳號和密碼)
CISCO(config-line) # no login             # 關閉 console login 設定 (無須帳號和密碼)

# 設定 telnet login 密碼
CISCO(config) # line vty 0 4              # 設定 0 ~ 4 vty
CISCO(config-line) # login                # 啟用 console login 設定 (僅須密碼, 不用帳號)

# 設定 ssh login 密碼
CISCO(config) # hostname <hotname>
CISCO(config) # ip domain-name <domain>
CISCO(config) # crypto key generate rsa
CISCO(config) # line vty 0 4
CISCO(config-line) # login                # 啟用 login check
CISCO(config-line) # login local          # 啟用 login check, 使用帳號密碼登入, 此時telnet, ssh 皆可登入
CISCO(config-line) # transport input ssh  # 僅 ssh 登入
```

### Setup IP

```bash
# for router
CISCO(config) # interface FastEthernet 0/1
CISCO(config-if)# ip address <ip> <netmask> # static IP
CISCO(config-if)# ip dhcp                   # DHCP / dynamic IP
CISCO(config-if)# no shutdown               # 開啟 interface

# for switch
CISCO(config)# interface Vlan 1
CISCO(config-if)# ip address <ip> <netmask> # static IP
CISCO(config-if)# ip address dhcp           # DHCP / dynamic IP
CISCO(config-if)# no shutdown               # 開啟 interface
```

### List

```bash
CISCO# show users
CISCO# show runnung-config
CISCO# show startup-config

CISCO# show ip interfaces brief  # 顯示所有 interface
CISCO# show mac address-table    # 顯示所有 每個 port 上連線的 mac address

CISCO# show interfaces summary
CISCO# show interfaces status
CISCO# show interfaces
CISCO# show configuration
CISCO# show spanning-tree interface TenGigabitEthernet 1/1

CISCO# show loggin | include
```

---

## Switch

### MAC table

```bash
SWITCH#
SWITCH(config)# mac-address-table static 1122.3344.5566 vlan 1 interface FastEthernet 0/1
SWITCH(config)# no mac-address-table static 1122.3344.5566 vlan 1 interface [FastEthernet 0/1]

SWITCH#show mac-address-table
```

### MTU

2950 只能設定在 1500

```
CISCO(config)# system mtu 1500

CISCO# show system mtu
```

### Port Monitor

```bash
CISCO(config)# monitor session 1 source interface FastEthernet 0/1
CISCO(config)# monitor session 1 destination interface FastEthernet 0/11

CISCO(config)# no monitor session 1

CISCO# show monitor
```

---

## VLAN

vlan 1 為預設的 native vlan (不帶任何 vlan tag)

```bash
# enable vlan for interface
CISCO# configure terminal
CISCO(config)# interface <interface>
CISCO(config-if)# switchport access vlan <vlan_id>
CISCO(config-if)# no shutdown

# disable vlan for interface
CISCO# no switchport access vlan <vlan_id>
CISCO# no shutdown

# check vlan for interface
CISCO# show spanning-tree interface TenGigabitEthernet 1/1
```
