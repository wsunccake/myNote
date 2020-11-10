# DHCP #


## Package ##

	rhel:~ # yum install dhcp


## Configuration ##

	rhel:~ # cp /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example /etc/dhcp/dhcpd.conf
	rhel:~ # cat /etc/dhcp/dhcpd.conf
	option domain-name "devops.com";        # 設定 domain name
	option domain-name-servers 192.168.0.1; # 設定 DNS 
	option routers 192.168.0.1;             # 設定 router/gateway
	filename "pxelinux.0";                  # 設定 pxe boot loader 
	next-server 192.168.0.1;                # 設定 tftp
	subnet 192.168.0.0 netmask 255.255.255.0 {
	  range 192.168.0.150 192.168.0.180;
	  host host1 {
	    hardware ethernet 11:22:33:44:55:66;
	    fixed-address 192.168.0.111;
	  }
	}

	rhel~: # cat /usr/lib/systemd/system/dhcpd.service 
	[Unit]
	Description=DHCPv4 Server Daemon
	Documentation=man:dhcpd(8) man:dhcpd.conf(5)
	Wants=network-online.target
	After=network-online.target
	After=time-sync.target

	[Service]
	Type=notify
	ExecStart=/usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid eth1   # 指定派 IP 的 NIC

	[Install]
	WantedBy=multi-user.target


## Service ##

	rhel:~ # systemctl enable dhcpd.service
	rhel:~ # systemctl start dhcpd.service
	rhel:~ # systemctl status dhcpd.service

	rhel:~ # netstat -lnutp | grep -E "67|68"   # dhcpd 使用 67 port, dhclient 使用 68 port