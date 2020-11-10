## 製作 USB 開機 

```bash
# usb flash 為 sdb
rhel:~ # dd if=rhel-server-7.1x86_64-boot.iso of=/dev/sdb bs=512k
```

Mac osx 指令同上

windows 使用 Fedora LiveUSB Creator 程式


---

## 網路安裝

1. NFS

```bash
cenots:~ # yum install nfs-utils
cenots:~ # cp -r /mnt/rhel7-install /image/path
cenots:~ # cat /etc/exports
cenots:~ # /image/path  *(ro)

cenots:~ # systemctl start nfs-server.service
cenots:~ # systemctl reload nfs-server.service
cenots:~ # systemctl enable nfs-server.service

cenots:~ # showmount -e localhost
cenots:~ # mount localhost:/image/path /mnt
```
	

2. HTTP

```bash
centos:~ # yum install http
centos:~ # cp -r /mnt/rhel7-install /var/www/html/image/path
centos:~ # cat /etc/httpd/conf/httpd.conf
centos:~ # systemctl start httpd.service
centos:~ # systemctl enable httpd.service
```


3. FTP

```bash
centos:~ # yum install vsftpd
centos:~ # cp -r /mnt/rhel7-install /var/ftp/image/path
centos:~ # cat /etc
centos:~ # systemctl start vsftpd.service
```

port

| protocol | port             |
| -------- | ---------------- |
| NFS      | 2049, 111, 20048 |
| HTTP     | 80               |
| HTTPS    | 443              |
| FTP      | 21               |


---

## 忘記 root password

在 grub2 的 kerenl 後面加上 init=/bin/sh

```sh
sh-4.2# mount -oremount,rw /
sh-4.2# mount -oremount,rw /proc
sh-4.2# password
sh-4.2# touch /.autorelabel # 因為 selinux 關係, 之後要多重開機一次
sh-4.2# sync
sh-4.2# /sbin/reboot -f
```


---

## 安裝 grub

```sh
sh-4.2# mount /dev/sda1 /mnt
sh-4.2# mount -obind /dev/ /mnt/dev/
sh-4.2# chroot /mnt/
sh-4.2# grub

grub> root (hd0, 1)
grub> setup (hd0)
```

(hd0, 1) 是包含 /boot 的 partition


---

## 安裝 grub2

```sh
sh-4.2# mount /dev/sda1 /mnt
sh-4.2# mount -obind /dev/ /mnt/dev/
sh-4.2# chroot /mnt/
sh-4.2# grub2-install --root-directory=/mnt /dev/sda
```


---

## 停用 Network Manager (NM), 改用傳統 network daemon

```bash
rhel:~ # systemctl list-units | grep -i network # 找尋 NM 和 network

# 停用 NM
rhel:~ # systemctl disable NetworkManager.service
rhel:~ # systemctl enable NetworkManager.service
rhel:~ # systemctl stop NetworkManager.service
rhel:~ # systemctl start NetworkManager.service
rhel:~ # systemctl status NetworkManager.service

# 若有錯誤訊息, 可以查看
rhel:~ # journalctl -xn 

rhel:~ # cat /etc/sysconfig/network-script/ifcfg-enxxxx # 新增 / 修改 以下兩設定
NM_CONTROLLED=no # 停用 NM
ONBOOT=yes       # 開機時自動啟動

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
rhel:~ # ls /usr/lib/systemd/system
rhel:~ # /usr/lib/systemd/system
rhel:~ # systemctl list-units
rhel:~ # systemctl list-sockets
rhel:~ # systemctl show network.service
```

---

## 將 iso image 加入 repository

```bash
centos:~ # mount -oloop rhel71.iso /mnt
centos:~ # cp /mnt/media.repo /etc/yum.repos.d
centos:~ # echo "baseurl=file:///mnt" >> /etc/yum.repos.d/media.repo # for iso
centos:~ # echo "baseurl=ftp://ip/" >> /etc/yum.repos.d/media.repo   # for ftp
centos:~ # yum repolist

centos:~ # yum update
centos:~ # yum grouplist
centos:~ # yum group install "Server with GUI"

centos:~ # hwinfo --disk
centos:~ # lspci -v
centos:~ # lshw -class disk
```


---

## create repository server

```bash
rhel:~ # mkdir -p /var/ftp/pub/rhel-server
rhel:~ # cp -rf /mnt/rhel-server/* /var/ftp/pub/rhel-server
rhel:~ # mount -oloop rhel-server-7.1-x86_64-dvd.iso /var/ftp/pub/rhel-server

rhel:~ # yum install -y createrepo
rhel:~ # createrepo /var/ftp/pub/rhel-server

rhel:~ # yum install -y vsftpd
rhel:~ # cat /etc/vsftpd/vsftpd.conf 
rhel:~ # systemctl enable vsftpd
rhel:~ # systemctl start vsftpd.target
```


---

## w3m 操作

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


---

# 掛載 exfat

```bash
centos:~ # yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-releas
e-7.noarch.rpm
centos:~ # yum install fuse-exfat

# sdb1 為 exfat 格式硬碟
centos:~ # mount /deb/sdb1 /mnt
```
