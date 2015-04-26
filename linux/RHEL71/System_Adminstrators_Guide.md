
### localectl ###

	rhel:~ # localectl status
	rhel:~ # localectl help

	rhel:~ # system enable systemd-localed
	rhel:~ # system start systemd-localed


`System Locale`

	# setup
	rhel:~ # localectl list-locales
	rhel:~ # localectl set-locale LANG=zh_TW.utf8

	# config file
	rhel:~ # cat /etc/locale.conf
	LANG=en_US.utf8
	LC_MESSAGES=C

	# other method
	rhel:~ # locale
	rhel:~ # locale --all


`Keyboard Layout`

	# setup
	rhel:~ # localectl list-keymaps
	rhel:~ # localectl set-keymap us
	rhel:~ # localectl set-x11-keymap de

	# config file
	rhel:~ # /etc/vconsole.conf
	KEYMAP="us"
	FONT="latarcyrheb-sun16"

	rhel:~ # ls /lib/kbd/keymaps
	rhel:~ # loadkeys -d



### timedatectl ###

`Date And Time`

	rhel:~ # timedatectl status
	rhel:~ # timedatectl help

	rhel:~ # systemctl enable systemd-timedated
	rhel:~ # systemctl enable chronyd

	rhel:~ # timedatectl set-time HH:MM:SS # 24 小時制
	rhel:~ # timedatectl list-timezones
	rhel:~ # timedatectl set-timezone Asia/Taipei
	rhel:~ # timedatectl set-ntp yes # 會使用 NTP server 更新


	rhel:~ # ls /usr/share/zoneinfo
	rhel:~ # ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime
	rhel:~ # export TZ=Asia/Taipei


`date`

	rhel:~ # date -s HH:MM:SS
	rhel:~ # date -s YYYY-MM-DD
	rhel:~ # date -s YYYY-MM-DD HH:MM:SS


`hwclock`

	rhel:~ # hwclock -w
	rhel:~ # hwclock -s


### User And Group ###


uid (user ID), gid (group ID) 系統預設起始值在 /etc/login.defs
shell 系統預設可使用值 /etc/shells
至於 useradd 設定值在 /etc/default/useradd


`User`

	rhel:~ # useradd user # 新增使用者
	rhel:~ # useradd -u uid -g gid user # 新增使用者, 且指定 uid, gid
	rhel:~ # useradd -N -G group1,group2 user # 將 user 加入到 group1, group2, ... 但沒有 upg
	rhel:~ # useradd -e YYYY-MM-DD user # 帳號過期 YYYY-MM-DD (-1: 永不過期)
	rhel:~ # useradd -f DD user # DD 日後要改密碼 (0: 馬上過期, -1: 永不過期)
	rhel:~ # useradd -s /sbin/nologin -r sysuser # 新增系統使用者, 禁止使用者登入

	rhel:~ # usermod -G group user # user 加入到 group, 原本的已加入的群組都會被移除
	rhel:~ # usermod -aG group user # user 加入到 group, 除了原本的群組之外還會多加 group


	rhel:~ # userdel user # 刪除使用者, 但會留下 HOME, MAIL_DIR
	rhel:~ # userdel -r user # 刪除使用者, 包括等 HOME, MAIL_DIR

	rhel:~ # passwd user # 設定 user 密碼 
	rhel:~ # chage -l user # 看帳號狀態


`Group`

	rhel:~ # groupadd group

	rhel:~ # gpasswd -a user group # user 加入 group
	rhel:~ # gpasswd -d user group # user 離開 group

	rhel:~ # rhel:~ # groupdel group


`設定群組`

	rhel:~ # mkdir /opt/myproject
	rhel:~ # groupadd myproject
	rhel:~ # chown root:myproject /opt/myproject
	rhel:~ # chmod 2775 /opt/myproject
	rhel:~ # ls -ld /opt/myproject
	rhel:~ # usermod -aG myproject username


`加入系統管理群組`

	rhel:~ # usermod -G wheel user
	rhel:~ # vi /etc/pam.d/su
	#auth           required        pam_wheel.so use_uid


`sudo`

/etc/sudoers
Defaults    timestamp_timeout=value
%users localhost=/sbin/shutdown -h now
juan ALL=(ALL) ALL


