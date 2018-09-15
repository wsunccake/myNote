`ls`

	freebsd:~ $ ls -G # 顏色

### System administration ###

一般使用者要有管理者權限, 將使用者帳號加入到 wheel 群組裡, 之後該使用者就可以使用 su 指令切換成 root

	freebsd:~ $ grep wheel /etc/group
	wheel:*:0:root,user
	freebsd:~ $ su -

	freebsd:~ # bsdconfig

	freebsd:~ # ls /etc/rc.d
	freebsd:~ # service start|stop|status|reload daemon

	/etc/rc.d/service-name {start} {stop} {status} {reload} {forceXXX} {rcvar}



-----------------------------

### Package ###

Ports：這是在安裝FreeBSD時，FreeBSD小組先將軟體的路徑與安裝方法整理，提供使用者安裝。
Package：聞名的RedHat有發展出一套RPM，在FreeBSD上就是Package了。
make：顧名思議，拿到軟體的原始碼之後，直接編釋安裝

Ports最大的缺點就是訊息無法即時更新，所以如果套件以經有新版的研發出來了，用Ports只能裝研發小組在FreeBSD推出時所有的最新套件，也就是你可能無法使用最新的套件，不過這當然不是沒有辦法處理的，Package就是因應這件事出來的。


#### ports ####

Ports Collection
/usr/ports

	freebsd:~ # cd /usr/ports
	freebsd:~ # make update
	freebsd:/usr/ports # make fetchindex

	freebsd:/usr/ports # make search name=pkg
	freebsd:/usr/ports # make quicksearch name=pkg

	freebsd://usr/ports # cd /usr/ports/ports-mgmt/pkg
	freebsd:/usr/ports/ports-mgmt/pkg # make
	freebsd:/usr/ports/ports-mgmt/pkg # make install

	freebsd:/usr/ports/ports-mgmt/pkg # make deinstall


#### packages ####

	freebsd:~ # pkg help
	freebsd:~ # pkg help info

	freebsd:~ # pkg info -a # list all installed package
	freebsd:~ # pkg info pkg # list package information
	freebsd:~ # pkg info -f pkg # list package file

	freebsd:~ # pkg update
	freebsd:~ # pkg search pkg
	freebsd:~ # pkg install pkg
	freebsd:~ # pkg delete pkg


-----------------------------

### X window ###

	freebsd:~ # pkg install xorg
	freebsd:~ # pkg install dbus
	freebsd:~ # pkg install hal

	freebsd:~ # pkg info xorg-server | grep HAL
	freebsd:~ # vi /etc/rc.conf
	freebsd:~ # hald_enable="YES"
	freebsd:~ # dbus_enable="YES"
	freebsd:~ # service hald start
	freebsd:~ # service dbus start

	freebsd:~ # mv /etc/X11/xorg.conf ~/xorg.conf.etc
	freebsd:~ # mv /usr/local/etc/X11/xorg.conf ~/xorg.conf.localetc

	freebsd:~ # startx


-----------------------------

### Desktop Environment ###


#### Xfce ####

	freebsd:~ # pkg install xfce

	freebsd:~ $ echo "exec /usr/local/bin/startxfce4" > ~/.xinitrc
	freebsd:~ $ echo "#!/bin/sh" > ~/.xsession
	freebsd:~ $ echo "exec /usr/local/bin/startxfce4" >> ~/.xsession
	freebsd:~ $ chmod +x ~/.xsession


-----------------------------

### Reference ###

[FreeBSD 使用手冊](https://www.freebsd.org/doc/zh_TW/books/handbook/)

[FreeBSD Handbook](https://www.freebsd.org/doc/handbook/index.html)

[Frequently Asked Questions for FreeBSD 8.X, 9.X and 10.X](https://www.freebsd.org/doc/en_US.ISO8859-1/books/faq/index.html)