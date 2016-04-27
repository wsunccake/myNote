# CISCO Switch


## Basic

baud rate: 9600


### Enable Privilege

```
# privilege mode
SWITCH> enable
SWITCH#

# config mode
SWITCH# configure terminal
SWITCH(config)#
```

### Common

```
# 設定 hostname
SWITCH(config)# hostname <hostname>

# 設定游標
SWITCH(config) # line console 0
SWITCH(config-line) # logging synchronous

# 關閉 DNS 查詢, 避免輸入錯誤命令時, iOS 向 DNS 伺服器進行查詢
SWITCH(config)# no ip domain-lookup
```

### NVRAM & Flash

```
SWITCH# dir nvram:   # startup-config 存放位置
SWITCH# dir flash:   # config.text 存放位置
SWITCH# rename flash:config.text flash:config.text.old   # 移動檔案
SWITCH# delete flash:config.text                         # 刪除檔案
SWITCH# copy flash:config.text.old flash:config.text     # 複製檔案

SWTICH# copy running-config startup-config               # 複製當前設定到啟動設定
```


### Set Factory

1. 拔掉電源線，並長按 "mode" button, 然後開機

2.

```
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

```
# 設定 console login 帳號密碼
SWITCH(config) # username <account> password <password>  # 設定登入的帳號密碼 (明碼)
SWITCH(config) # username <account> secret   <password>  # 設定登入的帳號密碼 (暗碼)

# 設定 privilege mode 密碼
SWITCH(config) # enable password <password> # 設定 enable password(明碼)
SWITCH(config) # enable secret <password>   # 設定 enable password(暗碼)

# 設定 console login 密碼
SWITCH(config) # line console 0
SWITCH(config-line) # password <password>  # 設定login password

# 切換 console 登入方式
SWITCH(config-line) # login                # 啟用 console login 設定 (僅須密碼, 不用帳號)
SWITCH(config-line) # login local          # 啟用 console login 設定 (須帳號和密碼)
SWITCH(config-line) # no login             # 關閉 console login 設定 (無須帳號和密碼)

# 設定 telnet login 密碼
SWITCH(config) # line vty 0 4              # 設定 0 ~ 4 vty
SWITCH(config-line) # login                # 啟用 console login 設定 (僅須密碼, 不用帳號)

# 設定 ssh login 密碼
SWITCH(config) # hostname <hotname>
SWITCH(config) # ip domain-name <domain>
SWITCH(config) # crypto key generate rsa
SWITCH(config) # line vty 0 4
SWITCH(config-line) # login                # 啟用 login check
SWITCH(config-line) # login local          # 啟用 login check, 使用帳號密碼登入, 此時telnet, ssh 皆可登入
SWITCH(config-line) # transport input ssh  # 僅 ssh 登入
```


### Setup IP

```
SWITCH(config)# ip name-server <ip>            # 設定 DNS
SWTICH(config)#ip default-gateway <ip>         # 設定 default gateway
SWITCH(config)# interface Vlan 1

# static IP
SWITCH(config-if)# ip address <ip> <netmask>   # 設定 static ip


# DHCP / dynamic IP
SWITCH(config-if)# ip dhcp                     # 設定 dynamic ip

# 開啟 interface
SWITCH(config-if)# no shutdown                 # 當 interface 設定完後, 要重啟設定才會套用
```


### List ###

```
SWITCH# show users
SWITCH# show runnung-config
SWITCH# show startup-config

SWITCH# show ip interfaces brief  # 顯示所有 interface
SWITCH# show mac address-table    # 顯示所有 每個 port 上連線的 mac table

SWITCH# show interfaces summary
SWITCH# show interfaces status
SWITCH# show interfaces [<interface>]
SWITCH# show configuration
SWITCH# show spanning-tree interface <interface>

SWITCH# show loggin | include
```

----


## Interface

```
# 設定 interface (單個 port)
SWTICH(config)# interface FastEthernet 0/1
SWTICH(config-if)#

# 設定 interface (多個 port)
SWTICH(config)#interface range FastEthernet 0/1 - 9
SWTICH(config-if-range)#
```

----

## MAC table

<interface>: FastEthernet 0/1

<mac>: 1122.3344.5566

<vlan_id>: 1

當起用 port-security, switch 會針對不同的 MAC 連上 port 有所不同的動作

```
# 設定 static mac table
SWITCH(config)# mac-address-table static <mac> vlan <vlan_id> interface <interface>         # 設定 static mac table
SWITCH(config)# no mac-address-table static <mac> vlan <vlan_id> interface [<interface>]    # 移除 static mac table

# 設定 dynamic mac table
SWTICH# clear mac-address-table dynamic  #  清除 dynamic mac table

#
SWITCH# show mac-address-table

# 設定 port-security
SWTICH(config)#interface <interface>
SWTICH(config-if)# switchport mode access
SWTICH(config-if)# switchport port-security
SWTICH(config-if)# switchport port-security maximum 1
SWTICH(config-if)# switchport port-security mac-address sticky
SWTICH(config-if)# switchport port-security violation shutdown
```

## MTU

2950 只能設定在 1500

```
SWITCH(config)# system mtu 1500

SWITCH# show system mtu
```


## Port Monitor

```
SWITCH(config)# monitor session 1 source interface FastEthernet 0/1
SWITCH(config)# monitor session 1 destination interface FastEthernet 0/11

SWITCH(config)# no monitor session 1

SWITCH# show monitor
```

----


## VLAN

vlan 1 為預設的 native vlan (不帶任何 vlan tag)

```
# enable vlan for interface
SWITCH# configure terminal
SWITCH(config)# interface <interface>
SWITCH(config-if)# switchport access vlan <vlan_id>
SWITCH(config-if)# no shutdown

# disable vlan for interface
SWITCH# no switchport access vlan <vlan_id>
SWITCH# no shutdown

# check vlan for interface
SWITCH# show spanning-tree interface TenGigabitEthernet 1/1
```


## Clock


### NTP

```

```