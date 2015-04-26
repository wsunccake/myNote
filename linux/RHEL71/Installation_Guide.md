### Boot and Installation Media ###

| Architecture							| Minimal boot image					| Full installation image			|
| ------------------------------------- | ------------------------------------- | -------------------------------	|
| AMD64 and Intel 64					| rhel-variant-7.1-x86_64-boot.iso		| rhel-variant-7.1-x86_64-dvd.iso	|
| IBM Power Systems (big endian)		| rhel-variant-7.1-ppc64-boot.iso		| rhel-variant-7.1-ppc64-dvd.iso	|
| IBM Power Systems (little endian)		| rhel-variant-7.1-ppc64le-boot.iso		| rhel-variant-7.1-ppc64le-dvd.iso	|
| IBM System z							| Not available							| rhel-variant-7.1-s390x-dvd.iso	|

* Red Hat Atomic Cloud Image					qcow2
* Red Hat Atomic Image for RHEV					ova
* Red Hat Atomic Image for vSphere				ova
* Red Hat Atomic Image for Microsoft Hyper-V	vhd
* Red Hat Atomic Installer						iso


### Download Image ###

	# download image
	rhel:~ # curl 'https://access.cdn.redhat.com//content/origin/files/sha256/85/85a...46c/rhel-server-7.0-x86_64-dvd.iso?_auth_=141...963' -o rhel-server-7.0-x86_64-dvd.iso

	# check md5
	rhel:~ # sha256sum rhel-server-7.0-x86_64-dvd.iso


### Making Installation USB Media ###

	# Linux
	rhel:~ # dd if=/home/testuser/Downloads/rhel-server-7.1x86_64-boot.iso of=/dev/sdb bs=512k	# sdb 是 USB flash

	# Windows
	使用 Fedora LiveUSB Creator

	# Mac OS X
	方式同 Linux



### Installation Source ###

1. DVD: binary DVD ISO image onto a DVD
2. Hard drive: binary DVD ISO image on a hard drive
3. Network location: binary DVD ISO image or the installation tree to a accessible network location. network protocols:
	* NFS: The binary DVD ISO image is placed into a Network File System (NFS) share.
	* HTTPS, HTTP or FTP: The installation tree is placed on a network location accessible over HTTP, HTTPS, or FTP.

`NFS`

	server:~ # yum install nfs-utils
	server:~ # vi /etc/exports		# man exports
	/rhel-server 192.168.0.0/24(ro)
	server:~ # cp -r /mnt/rhel-server /rhel-server

	# nfs-server daemon
	server:~ # systemctl enable nfs-server
	server:~ # systemctl start nfs-server

	# firewall
	server:~ # firewall-cmd --permanent --zone=public --add-service=nfs
	server:~ # firewall-cmd --reload
	server:~ # firewall-cmd --list-all

	# check NFS
	server:~ # showmout -e localhost

`HTTP`

	server:~ # yum install httpd
	server:~ # systemctl enable httpd
	server:~ # systemctl start httpd
	server:~ # vi /etc/httpd/conf/httpd.conf
	server:~ # cp -r /mnt/rhel-server /var/www/html

	# firewall
	server:~ # firewall-cmd --permanent --zone=public --add-service=http
	server:~ # firewall-cmd --reload
	server:~ # firewall-cmd --list-all

	# check HTTP
	server:~ # w3m localhost/rhel-server

`FTP`

	server:~ # yum install vsftpd
	systemctl enable vsftpd
	systemctl start vsftpd
	vi /etc/vsftpd/vsftpd.conf		# man vsftpd.conf
	# default anonymous dir(anon_root): /var/ftp, 
	server:~ # cp -r /mnt/rhel-server /var/ftp/pub

	# check FTP
	server:~ # ftp localhost

| Protocol used	| Ports to open		|
| ------------- | ----------------- |
| NFS			| 111, 2049, 20048	|
| HTTP			| 80				|
| HTTPS			| 443				|
| FTP			| 21				|


### Disk Space And Memory Requirements ###

* HDD minimum 10 GB
* RAM minimum 1 GB (Red Hat Enterprise Linux Atomic Host)
* RAM minimum 2 GB (bare metal)


### Installation Boot Method ###

Full installation DVD or USB drive
Minimal boot CD, DVD or USB Flash Drive
PXE Server


### Automating Installation ###

Kickstart


### Anaconda ###

* main installation interface
* Ctrl+Alt+F1: text mode installation
* Ctrl+Alt+F6: graphical installation 
* Shift+Print Screen: /tmp/anaconda-screenshots


`tmux Windows`

| Shortcut	| Contents										|
| --------- | --------------------------------------------- |
| Ctrl+b 1	| Main installation program window				|
| Ctrl+b 2	| Interactive shell prompt with root privileges	|
| Ctrl+b 3	| Installation log (/tmp/anaconda.log)			|
| Ctrl+b 4	| Storage log (/tmp/storage.log)				|
| Ctrl+b 5	| Program log (/tmp/program.log)				|


* installation in text mode

在開機時 grub menu 時, 加上 inst.text  或 inst.xdriver=vesa 選項即可


* installation in graphic user interface

無論是圖形介面或文字介面安裝, 要透過網路安裝, 須先設定好網路 (Networking settings), 然後選定安裝來源 (Installation source), 最後才可安裝軟體 (Software Selection)


