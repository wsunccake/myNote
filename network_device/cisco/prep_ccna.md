# prep ccna

## switch - basic

### enable privilege

```bash
# privilege mode
Switch> enable
Switch#

# config mode
Switch# configure terminal
Switch(config)#

Switch(config)# end
Switch#
```

### show config

```bash
Switch# show users
Switch# show runnung-config
Switch# show startup-config

Switch# show ip interfaces brief  # 顯示所有 interface
Switch# show mac address-table    # 顯示所有 每個 port 上連線的 mac table
Switch# show interfaces status
```

### privilege mode password

```bash
Switch(config)# enable password <password> # setup privilege password (明碼)
Switch(config)# enable secret   <password> # setup privilege password (暗碼)
```

### account

```bash
Switch(config)# username <account> password <password>  # 設定登入的帳號密碼 (明碼)
Switch(config)# username <account> secret   <password>  # 設定登入的帳號密碼 (暗碼)
```

---

## conf

RAM: working memory & running configuration

Flash: IOS

ROM: booststrap

NVRAM: startup configuration

```bash
Switch# copy running-config startup-config  # copy running-config to startup-config
Switch# erase startup-config                # erase startup-config
Switch# reload                              # reboot

Switch# show running-config
Switch# show startup-config
```

---

## switch - login

### console

```bash
Switch(config)# line console 0             # setup console 0
Switch(config-line)# password <password>   # setup password

Switch(config-line)# login                 # enable console login (only password)
Switch(config-line)# login local           # enable console login (需密碼帳號)
Switch(config-line)# no login              # diable console login (no password)
```

### telnet

```bash
Switch(config)# line vty 0 4              # setup 0 ~ 4 vty
Switch(config-line)# password <password>  # setup password
Switch(config-line)# login                # only enable telnet login (only password)

Switch(config-line)# no password          # remove login password
```

### ssh

```bash
# prepare to gen ssh key
Switch(config)# hostname <hotname>
Switch(config)# ip domain-name <domain>
Switch(config)# crypto key generate rsa

Switch(config)# line vty 0 4
Switch(config-line)# login
Switch(config-line)# password <password>
Switch(config-line)# login local          # both enable telnet and ssh login
Switch(config-line)# transport input ssh  # only enable ssh login
```

### password encryption

```bash
Switch(config)# service password-encryption
Switch(config)# no service password-encryption
```

---

## switch - common

### ip

```bash
Switch(config)# ip name-server <ip>      # setup DNS
Switch(config)# ip default-gateway <ip>  # setup default gateway
Switch(config)# interface Vlan 1         # svi / switch virtual interface

# static IP
Switch(config-if)# ip address <ip> <netmask>   # setup static ip

# DHCP / dynamic IP
Switch(config-if)# ip dhcp                     # setup dynamic ip

# interface
Switch(config-if)# no shutdown                 # 當 interface 設定完後, 要重啟設定才會套用
Switch(config-if)# end

# show ip
Switch# show ip interface
Switch# show ip interface Vlan 1
Switch# show ip interfaces brief
```

### interface

- Ethernet (Eth), 10 Mbps
- FastEthernet (Fa / FastEthernet), 100 Mbps
- GigabitEthernet (Gi / GigaEthernet), 1 Gbps (1000 Mbps)

```bash
# single interface / port
Switch(config)# interface FastEthernet 0/1
Switch(config-if)# shutdown
Switch(config-if)# no shutdown        # interface 設定完後, 建議要執行

# multi interface / port
Switch(config)# interface range FastEthernet 0/1 - 9
Switch(config-if-range)# shutdown
Switch(config-if-range)# no shutdown

# show interface
Switch# show interfaces
Switch# show interfaces status
Switch# show interfaces [<interface>]
```

---

## routing

```bash
# static IP
Router(config-if)# ip address <ip> <netmask>   # setup static ip

# DHCP / dynamic IP
Router(config-if)# ip dhcp                     # setup dynamic ip

# interface
Router(config-if)# no shutdown                 # 當 interface 設定完後, 要重啟設定才會套用
Router(config-if)# end
```

### static route

```bash
                R1                  R2
10.0.0.1/30     .1                  .2
                |                   |
                S1                  S2
                192.168.1.0/24      192.168.2.0/24

R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 10.0.0.1 255.255.255.252
R1(config-if)# no shutdown
R1(config)# ip route 192.168.2.0 255.255.255.0 10.0.0.2
R1# show ip route

R2(config)# interface GigabitEthernet0/0
R2(config-if)# ip address 10.0.0.2 255.255.255.252
R2(config-if)# no shutdown
R2(config)# ip route 192.168.1.0 255.255.255.0 10.0.0.1
R2# show ip route
```

### fault tolerance

