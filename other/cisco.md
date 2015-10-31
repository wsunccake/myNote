# CISCO #


## Basic ##


### enable privilege ###

	# privilege mode
	CISCO> enable
	CISCO#

	# config mode
	CISCO# configure terminal
	CISCO(config)#


### common ###

	# 設定 hostname
	CISCO(config)# hostname <hostname>

	# 設定游標
	CISCO(config) # line console 0
	CISCO(config-line) # logging synchronous

	# 關閉 DNS 查詢, 避免輸入錯誤命令時, iOS 向 DNS 伺服器進行查詢
	CISCO(config)# no ip domain lookup


### setup login ###

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


### setup IP ###

	# for router
	CISCO(config) # interface FastEthernet 0/1
	CISCO(config-if)# ip address <ip> <netmask> # static IP
	CISCO(config-if)# ip address dhcp           # DHCP / dynamic IP
	CISCO(config-if)# no shutdown               # 開啟 interface

	# for switch
	CISCO(config)# interface Vlan 1
	CISCO(config-if)# ip address <ip> <netmask> # static IP
	CISCO(config-if)# ip address dhcp           # DHCP / dynamic IP
	CISCO(config-if)# no shutdown               # 開啟 interface


### list ###

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


## Vlan ##

	# enable vlan for interface
	CISCO# configure terminal
	CISCO(config)# interface TenGigabitEthernet 1/1
	CISCO(config-if)# switchport access vlan 10
	CISCO(config-if)# no shutdown

	# disable vlan for interface
	CISCO# no switchport access vlan 10
	CISCO# no shutdown

	# check vlan for interface
	CISCO# show spanning-tree interface TenGigabitEthernet 1/1