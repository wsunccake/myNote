# Hostname #


## config file ##

/etc/hostname


## daemon ##

```
rhel:~ # systemctl restart systemd-hostnamed
```

## command ##

```
# method 1: using hostnamectl setup hostname
rhel:~ # hostnamectl status
rhel:~ # hostnamectl set-hostname name # setup hostname
rhel:~ # hostnamectl set-hostname "" # empty hostname
rhel:~ # hostnamectl set-hostname -H [username]@hostname # setup remote hostname

# method 2: using nmcli setyo hostname
rhel:~ # nmcli general hostname
rhel:~ # nmcli general hostname my-server
```


# RedHat Networking  #


## nm vs networking ##

| NetworkManager		| The default networking daemon		|
| --------------------- | --------------------------------- |
| nmtui					| tui for NetworkManager			|
| nmcli					| cli with NetworkManager			|
| control-center		| gui by the GNOME Shell			|
| nm-connection-editor	| gui by A GTK+ 3 application		|

/etc/sysconfig/network-scripts/ifcfg-ifname

/etc/NetworkManager


```
rhel:~ # yum install NetworkManager
rhel:~ # systemctl status NetworkManager.service
rhel:~ # systemctl start NetworkManager.service
rhel:~ # systemctl enable NetworkManager.service

rhel:~ # systemctl restart network.service
```


## ifcfg vs nmcli ##

/usr/share/doc/initscripts-version/sysconfig.txt

| ifcfg command 				 | nmcli command 				 |
| ------------------------------ | ----------------------------- |
| /etc/init.d/network restart 	 | 	nmcli connection reload 	 |
| ifup eth0 					 | 	nmcli connection up eth0 	 |
| ifdown eth0 					 | 	nmcli connection down eth0 	 |


## nmtui ##

```
rhel:~ # yum install NetworkManager-tui
rhel:~ # nmtui
rhel:~ # nmtui edit con-name
rhel:~ # nmtui connect con-name
```


## nmcli ##

```
rhel:~ # ip -V
rhel:~ # nmcli help
rhel:~ # nmcli general help
rhel:~ # nmcli device status
rhel:~ # nmcli device show
rhel:~ # nmcli device show ifname
rhel:~ # nmcli device connect ifname
rhel:~ # nmcli device disconnect ifname

rhel:~ # nmcli connection reload
rhel:~ # nncli connection load /etc/sysconfig/network-script/ifcfg-ifname
rhel:~ # nmcli connection up con-name
rhel:~ # nmcli connection down con-name
rhel:~ # nmcli connection show
rhel:~ # nmcli connection show con-name
rhel:~ # nmcli connection show --active
rhel:~ # nmcli connection modify con-name 802-11-wireless.mtu 1350 # 不會改變 ifcfg-ifname 的設定, 但是實際設定會變

rhel:~ # nmcli connection type ethernet add ifname eth0 con-name eth0 # create /etc/sysconfig/network-script/ifcfg-ifname
rhel:~ # nmcli connection delete eth0 # remove ifcfg-ifname

rhel:~ # nmcli connection edit
rhel:~ # nmcli connection edit [con-name]
nmcli> print
nmcli> describe ipv4.method
nmcli> set ipv4.method auto
nmcli> set connection.id eth0 # con-name
nmcli> set connection.interface-name eth0 # ifname
nmcli> set 802-11-wireless.mtu auto # 只有目前設定會改變, 但未套用
nmcli> save # 將設定寫入 ifcfg-ifname, 並套用
nmcli> quit

rhel:~ # nmcli general status
```


# Networking IP #


## static ip ##


### setting ###

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # nmcli connection add type ethernet ifname eth0 con-name eth0 ip4 10.0.0.11/24 gw4 10.0.0.1
rhel:~ # nmcli connection add type ethernet ifname eth0 con-name eth0 ip4 10.0.0.11/24 gw4 10.0.0.1 ip6 abbe::cafe gw6 2001:db8::1 # 可同時設定 IPv4, IPv6
rhel:~ # nmcli connection modify eth0 ipv4.dns 8.8.8.8
rhel:~ # nmcli connection modify eth0 "8.8.8.8 8.8.4.4" # 可同時設定多組 DNS
rhel:~ # nmcli connection modify eth0 +ipv4.dns "8.8.8.8 8.8.4.4"

