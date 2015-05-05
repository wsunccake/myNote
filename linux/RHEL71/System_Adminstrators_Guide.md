
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



### OpenSSH ###

`System-wide configuration files`

* /etc/ssh/ssh\_config
* /etc/ssh/sshd\_config
* /etc/ssh/moduli
* /etc/ssh/ssh\_host_ecdsa_key
* /etc/ssh/ssh\_host_ecdsa_key.pub
* /etc/ssh/ssh\_host_key
* /etc/ssh/ssh\_host_key.pub
* /etc/ssh/ssh\_host_rsa_key
* /etc/ssh/ssh\_host_rsa_key.pub
* /etc/pam.d/sshd
* /etc/sysconfig/sshd


`User-specific configuration files`

* ~/.ssh/known\_hosts
* ~/.ssh/authorized\_keys
* ~/.ssh/id\_ecdsa
* ~/.ssh/id\_ecdsa.pub
* ~/.ssh/id\_rsa
* ~/.ssh/id\_rsa.pub
* ~/.ssh/identity
* ~/.ssh/identity.pub


`Starting an OpenSSH Server`

	rhel:~ # systemctl start sshd.service
	rhel:~ # systemctl stop sshd.service
	rhel:~ # systemctl enable sshd.service


`Using Key-based Authentication`

	rhel:~ # vi /etc/ssh/sshd_config
	PasswordAuthentication no


`Generating Key Pairs`

	rhel:~ # ssh-keygen -t rsa
	rhel:~ # ssh-copy-id [-i ~/.ssh/id_rsa.pub] user@hostname


`Configuring ssh-agent`

	rhel:~ # ssh-add
	rhel:~ # ssh-agent
	rhel:~ # ssh-agent -k


`Utility`

	rhel:~ # ssh [username@]hostname
	rhel:~ # ssh [username@]hostname command

	rhel:~ # ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key.pub
	rhel:~ # ssh-keygen -R penguin.example.com


	rhel:~ # scp localfile [username@]hostname:remotefile
	rhel:~ # scp [username@]hostname:remotefile localfile

	rhel:~ # sftp [username@]hostname


`X11 Forwarding`

	rhel:~ # ssh -Y username@hostname


`Port Forwarding`

In\_Host(9000)   ----|--->   Out\_Host(2000)

	In_Host:~ $ ssh -L 9000:localhost:2000 Out_Host


In\_Host(9000)   <---|----   Out\_Host(2000)

	In_Host:~ $ ssh -R 9000:localhost:2000 Out_Host



### VNC ###


`Starting VNC Server`

	rhel:~ # yum install tigervnc-server
	rhel:~ # cp /lib/systemd/system/vncserver@.service /etc/systemd/system/.
	rhel:~ # vi /etc/systemd/system/vncserver@.service
	ExecStart=/sbin/runuser -l USER -c "/usr/bin/vncserver %i -geometry 1280x1024"
	PIDFile=/home/USER/.vnc/%H%i.pid

	rhel:~ # systemctl start vncserver@:display_number.service
	rhel:~ # systemctl enable vncserver@:display_number.service
	rhel:~ # systemctl disable vncserver@:display_number.service
	rhel:~ # systemctl stop vncserver@:display_number.service

	rhel:~ # firewall-cmd --list-all
	rhel:~ # firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.122.116" service name=vnc-server accept'
	rhel:~ # firewall-cmd --zone=public --add-port=5904/tcp

	rhel:~ # systemctl daemon-reload
	rhel:~ # su - USER
	rhel:~ # vncpasswd


`Configuring VNC Server for Two Users`

	rhel:~ # systemctl start vncserver-USER_1@:3.service
	rhel:~ # systemctl start vncserver-USER_2@:5.service


`Starting VNC Client`

	rhel:~ # yum install tigervnc
	rhel:~ # vncviewer address:display_number
	rhel:~ # vncviewer -via user@host:display_number # by ssh


### HTTP ###

/etc/httpd/conf/httpd.conf
/etc/httpd/conf.modules.d/
/etc/httpd/conf.d/autoindex.conf	# new
/etc/httpd/conf.d/userdir.conf		# new
/etc/httpd/conf.d/welcome.conf		# new


httpd 2.2								->		httpd 2.4

/usr/sbin/apxs 							->		/usr/bin/apxs

mod\_auth\_mysql, mod\_auth\_pgsql		->		mod\_authn\_dbd
mod\_ldap, mod\_perl					->		mod\_proxy\_html, mod\_xml2enc

/var/cache/mod_proxy/					->		/var/cache/httpd/
/var/www/icons/							->		/usr/share/httpd/icons
/var/www/manual/						->		/usr/share/httpd/manual/
/var/www/error/							->		/usr/share/httpd/error/
/var/log/httpd/suexec.log				->		/var/log/secure