1. Date & Time
2. Language Support
3. Keyboard
4. Installation Source
5. Network & Hostname
6. Software Selection
7 Installation Destination
	* MBR if the size of the disk is less than 2 TB
	* GPT if the size of the disk is more than 2 TB
	UEFI systems
	Only GPT is allowed on UEFI systems.  /boot/efi partition should be at least 50 MB, recommended size is 200 MB


### Device Types ###

1. standard partition
2. logical volume (LVM)
3. LVM thin provisioning
4. BTRFS
5. software RAID


### File Systems ###

1. xfs: XFS partition is maximum 500 TB
2. ext4: ext4 partition is maximum 50 TB
3. ext3
4. ext2: ext2 assign long file names, up to 255 characters
5. swap
6. vfat
7. BIOS Boot: GPT on a BIOS system
8. EFI System Partition: GPT on a UEFI system


### RAID levels ###

1. RAID0 - Optimized performance (stripe)
2. RAID1 - Redundancy (mirror)
3. RAID4 - Error detection (parity)
4. RAID5 - Distributed error detection
5. RAID6 - Redundant
6. RAID10 - Redundancy (mirror) and Optimized performance (stripe)


### Size Policy ###

1. Automatic
2. As large as possible
3. Fixed


`Partitioning Scheme`

| parition	| size					|
| --------- | --------------------- |
| /boot		| \> 500 MB				|
| / (root)	| \> 10 GB (min. 5GB)	|
| /home		| \> 1 GB				|
| swap		| \> 1 GB				|

* Note

1. /boot don't support LVM, Btrfs
2. /usr don't suppprt Btrfs
3. / (root) partition > 2 TB and (U)EFI. /boot partition < 2 TB to boot.


`Recommended System Swap Space`

| Amount of RAM		| Recommended			| Hibernation					|
| ------------------| ----------------------| ----------------------------- |
| < 2 GB			| 2 x RAM				| 3 x RAM						|
| 2 GB - 8 GB		| ~ RAM					| 2 x RAM						|
| 8 GB - 64 GB		| 0.5 x RAM				| 1.5 x RAM						|
| \> 64 GB			| workload dependent	| hibernation not recommended	|



### Storage Devices ###

Multipath Devices
Other SAN Devices
	iSCSI Target
	FCoE SAN
Firmware RAID


`iSCSI`

	server:~ # yum install targetcli
	server:~ # systemctl enable target
	server:~ # systemctl start target
	server:~ # dd if=/dev/zero of=/tmp/iscsi.img count=10 bs=1G
	server:~ # targetcli ls
	/> cd /backstores/fileio 
	/backstores/fileio> create file1 /home/iscsi.img
	/backstores/fileio> cd /iscsi
	/iscsi> create
	/iscsi> ls
	/iscsi> cd iqn.xxx/tpg1
	/iscsi/iqn....xxx/tpg1> set attribute authentication=0
	/iscsi/iqn....xxx/tpg1> set attribute generate_node_acls=1
	/iscsi/iqn....xxx/tpg1> luns/ create /backstores/fileio/file1
	/iscsi/iqn....xxx/tpg1> cd /
	/> saveconfig
	/> exit

	# check iSCSI
	server:~ # iscsiadm -m discovery -p 127.0.0.1 -t st
	server:~ # iscsiadm -m node -p 127.0.0.1 -T iqn.... -l
	server:~ # lsblk


### Installation Log File ###

| Log file				| Contents											|
| --------------------- | ------------------------------------------------- |
| /tmp/anaconda.log		| general Anaconda messages							|
| /tmp/program.log		| all external programs run during the installation	|
| /tmp/storage.log		| extensive storage module information				|
| /tmp/packaging.log	| yum and rpm package installation messages			|
| /tmp/syslog			| hardware-related system messages					|


`Transfer Log Files Onto a USB Drive`


	rhel:~ # mkdir usb
	rhel:~ # mount /dev/sdb1 /mnt/usb # 假設 usb flash 為 sdb1
	rhel:~ # cp /tmp/*log /mnt/usb
	rhel:~ # umount /mnt/usb


`Transfer Log Files OVer network`

	rhel:~ # cd /tmp
	rhel:~ # scp *log john@192.168.0.122:/home/john/logs/


| option						| description			|
| ----------------------------- | --------------------- |
| inst.xdriver=vesa				| text mode				|
| inst.xdriver=nouveau			| video driver			|
| inst.resolution=1024x768		| display resolution	|
| inst.text console=boot		| serial mode			|
| inst.graphical				| GUI					|
| inst.vnc						| vnc					|
| inst.vncpassword=PASSWORD		| vnc password			|
| inst.rescue					| rescue mode			|

inst.repo 指定安裝來源
inst.stage2 指定 install image 的位置, 語法同上
inst.dd 指定額外驅動程式
inst.ks 指定 kickstart 檔案
modprobe.blacklist

inst.repo=cdrom
inst.repo=http://ip/dir
inst.repo=ftp://user@password/ip/dir
inst.repo=nfs:ip/dir


### PXE Installation ###

`tftp`

`DHCP`


BOID and UEFI 安裝差異

`UEFI`

	Shell> map
	Shell> fs0:
	fs0:\EFI\redhat\grubx64.efi


### VNC Installation ###

### Kickstart Installation ###



%packages、%pre 與 %post 等三節必須以 %end

yum install pykickstart
ksvalidator /path/to/kickstart.ks


### Forget root password ###
init=/bin/sh

sh-4.2# /usr/sbin/load_policy -i
sh-4.2# mount -o remount,rw /
sh-4.2# passwd root
sh-4.2# mount -o remount,ro /