```bash
                R1                  R2
10.0.0.1/30     .1                  .2
10.0.0.4/30     .5                  .6
                |                   |
                S1                  S2
                192.168.1.0/24      192.168.2.0/24

R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 10.0.0.1 255.255.255.252
R1(config-if)# no shutdown
R1(config)# ip route 192.168.2.0 255.255.255.0 10.0.0.2
R1(config)# interface GigabitEthernet0/1
R1(config-if)# ip address 10.0.0.5 255.255.255.252
R1(config-if)# no shutdown
R1(config)# ip route 192.168.2.0 255.255.255.0 10.0.0.6
R1# show ip route

R2(config)# interface GigabitEthernet0/0
R2(config-if)# ip address 10.0.0.2 255.255.255.252
R2(config-if)# no shutdown
R2(config)# ip route 192.168.1.0 255.255.255.0 10.0.0.1
R2(config)# interface GigabitEthernet0/0
R2(config-if)# ip address 10.0.0.6 255.255.255.252
R2(config-if)# no shutdown
R2(config)# ip route 192.168.1.0 255.255.255.0 10.0.0.5
R2# show ip route
```

### default route

```bash
                R1                  R2
10.0.0.1/30     .1                  .2
                |                   |
                S1                  S2
                192.168.1.0/24      192.168.2.0/24

R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 10.0.0.1 255.255.255.252
R1(config-if)# no shutdown
R1(config)# ip route 0.0.0.0 0.0.0.0 10.0.0.2
R1# show ip route

R2(config)# interface GigabitEthernet0/0
R2(config-if)# ip address 10.0.0.2 255.255.255.252
R2(config-if)# no shutdown
R2(config)# ip route 0.0.0.0 0.0.0.0 10.0.0.1
R2# show ip route
```

### dymanic route

- IGP / interior gateway protocol
  RIPV2, OSPF, EIGRP

- EFP / exterior gateway protocol
  BGP

```bash
                R1                  R2
10.0.0.1/30     .1                  .2
                |                   |
                S1                  S2
                192.168.1.0/24      192.168.2.0/24

R1(config)# interface GigabitEthernet0/0
R1(config-if)# ip address 10.0.0.1 255.255.255.252
R1(config-if)# no shutdown
R1(config)# router ospf 1
R1(config-router)# network 10.0.0.1 0.0.0.3 area 0
R1(config-router)# network 192.168.1.0 0.0.0.255 area 0
R1# show ip route
R1# show ip route ospf

R2(config)# interface GigabitEthernet0/0
R2(config-if)# ip address 10.0.0.2 255.255.255.252
R2(config-if)# no shutdown
R2(config)# ip route 0.0.0.0 0.0.0.0 10.0.0.1
R2(config)# router ospf 1
R2(config-router)# network 10.0.0.1 0.0.0.3 area 0
R2(config-router)# network 192.168.1.0 0.0.0.255 area 0
R2# show ip route
R2# show ip route ospf
```

```bash
192.168.0.0/24     10.0.1.0/30     192.168.10.0/24
                R1      -       R2
    10.0.4.0/30 |                | 10.0.2.0/30
                R4      -       R3
192.168.30.0       10.0.3.0/30     192.168.20.0/24

R1(config)# router ospf 1
R1(config-router)# network 192.168.0.0 0.0.0.255 area 0
R1(config-router)# network 10.0.1.0 0.0.0.3 area 0
R1(config-router)# network 10.0.4.0 0.0.0.3 area 0

R2(config)# router ospf 1
R2(config-router)# network 192.168.10.0 0.0.0.255 area 0
R2(config-router)# network 10.0.1.0 0.0.0.3 area 0
R2(config-router)# network 10.0.2.0 0.0.0.3 area 0

R3(config)# router ospf 1
R3(config-router)# network 192.168.20.0 0.0.0.255 area 0
R3(config-router)# network 10.0.2.0 0.0.0.3 area 0
R3(config-router)# network 10.0.3.0 0.0.0.3 area 0

R4(config)# router ospf 1
R4(config-router)# network 192.168.30.0 0.0.0.255 area 0
R4(config-router)# network 10.0.3.0 0.0.0.3 area 0
R4(config-router)# network 10.0.4.0 0.0.0.3 area 0
```

```bash
                                ISP  10.10.10.1
                                 |
192.168.0.0/24     10.0.1.0/30     192.168.10.0/24
                R1      -       R2
    10.0.4.0/30 |                | 10.0.2.0/30
                R4      -       R3
192.168.30.0       10.0.3.0/30     192.168.20.0/24

same above and add below

R2(config)# ip route 0.0.0.0 0.0.0.0 10.10.10.1
R2(config-router)# default-information originate
```

---

## vlan