/etc/pam.d/system-auth
session required pam_tty_audit.so disable=pattern enable=pattern
session required pam_tty_audit.so disable=* enable=root

/var/log/messages
/var/log/secure


### YUM ###


`Repository`

	rhel:~ # yum repolist
	rhel:~ # yum repolist all
	rhel:~ # yum repolist -v
	rhel:~ # yum repoinfo


`Package`

	# search
	rhel:~ # yum search term
	rhel:~ # yum list all # show installed and available package
	rhel:~ # yum list glob_expression
	rhel:~ # yum list available glob_expression
	rhel:~ # yum list installed glob_expression
	rhel:~ # yum provides glob_expression

	rhel:~ # yum list *log*
	rhel:~ # yum provides "*bin/named"

	# info
	rhel:~ # yum info package_name
	rhel:~ # yumdb info package_name

	# install
	rhel:~ # yum install package_name
	rhel:~ # yum install glob_expression
	rhel:~ # yum install-n name
	rhel:~ # yum install-na name.architecture
	rhel:~ # yum install-nevra name-epoch:version-release.architecture
	rhel:~ # yum localinstall path

	rhel:~ # yum install audacious-plugins-\*
	rhel:~ # yum install /usr/sbin/named

	# remove
	rhel:~ # yum remove package_name

	# update
	rhel:~ # yum check-update
	rhel:~ # yum update package_name # update package
	rhel:~ # yum group update group_name
	rhel:~ # yum update # update all package

下載的 package 放在 /var/cache/yum/$basearch/$releasever/packages 目錄下


`Package Group`

	rhel:~ # yum group list glob_expression
	rhel:~ # yum group info glob_expression
	rhel:~ # yum group ids

	# install
	rhel:~ # yum group install "KDE Desktop"
	rhel:~ # yum group install kde-desktop
	rhel:~ # yum install @"KDE Desktop"
	rhel:~ # yum install @kde-desktop

	# remove
	rhel:~ # yum group remove "KDE Desktop"
	rhel:~ # yum group remove kde-desktop
	rhel:~ # yum remove @"KDE Desktop"
	rhel:~ # yum remove @kde-desktop


`History`

	rhel:~ # yum history list
	rhel:~ # yum history list all
	rhel:~ # yum history list 1..3

	rhel:~ # yum history summary
	rhel:~ # yum history summary 1..3
	rhel:~ # yum history summary glob_expression

	rhel:~ # yum history info 1
	rhel:~ # yum history info 1..3

	rhel:~ # yum history package-list glob_expression

	rhel:~ # yum history undo id
	rhel:~ # yum history redo id

	rhel:~ # yum history new

YUM 使用 SQLite 存放在 /var/lib/yum/history/ 目錄下



`[main]`

	rhel:~ # cat /etc/yum.conf
	[main]
	cachedir=/var/cache/yum/$basearch/$releasever
	keepcache=0
	debuglevel=2
	logfile=/var/log/yum.log
	exactarch=1
	obsoletes=1
	gpgcheck=1
	plugins=1
	installonly_limit=3



`[repository]`

	rhel:~ # cat /etc/yum.repo.d/example.repo
	[InstallMedia]
	baseurl=file:///mnt/rhel-server
	name=Red Hat Enterprise Linux 7.1
	mediaid=1424360759.989976
	metadata_expire=-1
	gpgcheck=0
	cost=500



`Config`

	rhel:~ # yum-config-manager
	rhel:~ # yum-config-manager section
	rhel:~ # yum-config-manager glob_expression…

	rhel:~ # yum-config-manager --add-repo repository_url
	rhel:~ # yum-config-manager --add-repo http://www.example.com/example.repo


	rhel:~ # yum-config-manager --enable repository
	rhel:~ # yum-config-manager --enable glob_expression
	rhel:~ # yum-config-manager --disable repository
	rhel:~ # yum-config-manager --disable glob_expression


`Create Yum Repository`

	rhel:~ # yum install createrepo
	rhel:~ # createrepo --database /mnt/local_repo



### Systemd ###