# method 3:
rhel:~ # ip link show  # 顯示網卡狀態
rhel:~ # ip link set dev eth0 up # 開啟網卡
rhel:~ # ip link set dev eth0 down # 關閉網卡

rhel:~ # ip addr show # 顯示網卡 IP
rhel:~ # ip addr add 10.0.0.3/24 dev eth0 # 新增網卡 IP
rhel:~ # ip addr del 10.0.0.3/24 dev eth0 # 刪除網卡 IP

rhel:~ # ip route # 顯示路由
rhel:~ # ip route add default via 10.0.3.254 dev eth0 # 新增預設路由
rhel:~ # ip route del default via 10.0.3.254 dev eth0 # 刪除預設路由
rhel:~ # ip route add 192.168.0.0/24 via 10.0.3.254 dev eth0 # 新增靜態路由
rhel:~ # ip route add via 192.168.0.254 dev eth1 # 新增路由
rhel:~ # ip route del via 192.168.0.254 dev eth1 # 刪除路由
rhel:~ # ip route del 192.168.0.0/24 via 10.0.3.254 dev eth0 # 刪除靜態路由


# method 4:
rhel:~ # ifconfig -a # 顯示網卡狀態
rhel:~ # ifconfig eth0 up # 開啟網卡
rhel:~ # ifconfig eth0 down # 關閉網卡

rhel:~ # ifconfig eth0 10.0.0.3 netmask 255.255.255.0 # 新增網卡 IP
rhel:~ # ifconfig eth0 0.0.0.0 netmask 255.255.255.0 # 刪除網卡 IP

rhel:~ # route add default gw 10.0.3.253 dev eth0 # 新增預設路由
rhel:~ # route del default gw 10.0.3.253 dev eth0 # 刪除預設路由
rhel:~ # route add -net 192.168.0.0 netmask 255.255.255.0 dev eth0 # 新增靜態路由
rhel:~ # route add gw 192.168.0.254 dev eth1 # 新增路由
rhel:~ # route del gw 192.168.0.254 dev eth1 # 刪除路由
rhel:~ # route del -net 192.168.0.0 netmask 255.255.255.0 dev eth0 # 刪除靜態路由
```

IPv6 方式跟 IPv4 一樣, 將 ipv4 改成 ipv6 即可


### config file ###

```
# 設定 IP
rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ifname
DEVICE=eth0
BOOTPROTO=none
ONBOOT=yes
PREFIX=24
IPADDR=10.0.1.27

# 指定路由
rhel:~ # cat /etc/sysconfig/network-script/route-ifname
192.168.1.0/24 via 10.0.3.1
```

## dhcp ##


### setting ###

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # nmcli connection add type ethernet ifname eth0 con-name eth0
rhel:~ # nmcli connection modify eth0 ipv4.dhcp-hostname host-name
rhel:~ # nmcli connection modify eth0 ipv4.ignore-auto-dns yes

# method 3:
rhel:~ # dhclient eth0

# remove dhcp client
rhel:~ # dhclient -x
```


### config file ##

```
rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ifname
DEVICE=em1
BOOTPROTO=dhcp
ONBOOT=yes

DHCP_HOSTNAME=hostname # 不使用 DHCP 所派的 hostname
PEERDNS=no # 不使用 DHCP 預設的 DNS
DNS1=ip-address # 當 PEERDNS=no, 才能另外指定 DNS1
DNS2=ip-address
```


## wifi ##

```
rhel:~ # nmcli dev wifi list
rhel:~ # nmcli connection type wifi add con-name MyCafe ifname wlan0 ssid MyCafe ip4 192.168.100.101/24 gw4 192.168.100.1
rhel:~ # nmcli connection modify MyCafe wifi-sec.key-mgmt wpa-psk # 設定連線加密方式
rhel:~ # nmcli connection modify MyCafe wifi-sec.psk caffeine # 設定 WPA2 password 為 caffeine
rhel:~ # nmcli radio wifi on
rhel:~ # nmcli radio wifi off
```


