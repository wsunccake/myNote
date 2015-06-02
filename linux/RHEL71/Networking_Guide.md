
| NetworkManager		| The default networking daemon		|
| --------------------- | --------------------------------- |
| nmtui					| tui for NetworkManager			|
| nmcli					| cli with NetworkManager			|
| control-center		| gui by the GNOME Shell			|
| nm-connection-editor	| gui by A GTK+ 3 application		|

/etc/sysconfig/network-scripts/ifcfg-xxx
/etc/NetworkManage


	rhel:~ # yum install NetworkManager
	rhel:~ # systemctl status NetworkManager
	rhel:~ # systemctl start NetworkManager
	rhel:~ # systemctl enable NetworkManager


`nmtui`

	rhel:~ # yum install NetworkManager-tui
	rhel:~ # nmtui
	rhel:~ # nmtui edit connection-name
	rhel:~ # nmtui connect connection-name


`nmcli`

	rhel:~ # ip -V
	rhel:~ # nmcli help
	rhel:~ # nmcli general help
	rhel:~ # nmcli device status
	rhel:~ # nmcli device show
	rhel:~ # nmcli device show ifname eth0

	rhel:~ # nmcli connection up eth0
	rhel:~ # nmcli connection down eth0

	rhel:~ # nmcli general status
	rhel:~ # nmcli connection show
	rhel:~ # nmcli connection show --active


`static ip`

	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet ip4 10.0.0.11/24 gw4 10.0.0.1 # create /etc/sysconfig/network-script/ifcfg-eth0
	rhel:~ # nmcli connection modify eth0 ipv4.dns 8.8.8.8


`dhcp`

	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet # create /etc/sysconfig/network-script/ifcfg-eth0
	rhel:~ # nmcli connection modify eth0 ipv4.dhcp-hostname host-name
	rhel:~ # nmcli connection modify eth0 ipv4.ignore-auto-dns yes

`delete`

	rhel:~ # nmcli connection delete eth0 # delete /etc/sysconfig/network-script/ifcfg-eth0

nmcli connection reload
nmcli con load /etc/sysconfig/network-scripts/ifcfg-ifname
nmcli dev disconnect interface-name
nmcli con up interface-name


vi /etc/sysconfig/network-script/ifcfg-interface
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