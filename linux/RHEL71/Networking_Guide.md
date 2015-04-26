
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

	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet ip4 10.0.0.11/24 gw4 10.0.0.1
	rhel:~ # nmcli connection modify eth0 ipv4.dns 8.8.8.8


`dhcp`

	rhel:~ # nmcli connection add ifname eth0 con-name eth0 type ethernet
	rhel:~ # nmcli connection modify eth0 ipv4.dhcp-hostname host-name
	rhel:~ # nmcli connection modify eth0 ipv4.ignore-auto-dns yes



nmcli connection reload
nmcli con load /etc/sysconfig/network-scripts/ifcfg-ifname
nmcli dev disconnect interface-name
nmcli con up interface-name