## multiple nic config file ##

```
rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ifname
HWADDR=11:22:33:44:55:66
TYPE=Ethernet
BOOTPROTO=dhcp # dhcp
DEFROUTE=yes # 設定為 default gateway, multiple NIC 環境中很重要
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no
NAME="eth0"
ONBOOT=yes # 開機使否開啟
NM_CONTROLLED=yes # 可否由 Network Manager
```


## GUI ##

```
rhel:~ # gnome-control-center network
```


# Networking Bond #


## setting ##

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # nmcli connection add type bond ifname bond0 cos-name bond0
rhel:~ # nmcli connection edit bond0
nmcli> describe bond.options
nmcli> set bond.options mode=active-backup
nmcli> save
nmcli> quit

rhel:~ # nmcli connection add type bond-slave ifname eth0 con-name eth0 master bond0
rhel:~ # nmcli connection add type bond-slave ifname eth1 con-name eth1 master bond0

# method 3:
rhel:~ # modprobe bonding
rhel:~ # modinfo bonding
rhel:~ # echo +bond0 >> /sys/class/net/bond_masters
rhel:~ # ip link set dev bond0 up
rhel:~ # ifenslave bond0 eth0 eth1

# remove bond
rhel:~ # ifenslave -d bond0 eth0 eth1
rhel:~ # ip link set dev bond0 down
rhel:~ # echo -bond0 >> /sys/class/net/bond_masters

# bond option
rhel:~ # echo 1000 > /sys/class/net/bond0/bonding/miimon
rhel:~ # echo 6 > /sys/class/net/bond0/bonding/mode
rhel:~ # echo balance-alb > /sys/class/net/bond0/bonding/mode

# check miimon
rhel:~ # ethtool interface_name | grep "Link detected:"
```


## config file ##

```
rhel~: # cat /etc/syscofnig/network-script/ifcfg-bond0
DEVICE=bond0
TYPE=Bond
NAME=bond0
BONDING_MASTER=yes
BOOTPROTO=dhcp
BONDING_OPTS="bonding parameters separated by spaces"
ONBOOT=yes

rhel~: # cat /etc/syscofnig/network-script/ifcfg-eth0
MACADDR=00:11:22:33:44:55
TYPE=Ethernet
NAME=eth0
DEVICE=eth0
ONBOOT=yes
MASTER=bond0
SLAVE=yes

rhel~: # cat /etc/syscofnig/network-script/ifcfg-eth1
MACADDR=00:11:22:33:44:56
TYPE=Ethernet
NAME=eth1
DEVICE=eth1
ONBOOT=yes
MASTER=bond0
SLAVE=yes
```


## GUI ##

```
rhel:~ # gnome-control-center network
```


# Networking Team #


## package ##

teamd, ethtool, arp_ping, nsna_ping, lacp

```
rhel:~ # yum install teamd
```


## bond to team ##

```
rhel:~ # bond2team --master bond0
rhel:~ # bond2team --master bond0 --rename team0
rhel:~ # bond2team --master bond0 --configdir /path/to/ifcfg-file
rhel:~ # bond2team --bonding_opts "mode=1 miimon=500"
rhel:~ # bond2team --bonding_opts "mode=1 miimon=500 primary=eth1 primary_reselect-0" --port eth1 --port eth2 --port eth3 --port eth4
```


## setting ##

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # nmcli connection add type team ifname team0 cos-name team0
rhel:~ # nmcli connection edit team0
nmcli> describe team.config
nmcli> set team.config {"runner": {"name": "activebackup"}}
nmcli> save
nmcli> quit

rhel:~ # nmcli connection add type team-slave ifname eth0 con-name eth0 master team0
rhel:~ # nmcli connection add type team-slave ifname eth1 con-name eth1 master team0

# method 3:
rhel:~ # ls /usr/share/doc/teamd-*/example_configs
rhel:~ # cp /usr/share/doc/teamd-*/example_configs/activebackup_ethtool_1.conf ~
rhel:~ # vi activebackup_ethtool_1.conf
rhel:~ # ip link set dev eth0 down
rhel:~ # ip link set dev eth1 down
rhel:~ # teamd -g -f activebackup_ethtool_1.conf -d

# 同上, 使用指令方式
rhel:~ # teamd -t team0 -d
rhel:~ # ip link set dev eth0 master team0
rhel:~ # ip link set dev team0 down

# 查看
rhel:~ # teamnl team0 ports
rhel:~ # teamnl team0 getoption activeport
rhel:~ # teamnl team0 setoption activeport 5
rhel:~ # teamnl team0 setoption mode activebackup

rhel:~ # teamdctl team0 state
rhel:~ # teamdctl team0 state view -vv
rhel:~ # teamdctl team0 config dump
rhel:~ # teamdctl team0 port add eth2
rhel:~ # teamdctl team0 port remove eth2
rhel:~ # cat eth2-cfg.json
{
  "prio": -10,
  "sticky": true
}
rhel:~ # teamdctl team0 port config update eth2 eth2-cfg.json

# remove team
rhel:~ # teamd -t team0 -k
```


