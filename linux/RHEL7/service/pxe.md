# PXE #


## Pacakge ##

TFTP, DHCP, DNS, DNSMASQ: TFTP, DHCP 是必備, 至於 DNS 可選, 但一般都會跟 DHCP 一起使用. 另一種是使用 DNSMASQ

HTTP, NFS, FTP: 三種選一種

	rhel:~ # yum install syslinux
	rhel:~ # yum install tftp-server dhcp bind # install TFTP, DHCP, DNS
	rhel:~ # yum install httpd  # install HTTP


## Configuration ##


### TFTP ###

	rhel:~ # vi /etc/xinetd.d/tftp
	        disable         = no
	        disable         = yes
	rhel:~ # systemctl restart xinetd
	rhel:~ # systemctl enable tftp.service
	rhel:~ # systemctl start tftp.service

	# setup pxe boot loader
	rhel:~ # cp /usr/share/syslinux/{pxelinux.0,menu.c32,memdisk,mboot.c32,chain.c32} /var/lib/tftpboot
	rhel:~ # mkdir -p /var/lib/tftpboot/pxelinux.cfg
	rhel:~ # vi /var/lib/tftpboot/pxelinux.cfg/default

	# setup centos image boot loader
	rhel:~ # mount -o loop CentOS-6.7-x86_64-minimal.iso /mnt
	rhel:~ # mkdir -p /var/lib/tftpboot/centos67
	rhel:~ # cp /mnt/isolinux/{vmlinuz,initrd.img} /var/lib/tftpboot/centos67


### DHCP ###

	RHEL:~ # vi /etc/dhcp/dhcpd.conf


### HTTP ###


### DNSMASQ ###