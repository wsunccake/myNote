# iptables #


## Package ##

	rhel:~ # yum install iptables


## Configuration ##

	rhel:~ # ls /usr/lib/systemd/system/iptables.service

	rhel:~ # cat /etc/sysconfig/iptables
	*filter
	:INPUT ACCEPT [0:0]
	:FORWARD ACCEPT [0:0]
	:OUTPUT ACCEPT [0:0]
	COMMIT

	*nat
	:PREROUTING ACCEPT [0:0]
	:INPUT ACCEPT [0:0]
	:OUTPUT ACCEPT [0:0]
	:POSTROUTING ACCEPT [0:0]
	-A POSTROUTING -j MASQUERADE
	COMMIT


## Serivce ##

	rhel:~ # systemctl start iptables.service
	rhel:~ # systemctl enable iptables.service
	rhel:~ # systemctl status iptables.service

	rhel:~ # iptables -S
	rhel:~ # iptables -L -nv