## config file ##

```
rhel:~ # cat /etc/syscofnig/network-script/ifcfg-team0
DEVICE=team0
DEVICETYPE=Team
NAME=team0
BOOTPROTO=dhcp
UUID=c9b24f8d-69e8-4b0f-9656-c7ed8e7c0b2e
ONBOOT=yes
TEAM_CONFIG="{\"runner\":{\"name\": \"activebackup\"}}"

rhel:~ # cat /etc/syscofnig/network-script/ifcfg-eth0
NAME=eth0
DEVICE=eth0
ONBOOT=yes
TEAM_MASTER=c9b24f8d-69e8-4b0f-9656-c7ed8e7c0b2e
DEVICETYPE=TeamPort

rhel:~ # cat /etc/syscofnig/network-script/ifcfg-eth1
NAME=eth1
DEVICE=eth1
ONBOOT=yes
TEAM_MASTER=c9b24f8d-69e8-4b0f-9656-c7ed8e7c0b2e
DEVICETYPE=TeamPort
```


## GUI ##

```
rhel:~ # gnome-control-center network
```


# Networking Bridge #


## package ##

```
rhel:~ # yum install bridge-utils
```

## bridge ##

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # nmcli connection add type bridge ifname br0 cos-name br0
rhel:~ # nmcli connection edit bond0
nmcli> print
nmcli> set bridge.stp yes
nmcli> save
nmcli> quit

rhel:~ # nmcli connection add type bridge-slave ifname eth0 cons-name eth0 master br0

# method 3:

rhel:~ # modprobe bridge
rhel:~ # modinfo bridge

rhel:~ # brctl addbr br0
rhel:~ # brctl addif br0 eth0

rhel:~ # brctl show

# remove bridge
rhel:~ # brctl delif br0 eth0
rhel:~ # brctl delbr br0
```


## config file ##

```
rhel:~ # cat /etc/syscofnig/network-script/ifcfg-br0
DEVICE=br0
STP=yes
TYPE=Bridge
BOOTPROTO=dhcp
NAME=br0
ONBOOT=yes
BRIDGING_OPTS=priority=4096

rhel:~ # cat /etc/syscofnig/network-script/ifcfg-eth0
TYPE=Ethernet
NAME=eth0
DEVICE=eth0
ONBOOT=yes
BRIDGE=br0
```


## GUI ##

```
rhel:~ # gnome-control-center network
```


# Networking 802.1q VLAN #


## package ##

```
rhel:~ # yum install vconfig
```


## settting ##

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # nmcli connection add type vlan ifname eth0.10 con-name eth0.10 id 10 dev eth0 # create  eth0.10

# method 3:
rhel:~ # modprobe 8021q
rhel:~ # modinfo 8021q

rhel:~ # ip link add link eth0 name eth0.10 type vlan id 10
rhel:~ # ip -d link show

# remove vlan
rhel:~ # ip link del eth0.10

# method 4:
rhel:~ # vconfig add eth0 10

# remove vlan
rhel:~ # vconfig rem eth0.10
```


## config file ##