service httpd graceful					->		apachectl graceful
service httpd configtest				->		apachectl configtest


	rhel:~ # yum install httpd

	rhel:~ # systemctl start httpd.service
	rhel:~ # systemctl enable httpd.service
	rhel:~ # systemctl stop httpd.service
	rhel:~ # systemctl disable httpd.service
	rhel:~ # systemctl restart httpd.service

	rhel:~ # systemctl reload httpd.service
	rhel:~ # apachectl graceful

	rhel:~ # systemctl is-active httpd.service

	rhel:~ # apachectl configtest

	rhel:~ # firewall-cmd --add-service http
	rhel:~ # firewall-cmd --add-service https


`Modules`

/usr/lib/httpd/modules/
/usr/lib64/httpd/modules/


	rhel:~ # cat /etc/httpd/conf.modules.d/xxx.conf
	LoadModule ssl\_module modules/mod\xxx.so

	rhel:~ # yum install httpd-devel
	rhel:~ # apxs -i -a -c module_name.c


`Virtual Hosts`

	rhel:~ # cp /usr/share/doc/httpd-X.Y.Z/httpd-vhosts.conf /etc/httpd/conf.d/


`SSL Server`

SSL/TLS over HTTP, referred to as HTTPS

	rhel:~ # yum install mod_ssl openssl

	rhel:~ # vi /etc/httpd/conf.d/ssl.conf
	SSLProtocol all -SSLv2 # disable SSL v2
	SSLProtocol -all +TLSv1 +TLSv1.1 +TLSv1.2 # enable TLS

	rhel:~ # systemctl restart httpd

	rhel:~ # openssl s_client -connect hostname:port -protocol
	rhel:~ # openssl s_client -connect localhost:443 -ssl3
	rhel:~ # openssl s_client -connect localhost:443 -tls1_2


`NSS`

	rhel:~ # yum remove mod_ssl
	rhel:~ # yum install mod_nss
	rhel:~ # vi /etc/httpd/conf.d/nss.conf
	Listen 443
	VirtualHost _default_:443
	NSSCertificateDatabase /etc/httpd/alias
	NSSPassPhraseDialog file:/etc/httpd/password.conf
	NSSNickname Server-Cert

	rhel:~ # chmod 640 /etc/httpd/password.conf
	rhel:~ # chown root:apache /etc/httpd/password.conf
	rhel:~ # vi /etc/httpd/password.conf
	internal:password

	rhel:~ # certutil -L -d /etc/httpd/alias # list NSS db
	rhel:~ # certutil -W -d /etc/httpd/alias # set password
	rhel:~ # certutil -d /etc/httpd/nss-db-directory/ -A -n "CA_certificate" -t CT,, -a -i certificate.pem


`NSS with/without SSL/TLS`

	rhel:~ # vi /etc/httpd/conf.d/nss.conf
	NSSProtocol TLSv1.0,TLSv1.1

	rhel:~ # openssl s_client -connect localhost:443 -ssl3
	rhel:~ # openssl s_client -connect localhost:443 -tls1


`Generating a New Key and Certificate`


	# method 1:
	rhel:~ # yum install crypto-utils

	rhel:~ # rm /etc/pki/tls/private/hostname.key
	rhel:~ # genkey hostname # 會替換掉 /etc/pki/tls/private/hostname.key, 所以要先刪除

	# method 2:
	rhel:~ # openssl genrsa 1024 > hostname.key
	rhel:~ # openssl req -new -key hostname.key -out hostname.csr
	rhel:~ # openssl req -x509 -key hostname.key -in hostname.csr > hostname.crt
	rhel:~ # openssl req -noout -text -in hostname.csr # verify csr

	# method 3:
	rhel:~ # openssl req -x509 -new -set_serial number -key hostname.key -out hostname.crt


	rhel:~ # vi /etc/httpd/conf.d/ssl.conf
	SSLCertificateFile /etc/pki/tls/certs/hostname.crt
	SSLCertificateKeyFile /etc/pki/tls/private/hostname.key


### MAIL ###

Mail Transport Protocols: SMTP/Simple Mail Transfer Protocol
Mail Access Protocols: POP/Post Office Protocol and IMAP/Internet Message Access Protocol
LMTP/Local Mail Transfer Protocol

`POP and IMAP`

APOP — POP3 with MD5 authentication.
KPOP — POP3 with Kerberos authentication.
RPOP — POP3 with RPOP authentication.


	rhel:~ # yum install dovecot

	rhel:~ # vi /etc/dovecot/dovecot.conf
	protocols = imap pop3 lmtp

	rhel:~ # systemctl restart dovecot
	rhel:~ # systemctl enable dovecot

	rhel:~ # vi /etc/dovecot/conf.d/10-ssl.conf
	ssl_protocols = !SSLv2 !SSLv3

	/etc/pki/dovecot/certs/dovecot.pem
	/etc/pki/dovecot/private/dovecot.pem


`MTA`

MTA/Mail Transport Agent (SMTP) (Postfix, Sendmail, and Fetchmail)
MDA/Mail Delivery Agent or LDA/Local Delivery Agent (SMTP, LMTP) (Postfix, Sendmail) (mail, procmail)
MUA/Mail User Agent (POP, IMAP)

	rhel:~ # alternatives --config mta
	rhel:~ # systemctl enable service
	rhel:~ # systemctl disable service


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



