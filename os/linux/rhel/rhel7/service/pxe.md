# PXE #


## Pacakge ##

TFTP, DHCP, DNS, DNSMASQ: TFTP, DHCP 是必備, 至於 DNS 可選, 但一般都會跟 DHCP 一起使用. 另一種是使用 DNSMASQ

HTTP, NFS, FTP: 三種選一種

	rhel:~ # yum install syslinux
	rhel:~ # yum install tftp-server dhcp bind # install TFTP, DHCP, DNS
	rhel:~ # yum install httpd                 # install HTTP


## Configuration ##


### TFTP ###

	rhel:~ # vi /etc/xinetd.d/tftp
	#        disable         = no
	        disable         = yes           # 啟用 tftp
	rhel:~ # systemctl restart xinetd
	rhel:~ # systemctl enable tftp.service
	rhel:~ # systemctl start tftp.service

	# setup pxe boot loader
	rhel:~ # cp /usr/share/syslinux/{pxelinux.0,menu.c32,memdisk,mboot.c32,chain.c32} /var/lib/tftpboot
	rhel:~ # mkdir -p /var/lib/tftpboot/pxelinux.cfg

	# default pxe config
	rhel:~ # vi /var/lib/tftpboot/pxelinux.cfg/default
	DEFAULT local disk

	LABEL local disk
	localboot 0x80

	LABLE rhel 7.1
	kernel vmlinuz
	append initrd=initrd.img

	# specific mac pxe config
	rhel:~ # vi /var/lib/tftpboot/pxelinux.cfg/01-11-22-33-aa-bb-cc           # 指定 11:22:33:aa:bb:cc 網卡使用該設定
	DEFAULT SZ

	LABEL SZ
	kernel http://<ip>/vmlinuz
	append initrd=http://<ip>/sz-installer.img stage2=initrd:

	# setup centos image boot loader
	rhel:~ # mount -o loop CentOS-6.7-x86_64-minimal.iso /mnt
	rhel:~ # mkdir -p /var/lib/tftpboot/centos67
	rhel:~ # cp /mnt/isolinux/{vmlinuz,initrd.img} /var/lib/tftpboot/centos67


### DHCP ###

	rhel:~ # systemctl enable dhcpd.service
	rhel:~ # systemctl start dhcpd.service
	rhel:~ # systemctl status dhcpd.service

	RHEL:~ # vi /etc/dhcp/dhcpd.conf


### DNS ###

	rhel:~ # vi /var/named/dynamic/db.test.com
	$TTL 10800
	@ IN SOA master.test.com. root.test.com. (
	        1       ;Serial
	        86400   ;Refresh
	        3600    ;Retry
	        604800  ;Expire
	        3600    ;Negative caching TTL
	)
	
	@ IN NS master.test.com.
	
	master.test.com. IN A 192.168.10.11

	rhel:~ # vi db.100.168.192.in-addr.arpa
	$TTL 10800
	@ IN SOA master.test.com. root.100.168.192.in-addr.arpa. (
	        1       ;Serial
	        86400   ;Refresh
	        3600    ;Retry
	        604800  ;Expire
	        3600    ;Negative caching TTL
	)
	
	@ IN NS master.test.com.

	11   PTR   master.test.com


### HTTP ###

	# setup httpd (apache):
	rhel:~ # systemctl enable httpd.service
	rhel:~ # systemctl start httpd.service
	rhel:~ # systemctl status httpd.service

	# copy centos 7 install package
	rhel:~ # mkdir -p /var/www/html/centos7/x86_64
	rhel:~ # mount -oloop CentOS-7-x86_64-DVD-1503-01.iso /mnt/
	rhel:~ # cp -r /mnt /var/www/html/centos7/x86_64/


### DNSMASQ ###