```
rhel:~ # cat ifcfg-eth0.10 
VLAN=yes
TYPE=Vlan
DEVICE=eth0.10
PHYSDEV=eth0
VLAN_ID=10
BOOTPROTO=dhcp
ONBOOT=yes
```

## GUI ##

```
rhel:~ # gnome-control-center network
```


# Networking VPN #


## pptp ##

```
rhel:~ # yum install NetworkManager-pptp NetworkManager-pptp-gnome

# method 1:
rhel:~ # nmcli connection add type vpn con-name vpn0 ifname vpn0 vpn-type pptp
rhel:~ # nmcli connection edit vpn0
nmcli> set vpn.data password-flags = 0, user = vpn_user, require-mppe = yes, gateway = vpn_server_ip
nmcli> set vpn.secrets password = vpn_password
nmcli> save
nmcli> quit

# firewall
rhel:~ # firewall-cmd --direct --add-rule ipv4 filter INPUT 0 -p gre -j ACCEPT
rhel:~ # firewall-cmd --permanent --direct --add-rule ipv6 filter INPUT 0 -p gre -j ACCEPT
rhel:~ # firewall-cmd --reload

# method 2:
rhel:~ # gnome-control-center network
```

## l2tp ##

```
rhel:~ # yum install NetworkManager-l2tp NetworkManager-l2tp-gnome
```


## ipsec ##

```
rhel:~ # yum install NetworkManager-libreswan NetworkManager-libreswan-gnome
```


# Networking Device Naming #

biosdevname

udev

Scheme 1: Names incorporating Firmware or BIOS provided index numbers for on-board devices (example: eno1), are applied if that information from the firmware or BIOS is applicable and available, else falling back to scheme 2.
Scheme 2: Names incorporating Firmware or BIOS provided PCI Express hotplug slot index numbers (example: ens1) are applied if that information from the firmware or BIOS is applicable and available, else falling back to scheme 3.
Scheme 3: Names incorporating physical location of the connector of the hardware (example: enp2s0), are applied if applicable, else falling directly back to scheme 5 in all other cases.
Scheme 4: Names incorporating interface's MAC address (example: enx78e7d1ea46da), is not used by default, but is available if the user chooses.
Scheme 5: The traditional unpredictable kernel naming scheme, is used if all other methods fail (example: eth0).


## device name procedure ##

1. /usr/lib/udev/rules.d/60-net.rules

	/lib/udev/rename_device look into all /etc/sysconfig/network-scripts/ifcfg-ifname

2. /usr/lib/udev/rules.d/71-biosdevname.rules

	biosdevname rename the interface, (biosdevname=0)

3. /lib/udev/rules.d/75-net-description.rules

	udev fill in the internal udev device, ID_NET_NAME_ONBOARD, ID_NET_NAME_SLOT, ID_NET_NAME_PATH, ID_NET_NAME_MAC

4. /usr/lib/udev/rules.d/80-net-name-slot.rules

	udev rename the interface, ID_NET_NAME_ONBOARD, ID_NET_NAME_SLOT, ID_NET_NAME_PATH (net.ifnames=0)


## nic device name ##

1. en for Ethernet

2. wl for wireless LAN (WLAN)

3. ww for wireless wide area network (WWAN)


## disable biosdevname ##

	rhel:~ # cat /etc/default/grub
	GRUB_CMDLINE_LINUX="... net.ifnames=0 biosdevname=0" # 多加 net.ifnames, biosdevname 設定
	rhel:~ # grub2-mkconfig > /boot/grub2/grub.cfg


## Trouble shooting ##

```
rhel:~ # udevadm info /sys/class/net/ifname | grep ID_NET_NAME
rhel:~ # ls /sys/class/net/
```


# Network Namespace #

```
rhel:~ # ip netns list
rhel:~ # ip netns add qdhcp
rhel:~ # ip netns exec qdhcp ip addr show
rhel:~ # ip netns delete qdhcp

rhel:~ # ip -all netns exec ip addr show
rhel:~ # ip -all netns delete
```


# Netowkr Veth Paire #

