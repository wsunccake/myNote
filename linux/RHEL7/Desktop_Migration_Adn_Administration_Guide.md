# GNOME 3 #

![GNOME 3](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Desktop_Migration_and_Administration_Guide/images/gnome3-classic2.png)

## GNOME Shell ##

	glxinfo | grep renderer

### systemd-logind ###

systemd-logind 用來替代 ConsoleKit, 來追蹤使用者登入情形

	loginctl list-sessions
	loginctl list-seats
	loginctl seat-status [<seat>]
	loginctl attach seat <device>

Ref:

[Session-Management on Linux](https://dvdhrm.wordpress.com/2013/08/24/session-management-on-linux/)


## GNOME Classic ##


## GSettings and Dconf ##

dconf-editor 是以 GUI 方式設定

	rhel:~ # yum install dconf-editor
	rhel:~ # dconf-editor

![dconf-editor](https://access.redhat.com/documentation/zh-CN/Red_Hat_Enterprise_Linux/7/html/Desktop_Migration_and_Administration_Guide/images/dconf-editor-screenshot.png)


$DCONF_PROFILE

/etc/dconf/profile/


	rhel:~ # cat /etc/dconf/profile/user 
	user-db:user          # ~/.config/dconf/user
	system-db:local       # /etc/dconf/db/local
	system-db:site        # /etc/dconf/db/site
	system-db:distro      # /etc/dconf/db/distro


gconftool-2 tool has been replaced by gsettings and dconf

gconf-editor has been replaced by dconf-editor


### PolicyKit ###

/etc/polkit-1/rules.d/50-default.rules

	pkcheck

## GVFS ##
## GTK+ ##

# GDM #

/etc/gdm/custom.conf