# DHCP #


## configuration ##

	rhel:~ # yum install dhcp

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

	rhel:~ # systemctl enable dhcpd.service
	rhel:~ # systemctl start dhcpd.service