```
rhel:~ # ip link add veth0 type veth peer name veth1
rhel:~ # ip -d link show
5: veth1@veth0: ...
6: veth0@veth1: ...
# 在相同 namespace 裡, veth1@veth0 表示 veth0 <-> veth1


rhel:~ # ip link set veth1 netns qdhcp
rhel:~ # ip -d link show
6: veth0@if5: ...
rhel:~ # ip netns exec qdhcp ip -d link show
5: veth1@if6: ...
# 在不同 namespace 裡, veth0@if5 表示 veth0 <-> if5, 但在 另一個 namespce 找到 index 5 為 veth1, 所以 veth0 <-> if5 - if6 <-> veth1
```

# InfiniBand & Remote Direct Memory Access #

## HW ##

IB (InfiniBand), RDMA (Remote Direct Memory Access)

iWARP: Chelsio hardware — libcxgb3 or libcxgb4

RoCE/IBoE: Mellanox hardware — libmlx4 or libmlx5


## package ##

`Required`

- rdma, libibverbs, opensm

`Recommended`

- librdmacm, librdmacm-utils, ibacm

- libibverbs-utils

- infiniband-diags, ibutils

- perftest, qperf

`Optional`

- dapl, dapl-devel, dapl-utils

- openmpi, mvapich2, mvapich2-psm

## RDMA ##

	rhel:~ # yum install rdma
	rhel:~ # dracut -f # rebuild initrd
	rhel:~ # systemctl enable rdma

- /etc/rdma/rdma.conf

- /etc/udev.d/rules.d/70-persistent-ipoib.rules

- /etc/security/limits.d/rdma.conf

- /etc/rdma/mlx4.conf or  /etc/rdma/mlx5.conf


## opensm ##

opensm is IB subnet manager. all InfiniBand networks must have a subnet manager running for the network to function.

	/etc/sysconfig/opensm

	/etc/rdma/opensm.conf

	/etc/rdma/partitions.conf

	systemctl enable opensm


## testing ##

```
rhel:~ # yum install libibverbs-utils
rhel:~ # ibv_devices
rhel:~ # ibv_devinfo
rhel:~ # ibv_devinfo -d mlx4_1
rhel:~ # ibstat mlx4_1

rhel:~ # yum install infiniband-diags
rhel:~ # ibping -S -C mlx4_1 -P 1
rhel:~ # ibping -c 10000 -f -C mlx4_0 -P 1 -L 2
rhel:~ # ibping -c 10000 -f -C mlx4_0 -P 1 -G 0xf4521403007bcba1
```


## IPoIB ##

```
# method 1:
rhel:~ # nmtui

# method 2:
rhel:~ # rmmod ib_ipoib
rhel:~ # modprobe ib_ipoib

rhel:~ # nmcli connection add type infiniband con-name mlx4_ib0 ifname mlx4_ib0 transport-mode connected mtu 65520
rhel:~ # nmcli connection edit mlx4_ib0
nmcli> set infiniband.mac-address 80:00:02:00:fe:80:00:00:00:00:00:00:f4:52:14:03:00:7b:cb:a3
nmcli> set ipv4.ignore-auto-dns yes
nmcli> set ipv4.ignore-auto-routes yes
nmcli> set ipv4.never-default true
nmcli> set ipv6.ignore-auto-dns yes
nmcli> set ipv6.ignore-auto-routes yes
nmcli> set ipv6.never-default true
nmcli> save
nmcli> quit

rhel:~ # nmcli con add type infiniband con-name mlx4_ib0.8002 ifname mlx4_ib0.8002 parent mlx4_ib0 p-key 0x8002 # create with P key
```


## config file ##

```
rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ib0
DEVICE=mlx4_ib0
TYPE=InfiniBand
ONBOOT=yes
HWADDR=80:00:00:4c:fe:80:00:00:00:00:00:00:f4:52:14:03:00:7b:cb:a1
BOOTPROTO=none
IPADDR=172.31.0.254
PREFIX=24
NETWORK=172.31.0.0
BROADCAST=172.31.0.255
MTU=65520
CONNECTED_MODE=yes
NAME=mlx4_ib0

rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ib0.8002
DEVICE=mlx4_ib0.8002
PHYSDEV=mlx4_ib0
PKEY=yes
PKEY_ID=2
TYPE=InfiniBand
ONBOOT=yes
HWADDR=80:00:00:4c:fe:80:00:00:00:00:00:00:f4:52:14:03:00:7b:cb:a1
BOOTPROTO=none
IPADDR=172.31.2.254
PREFIX=24
NETWORK=172.31.2.0
BROADCAST=172.31.2.255
MTU=65520
CONNECTED_MODE=yes
NAME=mlx4_ib0.8002
```