| Unit Type			| File Extension	| Description															|
| ----------------- | ----------------- | --------------------------------------------------------------------- |
| Service unit		| .service			| system service														|
| Target unit		| .target			| group of systemd units												|
| Automount unit	| .automount		| file system automount point											|
| Device unit		| .device			| device file recognized by the kernel									|
| Mount unit		| .mount			| file system mount point												|
| Path unit			| .path				| file or directory in a file system									|
| Scope unit		| .scope			| externally created process											|
| Slice unit		| .slice			| group of hierarchically organized units that manage system processes	|
| Snapshot unit		| .snapshot			| saved state of the systemd manager									|
| Socket unit		| .socket			| inter-process communication socket									|
| Swap unit			| .swap				| swap device or a swap file											|
| Timer unit		| .timer			| systemd timer															|


Directory					Description
/usr/lib/systemd/system/	Systemd units distributed with installed RPM packages.
/run/systemd/system/		Systemd units created at run time. This directory takes precedence over the directory with installed service units.
/etc/systemd/system/		Systemd units created and managed by the system administrator. This directory takes precedence over the directory with runtime units.

`service `

| service					| systemctl									|
| ------------------------- | ----------------------------------------- |
| service name start		| systemctl start name.service				|
| service name stop			| systemctl stop name.service				|
| service name restart		| systemctl restart name.service			|
| service name condrestart	| systemctl try-restart name.service		|
| service name reload		| systemctl reload name.service				|
| service name status		| systemctl status name.service				|
| service --status-all		| systemctl list-units --type service --all	|


`chkconfig`

| chkconfig					| systemctl									|
| ------------------------- | ----------------------------------------- |
| chkconfig name on			| systemctl enable name.service				|
| chkconfig name off		| systemctl disable name.service			|
| chkconfig --list name		| systemctl status name.service				|
| chkconfig --list			| systemctl list-unit-files --type service	|


	# chkconfig off
	rhel:~ # systemctl mask name.service
	rhel:~ # systemctl disable name.service

	# chkconfig on
	rhel:~ # systemctl umask name.service
	rhel:~ # systemctl enable name.service

enable/disable create/remove soft link
mask/umask link to /dev/null


`Runlevel`

| Runlevel	| Target Units							|
| --------- | ------------------------------------- |
| 0			| runlevel0.target, poweroff.target		|
| 1			| runlevel1.target, rescue.target		|
| 2			| runlevel2.target, multi-user.target	|
| 3			| runlevel3.target, multi-user.target	|
| 4			| runlevel4.target, multi-user.target	|
| 5			| runlevel5.target, graphical.target	|
| 6			| runlevel6.target, reboot.target		|

SysV	LSB
runlevel			systemctl list-units --type target
telinit runlevel	systemctl isolate name.target

systemctl get-default
systemctl set-default graphical.target
systemctl isolate multi-user.target
systemctl rescue
systemctl --no-wall rescue
systemctl emergency
systemctl --no-wall emergency


`Power Management`

| Old Command		| New Command			|
| ----------------- | --------------------- |
| halt				| systemctl halt		|
| poweroff			| systemctl poweroff	|
| reboot			| systemctl reboot		|
| pm-suspend		| systemctl suspend		|
| pm-hibernate		| systemctl hibernate	|
| pm-suspend-hybrid	| systemctl hybrid-sleep|


`Remote Machine`

	rhel:~ # systemctl -H root@server-01.example.com status httpd.service


`System Unit File`

a


### Subscription Manager ###

	# setup subscription manager
	subscription-manager register
	subscription-manager list --available
	subscription-manager attach --pool=pool_id
	subscription-manager list --consumed
	subscription-manager register --auto-attach

	# software repository
	subscription-manager repos --list
	rhel-variant-rhscl-version-rpms
	rhel-variant-rhscl-version-debug-rpms
	rhel-variant-rhscl-version-source-rpms

	rhel-server-rhscl-7-eus-rpms
	rhel-server-rhscl-7-eus-source-rpms
	rhel-server-rhscl-7-eus-debug-rpms

	subscription-manager repos --enable repository
	subscription-manager repos --disable repository

	# remove subscription
	subscription-manager remove --serial=serial_number
	subscription-manager remove --all


### Red Hat Support Tool ###

	yum install redhat-support-tool
	redhat-support-tool config user username
	redhat-support-tool config password
	redhat-support-tool




access control lists (ACLs)
user private group (UPG)


/etc/group
/etc/passwd
/etc/shadow
/etc/login.defs

gpasswd
useradd/usermod command with the -e, --expiredate or -f, --inactive



