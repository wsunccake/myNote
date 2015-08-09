製作 USB 開機 

	rhel:~ # dd if=rhel-server-7.1x86_64-boot.iso of=/dev/sdb bs=512k # usb flash 為 sdb

Mac osx 指令同上
windows 使用 Fedora LiveUSB Creator 程式


網路安裝
	1. NFS
	2. HTTP
	3. FTP

	1. NFS
	yum install nfs-utils
	cp -r /mnt/rhel7-install /image/path
	cat /etc/exports
	/image/path  *(ro)

	systemctl start nfs-server.service
	systemctl reload nfs-server.service
	systemctl enable nfs-server.service

	showmount -e localhost
	mount localhost:/image/path /mnt

	2. HTTP
	yum install http
	cp -r /mnt/rhel7-install /var/www/html/image/path
	cat /etc/httpd/conf/httpd.conf
	systemctl start httpd.service
	systemctl enable httpd.service

	3. FTP
	yum install vsftpd
	cp -r /mnt/rhel7-install /var/ftp/image/path
	cat /etc
	# systemctl start vsftpd.service

	NFS			2049, 111, 20048
	HTTP		80
	HTTPS		443
	FTP			21

忘記 root password
	在 grub2 的 kerenl 後面加上 init=/bin/sh

	sh-4.2# mount -oremount,rw /
	sh-4.2# mount -oremount,rw /proc
	sh-4.2# password
	sh-4.2# touch /.autorelabel # 因為 selinux 關係, 之後要多重開機一次
	sh-4.2# sync
	sh-4.2# /sbin/reboot -f


停用 Network Manager (NM), 改用傳統 network daemon

	rhel:~ # systemctl list-units | grep -i network # 找尋 NM 和 network

	# 停用 NM
	rhel:~ # systemctl disable NetworkManager.service
	rhel:~ # systemctl enable NetworkManager.service
	rhel:~ # systemctl stop NetworkManager.service
	rhel:~ # systemctl start NetworkManager.service
	rhel:~ # systemctl status NetworkManager.service

	journalctl -xn

	rhel:~ # cat /etc/sysconfig/network-script/ifcfg-enxxxx # 新增 / 修改 以下兩設定
	NM_CONTROLLED=no # 停用 NM
	ONBOOT=yes # 開機時自動啟動

	# 啟動 network
	rhel:~ # systemctl enable network
	rhel:~ # systemctl start network
	rhel:~ # systemctl status network

	# Runlevel
	rhel:~ # ls /etc/systemd/system
	rhel:~ # systemctl get-default
	rhel:~ # systemctl set-default graphical.target
	rhel:~ # systemctl isolate multi-user.target

	#
	rhel:~ # systemctl -a # 看全部 (包括被disable)
	ls /usr/lib/systemd/system
	/usr/lib/systemd/system
	rhel:~ # systemctl list-units
	rhel:~ # systemctl list-sockets
	rhel:~ # systemctl show network.service

將 iso image 加入 repository

	mount -oloop rhel71.iso /mnt
	cp /mnt/media.repo /etc/yum.repos.d
	echo "baseurl=file:///mnt" >> /etc/yum.repos.d/media.repo # for iso
	echo "baseurl=ftp://ip/" >> /etc/yum.repos.d/media.repo # for ftp
	yum repolist


	yum update
	yum grouplist
	yum group install "Server with GUI"



	hwinfo --disk
	lspci -v
	lshw -class disk

create repository server
	mkdir -p /var/ftp/pub/rhel-server
	cp -rf /mnt/rhel-server/* /var/ftp/pub/rhel-server
	mount -oloop rhel-server-7.1-x86_64-dvd.iso /var/ftp/pub/rhel-server

	yum install -y createrepo
	createrepo /var/ftp/pub/rhel-server

	yum install -y vsftpd
	cat /etc/vsftpd/vsftpd.conf 
	systemctl enable vsftpd
	systemctl start vsftpd.target


w3m
	# basic
	U		open URL
	B		上一頁
	H		說明
	q		離開
	# page
	ctrl^v	page down
	b		page up
	# link
	[		first link
	]		last link
	tab		next link
	ctl^u	prev link
	# menu
	s		selection menu
	o		option menu