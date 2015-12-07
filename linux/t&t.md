# Tip and Troubleshoot #

## System ##

### Common ###

#### 忘記 root 密碼 ####

在 grub2 的 kerenl 後面加上 init=/bin/sh

	sh-4.2# mount -oremount,rw /
	sh-4.2# mount -oremount,rw /proc
	sh-4.2# password
	sh-4.2# touch /.autorelabel       # 因為 selinux 關係, 所以須使用次步驟, 之後要多重開機一次; 若無 selinux 可略過次步驟
	sh-4.2# sync
	sh-4.2# /sbin/reboot -f


### CPU ###

### Memory ###

### HD ###


#### 清除 MBR ####

	Linux:~ # dd if=/dev/zero of=/dev/sda bs=512 count=1


### CD/DVD ###

#### 掛載 image/iso ####

	Linux:~ # mount -oloop image.iso /mnt


#### 光碟燒錄 ####

wodim -> cdrecord (symbol link)

	Linux:~ # wodim -v -dao dev=/dev/cdrw image.iso


#### 建立 image/iso ####

genisoimage -> mkisofs (symbol  link)

	Linux:~ # genisoimage -r -joliet-long -V "cd_name" -o image.iso dir


### Other ###


## Network ##


## Service ##