## GUI ##

```
rhel:~ # gnome-control-center network
```


# DHCP #


## dhcp ##


### package ###

```
rhel:~ # yum install dhcp

rhel:~ # systecmctl enable dhcpd.service # or copy /usr/lib/systemd/system/dhcpd.service to /etc/systemd/system/
rhel:~ # vi /etc/systemd/system/dhcpd.service
...
ExecStart=/usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid eth0
...
rhel:~ # systemctl --system daemon-reload
rhel:~ # systemctl restart dhcpd

rhel:~ # systemctl start dhcpd.service
rhel:~ # systemctl stop dhcpd.service
```


### config file ###

```
rhel:~ # cp /usr/share/doc/dhcp-version_number/dhcpd.conf.example /etc/dhcp/dhcpd.conf # example

rhel:~ # cat /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
option subnet-mask 255.255.255.0;
option broadcast-address 192.168.1.255;
option routers 192.168.1.254;
option domain-name-servers 192.168.1.1, 192.168.1.2;
option domain-search "example.com";
subnet 192.168.1.0 netmask 255.255.255.0 {
   range 192.168.1.10 192.168.1.100;
   host apex {
      option host-name "apex.example.com";
      hardware ethernet 00:A0:78:8E:9E:AA;
      fixed-address 192.168.1.4;
   }
}

rhel:~ # ls /var/lib/dhcpd/dhcpd.leases
```


## dhcrelay ##

DHCP Relay Agent (dhcrelay) enables the relay of DHCP and BOOTP requests from a subnet with no DHCP server on it to one or more DHCP servers on other subnets.

`IPv4`

```
rhel:~ # systecmctl enable dhcpd.service # or copy /lib/systemd/system/dhcrelay.service to /etc/systemd/system/
rhel:~ # vi /etc/systemd/system/dhcrelay.service
...
ExecStart=/usr/sbin/dhcrelay -d --no-pid 192.168.1.1 [-i eth1] # 192.168.1.1 is dhcp server ip, eth1 is specfic listen nic
...
rhel:~ # systemctl --system daemon-reload
rhel:~ # systemctl restart dhcrelay
```


`IPv6`

```
rhel:~ # cp /lib/systemd/system/dhcrelay.service /etc/systemd/system/dhcrelay6.service
rhel:~ # vi /etc/systemd/system/dhcrelay6.service
...
ExecStart=/usr/sbin/dhcrelay -d --no-pid -6 -l em1 -u em2
...
rhel:~ # systemctl --system daemon-reload
rhel:~ # systemctl restart dhcrelay6
```


# DNS #

`authoritative`
Authoritative nameservers answer to resource records that are part of their zones only. This category includes both primary (master) and secondary (slave) nameservers.
`recursive`
Recursive nameservers offer resolution services, but they are not authoritative for any zone. Answers for all resolutions are cached in a memory for a fixed period of time, which is specified by the retrieved resource record.


/etc/named.conf
/etc/named.d


bind-chroot
/var/named/chroot/
vim -c "set backupcopy=yes" /etc/named.conf

## bind-chroot ##

```
rhel:~ # yum install bind-chroot
rhel:~ # systemctl status named
rhel:~ # systemctl stop named
rhel:~ # systemctl disable named
rhel:~ # stemctl enable named-chroot
rhel:~ # systemctl start named-chroot
rhel:~ # systemctl status named-chroot
```


### config file ###