Inter-VLAN Routing

### same subnet

```bash
                     S
                /   / \     \
             pc0  pc1  pc2  pc3
192.168.10   .11  .12  .13  .14
vlan 10 pc0, pc1
vlan 20 pc2, pc3
Switch(config)# vlan 10
Switch(config)# vlan 20

Switch(config)# interface Fa0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config)# spanning-tree portfast      # 不用等 30~50 秒

Switch(config)# interface Fa0/2
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config)# interface range Fa0/23-24
Switch(config)# spanning-tree portfast

Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport access vlan 20
Switch(config-if-range)# spanning-tree portfast

Switch# show vlan
Switch# show vlan brief

Switch# show flash        # vlan 設定會存到 flash 裡面的 vlan.dat
Switch# delete vlan.dat
```

```bash
               S1     -    S2
              /   \       /   \
             pc0  pc1   pc2   pc3
192.168.10   .11  .12   .13   .14
vlan 10 pc0, pc2
vlan 20 pc1, pc3

S1(config)# interface vlan 10
S1(config)# interface vlan 20

S1(config)# interface Fa0/1
S1(config-if)# switchport mode access
S1(config-if)# switchport access vlan 10
S1(config-if)# spanning-tree portfast

S1(config)# interface Fa0/24
S1(config-if)# switchport mode access
S1(config-if)# switchport access vlan 20
S1(config-if)# spanning-tree portfast

S1(config)# interface range GigabitEthernet 0/1-2
S1(config-if-range)# switchport mode trunk
S1# show interfaces trunk

#
S2(config)# interface vlan 10
S2(config)# interface vlan 20

S2(config)# interface Fa0/1
S2(config-if)# switchport mode access
S2(config-if)# switchport access vlan 10
S2(config-if)# spanning-tree portfast

S2(config)# interface Fa0/24
S2(config-if)# switchport mode access
S2(config-if)# switchport access vlan 20
S2(config-if)# spanning-tree portfast

S2(config)# interface range GigabitEthernet 0/1-2
S2(config-if-range)# switchport mode trunk
S2# show interfaces trunk
```

### trunk link

| Swtich A          | Swtich B          | Trunk Link |
| ----------------- | ----------------- | ---------- |
| trunk             | trunk             | pass       |
| trunk             | dynamic auto      | pass       |
| trunk             | dynamic desirable | pass       |
| trunk             | access            | fail       |
| dynamic desirable | dynamic desirable | pass       |
| dynamic desirable | dynamic auto      | pass       |
| dynamic auto      | dynamic auto      | fail       |

```bash
S2(config)# interface range GigabitEthernet 0/1
S2(config-if)# switchport mode dynamic desirable

S2# show interfaces trunk
```

### different subnet

Router-on-a-Stick

```bash
0/0.1    192.168.1.0/24
0/0.10   192.168.10.0/24
0/0.20   192.168.20.0/24
               R
               |
               S1     -    S2
              /   \       /   \
             pc0  pc1   pc2   pc3
192.168.10   .11        .13
192.168.20        .12        .14
vlan 10 pc0, pc2
vlan 20 pc1, pc3

same above and add below

Router(config)# interface gi0/0
Router(config-if)# no ip address
Router(config-if)# no shutdown

Router(config)# interface GigabitEthernet 0/0.10
Router(config-subif)# encapsulation dot1Q 10
Router(config-subif)# ip address 192.168.10.1 255.255.255.0

Router(config-subif)# interface GigabitEthernet 0/0.20
Router(config-subif)# encapsulation dot1Q 20
Router(config-subif)# ip address 192.168.20.1 255.255.255.0

Router(config)# ip routing
```

---

## port-security

```bash
       PC0
        |
        S
        |
        H
      /   \
    PC1   PC2

Switch(config)# interface FastEther 0/24
Switch(config-if)# switchport mode access
Switch(config-if)# switchport port-security
Switch(config-if)# switchport port-security maximum 1
Switch(config-if)# switchport port-security mac-address [<MAC address>]
Switch(config-if)# switchport port-security violation restrict
# protect|restrict|shutdown

Switch# clear port-security all
```

---

## acl

- Stateless ACL
- Stateful ACL

| \\         | Standard ACL       | Extended ACL                            | Named ACL |
| ---------- | ------------------ | --------------------------------------- | --------- |
| port       | 1 - 99, 1300- 1999 | 100 - 199, 2000 - 2699                  | -         |
| limitation | source ip          | source ip & port, destination ip & port | -         |

acl 要綁在離 target 越近越好

### standard acl

