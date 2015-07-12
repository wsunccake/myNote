### RedHat Networking  ###

| NetworkManager		| The default networking daemon		|
| --------------------- | --------------------------------- |
| nmtui					| tui for NetworkManager			|
| nmcli					| cli with NetworkManager			|
| control-center		| gui by the GNOME Shell			|
| nm-connection-editor	| gui by A GTK+ 3 application		|

/etc/sysconfig/network-scripts/ifcfg-xxx
/etc/NetworkManager


	rhel:~ # yum install NetworkManager
	rhel:~ # systemctl status NetworkManager
	rhel:~ # systemctl start NetworkManager
	rhel:~ # systemctl enable NetworkManager


`nmtui`

	rhel:~ # yum install NetworkManager-tui
	rhel:~ # nmtui
	rhel:~ # nmtui edit con-name
	rhel:~ # nmtui connect con-name


`nmcli`

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

	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet # create /etc/sysconfig/network-script/ifcfg-ifname
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

/usr/share/doc/initscripts-version/sysconfig.txt

| ifcfg command 				 | nmcli command 				 |
| ------------------------------ | ----------------------------- |
| /etc/init.d/network restart 	 | 	nmcli connection reload 	 |
| ifup eth0 					 | 	nmcli connection up eth0 	 |
| ifdown eth0 					 | 	nmcli connection down eth0 	 |


### Networking IP ###

`static ip`

	# method 1:
	rhel:~ # nmtui

	# method 2:
	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet ip4 10.0.0.11/24 gw4 10.0.0.1
	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet ip4 10.0.0.11/24 gw4 10.0.0.1 ip6 abbe::cafe gw6 2001:db8::1 # 可同時設定 IPv4, IPv6
	rhel:~ # nmcli connection modify eth0 ipv4.dns 8.8.8.8
	rhel:~ # nmcli connection modify eth0 "8.8.8.8 8.8.4.4" # 可同時設定多組 DNS
	rhel:~ # nmcli connection modify eth0 +ipv4.dns "8.8.8.8 8.8.4.4"

IPv6 方式跟 IPv4 一樣, 將 ipv4 改成 ipv6 即可


`dhcp`

	# method 1:
	rhel:~ # nmtui

	# method 2:
	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet
	rhel:~ # nmcli connection modify eth0 ipv4.dhcp-hostname host-name
	rhel:~ # nmcli connection modify eth0 ipv4.ignore-auto-dns yes


`wifi`

	rhel:~ # nmcli dev wifi list
	rhel:~ # nmcli con add con-name MyCafe ifname wlan0 type wifi ssid MyCafe ip4 192.168.100.101/24 gw4 192.168.100.1
	rhel:~ # nmcli con modify MyCafe wifi-sec.key-mgmt wpa-psk # 設定連線加密方式
	rhel:~ # nmcli con modify MyCafe wifi-sec.psk caffeine # 設定 WPA2 password 為 caffeine
	rhel:~ # nmcli radio wifi on
	rhel:~ # nmcli radio wifi off


`Static Network Settings`

	rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ifname
	DEVICE=eth0
	BOOTPROTO=none
	ONBOOT=yes
	PREFIX=24
	IPADDR=10.0.1.27


`Dynamic Network Settings`

	rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ifname
	DEVICE=em1
	BOOTPROTO=dhcp
	ONBOOT=yes

	DHCP_HOSTNAME=hostname # 不使用 DHCP 所派的 hostname
	PEERDNS=no # 不使用 DHCP 預設的 DNS
	DNS1=ip-address # 當 PEERDNS=no, 才能另外指定 DNS1
	DNS2=ip-address


`multiple NIC`

	rhel:~ # cat /etc/sysconfig/network-script/ifcfg-ifname
	HWADDR=11:22:33:44:55:66
	TYPE=Ethernet
	BOOTPROTO=dhcp # dhcp
	DEFROUTE=yes # 設定為 default gateway, multiple NIC 環境中很重要
	PEERDNS=yes
	PEERROUTES=yes
	IPV4\_FAILURE_FATAL=no
	IPV6INIT=yes
	IPV6_AUTOCONF=yes
	IPV6_DEFROUTE=yes
	IPV6_PEERDNS=yes
	IPV6_PEERROUTES=yes
	IPV6\_FAILURE_FATAL=no
	NAME="eth0"
	ONBOOT=yes # 開機使否開啟
	NM_CONTROLLED=yes # 可否由 Network Manager


`ip command`

	ip link show  # 顯示網卡狀態
	ip link set dev eth0 up # 開啟網卡
	ip link set dev eth0 down # 關閉網卡

	ip addr show # 顯示網卡 IP
	ip addr add 10.0.0.3/24 dev eth0 # 新增網卡 IP
	ip addr del 10.0.0.3/24 dev eth0 # 刪除網卡 IP

	ip route # 顯示路由
	ip route add default via 10.0.3.254 dev eth0 # 新增預設路由
	ip route del default via 10.0.3.254 dev eth0 # 刪除預設路由
	ip route add via 192.168.0.254 dev eth1 # 新增路由
	ip route del via 192.168.0.254 dev eth1 # 刪除路由


`GUI`

	rhel:~ # gnome-control-center network


`VPN`

	rhel:~ # yum install NetworkManager-libreswan
	rhel:~ # yum install NetworkManager-libreswan-gnome

Bond
Bridge
VLAN


### Hostname ###

`config file`

/etc/hostname


`daemon`

	rhel:~ # systemctl restart systemd-hostnamed


`command`

	# using hostnamectl setup hostname
	rhel:~ # hostnamectl status
	rhel:~ # hostnamectl set-hostname name # setup hostname
	rhel:~ # hostnamectl set-hostname "" # empty hostname
	rhel:~ # hostnamectl set-hostname -H [username]@hostname # setup remote hostname

	# using nmcli setyo hostname
	rhel:~ # nmcli general hostname
	rhel:~ # nmcli general hostname my-server


### Networking Bond ###

`bond`

	# method 1:
	rhel:~ # nmtui

	# method 2:
	rhel:~ # nmcli connection add type bond ifname bond0 cos-name bond0
	rhel:~ # nmcli connection edit bond0
	nmcli> describe bond.options
	nmcli> set bond.options mode=active-backup
	nmcli> save
	nmcli> quit

	rhel:~ # nmcli connection add type bond ifname eth0 con-name eth0 master bond0
	rhel:~ # nmcli connection add type bond ifname eth1 con-name eth1 master bond0

	# method 3:
	rhel:~ # modprobe bonding
	rhel:~ # modinfo bonding
	rhel:~ # echo +bond0 >> /sys/class/net/bond_masters
	rhel:~ # ip link set dev bond0 up
	rhel:~ # ifenslave bond0 eth0 eth1

	# un bonding
	rhel:~ # ifenslave -d bond0 eth0 eth1
	rhel:~ # ip link set dev bond0 down
	rhel:~ # echo -bond0 >> /sys/class/net/bond_masters

	# bond option
	rhel:~ # echo 1000 > /sys/class/net/bond0/bonding/miimon
	rhel:~ # echo 6 > /sys/class/net/bond0/bonding/mode
	rhel:~ # echo balance-alb > /sys/class/net/bond0/bonding/mode

	# check miimon
	rhel:~ # ethtool interface_name | grep "Link detected:"


`config file`

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


`GUI`

	rhel:~ # gnome-control-center network


### Networking Team ###