```
rhel:~ # vi /etc/named.conf
acl black-hats {
  10.0.2.0/24;
  192.168.0.0/24;
  1234:5678::9abc/24;
};

acl red-hats {
  10.0.1.0/24;
};

options {
  blackhole { black-hats; };
  allow-query { red-hats; localhost; };
  allow-query-cache { red-hats; };

  listen-on port    53 { 127.0.0.1; };
  listen-on-v6 port 53 { ::1; };
  max-cache-size    256M;
  directory         "/var/named";
  statistics-file   "/var/named/data/named_stats.txt";

  recursion         yes;
  dnssec-enable     yes;
  dnssec-validation yes;

  pid-file          "/run/named/named.pid";
  session-keyfile   "/run/named/session.key";
};

logging {
  channel default_debug {
    file "data/named.run";
    severity dynamic;
  };
};

zone "example.com" IN { // file in /var/named dir, primary 
  type master;
  file "example.com.zone";
  allow-transfer { 192.168.0.2; };
};

zone "example.com" { # slave
  type slave;
  file "slaves/example.com.zone";
  masters { 192.168.0.1; };
};

zone "1.0.10.in-addr.arpa" IN {
  type master;
  file "example.com.rr.zone";
  allow-update { none; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```


### zone file ###

```
rhel:~ # vi /var/named/example.com.zone
$ORIGIN example.com.
$TTL 86400
@         IN  SOA  dns1.example.com.  hostmaster.example.com. (
              2001062501  ; serial
              21600       ; refresh after 6 hours
              3600        ; retry after 1 hour
              604800      ; expire after 1 week
              86400 )     ; minimum TTL of 1 day
;
;
          IN  NS     dns1.example.com.
          IN  NS     dns2.example.com.
dns1      IN  A      10.0.1.1
          IN  AAAA   aaaa:bbbb::1
dns2      IN  A      10.0.1.2
          IN  AAAA   aaaa:bbbb::2
;
;
@         IN  MX     10  mail.example.com.
          IN  MX     20  mail2.example.com.
mail      IN  A      10.0.1.5
          IN  AAAA   aaaa:bbbb::5
mail2     IN  A      10.0.1.6
          IN  AAAA   aaaa:bbbb::6
;
;
; This sample zone file illustrates sharing the same IP addresses
; for multiple services:
;
services  IN  A      10.0.1.10
          IN  AAAA   aaaa:bbbb::10
          IN  A      10.0.1.11
          IN  AAAA   aaaa:bbbb::11

ftp       IN  CNAME  services.example.com.
www       IN  CNAME  services.example.com.
;
;

rhel:~ # vi /var/named/example.com.rr.zone
$ORIGIN 1.0.10.in-addr.arpa.
$TTL 86400
@  IN  SOA  dns1.example.com.  hostmaster.example.com. (
       2001062501  ; serial
       21600       ; refresh after 6 hours
       3600        ; retry after 1 hour
       604800      ; expire after 1 week
       86400 )     ; minimum TTL of 1 day
;
@  IN  NS   dns1.example.com.
;
1  IN  PTR  dns1.example.com.
2  IN  PTR  dns2.example.com.
;
5  IN  PTR  server1.example.com.
6  IN  PTR  server2.example.com.
;
3  IN  PTR  ftp.example.com.
4  IN  PTR  ftp.example.com.
```


## rndc ##

/etc/rndc.conf

/etc/rndc.key


```
rhel:~ # chmod o-rwx /etc/rndc.key
rhel:~ # rndc status
```


### reload configuration and zone ###

```
rhel:~ # rndc reload # reload configuration and zones
rhel:~ # rndc reload localhost # reload single zone (zone name: localhost)
rhel:~ # rndc reconfig # reload configuration and newly added zones

rhel:~ # rndc freeze localhost
rhel:~ # rndc thaw localhost
```


### update zone key ###

```
rhel:~ # vi /etc/named.conf
...
zone "localhost" IN {
  type master;
  file "named.localhost";
  allow-update { none; };
  auto-dnssec maintain; # add auto-dnssec keyword
};
...

rhel:~ # rndc sign localhost # udpate zone key

rhel:~ # rndc validation on
rhel:~ # rndc validation off
rhel:~ # rndc querylog
```


## dig ##

```
rhel:~ # dig example.com NS
rhel:~ # dig example.com A
rhel:~ # dig -x 192.0.32.10
```