```bash
Srv0 - S0 - R0  --- R1 - S1 -- Srv1

192.168.10.0/24: Srv0, R0
192.168.30.0/24: Srv1, R1  |  Srv1 -> 192.168.10.0/24
10.0.0.1/30:     R0, R1

# routing
R0(config) ip routing
R0(config) route ospf 1
R0(config-router)# network 192.168.10.0 0.0.0.255 area 0
R0(config-router)# network 10.0.0.1 0.0.0.3 area 0

R1(config) ip routing
R1(config) route ospf 1
R1(config-router)# network 192.168.30.0 0.0.0.255 area 0
R1(config-router)# network 10.0.0.1 0.0.0.3 area 0

# acl
R0(config)# access-list 10 permit 192.168.30.10 0.0.0.0
R0(config)# interface GigabitEthernet 0/0/0
R0(config-if)# ip access-group 10 out
# out: 離開 router
# in:  進入 router

R0# show access-lists
R0# show ip access-lists

R0(config)# interface GigabitEthernet0/0/0
R0(config-if)# no ip access-group 10 out
R0(config)# no access-list 10 permit host 192.168.30.10
```

```bash

PC0      S1  - PC1
|        |
S0   -   R0     ---    R1   - S3  - Srv
|        |
PC3      S2  - PC2

172.16.1.0/24:  S0, PC0     | PC0 -> Srv, PC3 x> Srv
172.16.2.0/24:  S1, PC1     | -> Srv
172.16.3.0/24:  S2, PC2     | x> Srv
172.16.4.0/24:  R0, R1      |
172.16.5.0/24:  S3, Srv     |

# routing
R0(config)# router ospf 1
R0(config)# ip routing
R0(config-router)# network 172.16.1.0 0.0.0.255 area 0
R0(config-router)# network 172.16.2.0 0.0.0.255 area 0
R0(config-router)# network 172.16.3.0 0.0.0.255 area 0
R0(config-router)# network 172.16.4.0 0.0.0.3 area 0

# routing
R1(config)# router ospf 1
R1(config)# ip routing
R1(config-router)# network 172.16.4.0 0.0.0.3 area 0
R1(config-router)# network 172.16.5.0 0.0.0.255 area 0

# acl
R1(config)# access-list 10 permit 172.16.1.11 0.0.0.0
# 功能同上
# R1(config)# access-list 10 permit host 172.16.1.11
R1(config)# access-list 10 deny 172.16.1.0 0.0.0.255
R1(config)# access-list 10 permit 172.16.2.0 0.0.0.255
# 有建立 acl, 會在最後一行自動加入以下
# R1(config)# access-list 10 deny any
# 功能同上
# R1(config)# access-list 10 deny 0.0.0.0 255.255.255.255

R1(config)# interface GigabitEthernet 0/0
R1(config-if)# ip access-group 10 out

R1# show access-lists
R1# show ip access-lists
```

### extended acl

```bash
Srv0 - S0 - R0  --- R1 - S1 -- Srv1

192.168.10.0/24: Srv0, R0  |  x> 192.168.20.2/24 (ping & web)
192.168.30.0/24: Srv1, R1
10.0.0.1/30:     R0, R1

# routing, 同上

# acl
R0(config)# access-list 110 deny tcp 192.168.10.10 0.0.0.255 192.168.30.10 0.0.0.0 eq 80  # http
R0(config)# access-list 110 deny tcp 192.168.10.10 0.0.0.255 192.168.30.10 0.0.0.0 eq 443 # https
R0(config)# access-list 110 deny icmp 192.168.10.10 0.0.0.255 192.168.30.10 0.0.0.0 8 # icmp
R0(config)# access-list 110 permit ip any any
R0(config)# interface GigabitEthernet 0/0/0
R0(config-if)# ip access-group 10 in

R0# show access-lists
R0# show ip access-lists
```

### named acl

```bash
Srv0 - S0 - R0  --- R1 - S1 -- Srv1

192.168.10.0/24: Srv0, R0  |  x> 192.168.20.2/24 (ping & web)
192.168.30.0/24: Srv1, R1
10.0.0.1/30:     R0, R1

# routing, 同上

# acl
R0(config)# ip access-list extended b30
R0(config-ext-nacl)# deny tcp 192.168.10.10 0.0.0.255 192.168.30.10 0.0.0.0 eq 80  # http
R0(config-ext-nacl)# deny tcp 192.168.10.10 0.0.0.255 192.168.30.10 0.0.0.0 eq 443 # https
R0(config-ext-nacl)# deny icmp 192.168.10.10 0.0.0.255 192.168.30.10 0.0.0.0 8 # icmp
R0(config-ext-nacl)# permit ip any any
R0(config)# interface GigabitEthernet 0/0/0
R0(config-if)# ip access-group b30 in

R0# show access-lists
R0# show ip access-lists
```

---

## nat

inside local
outside local
inside global
outsode glbal

---

## ipv6
