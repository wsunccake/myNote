### HOW TO UPGRADE FROM RED HAT ENTERPRISE LINUX 6 ###

step
1. Check your support status
2. Prepare your system for upgrade
	* Back up all data
	* Test first
	* Convert to Red Hat Subscription Management
	* Ensure only supported package groups are installed
	* Update all packages
3. Check system upgrade suitability
	* Preupgrade Assistant (preupg)
4. Upgrade your system


`Install Preupgrade Asstant`

```
rhel:~ # cat /etc/redhat-release
rhel:~ # yum upgrade -y
rhel:~ # reboot
rhel:~ # redhat-upgrade-tool --device /dev/sdb --addrepo optional=http://hostname/path/to/repo

rhel:~ # subscription-manager repos --enable rhel-6-server-extras-rpms
rhel:~ # subscription-manager repos --enable rhel-6-server-optional-rpms
rhel:~ # rhn-channel --add --channel rhel-x86_64-server-extras-6
rhel:~ # yum -y install preupgrade-assistant preupgrade-assistant-ui preupgrade-assistant-contents
```


`Run the Preupgrade Assistant`

	rhel:~ # preupg -y
	rhel:~ # preupg -y -u http://hostname:port/submit


`Run the Preupgrade Assistant Web UI`

	rhel:~ # cd /etc/httpd/conf.d
	rhel:~ # mv 99-preup-httpd.conf 99-preup-httpd.conf.private
	rhel:~ # cp 99-preup-httpd.conf.public 99-preup-httpd.conf
	rhel:~ # setenforce 0
	rhel:~ # iptables -I INPUT -m state --state NEW -p tcp --dport 8099 -j ACCEPT
	rhel:~ # service httpd restart

使用瀏覽器開啟 http://192.168.99.1:8099 (default port: 8099/tcp)

`Upgrade system`

	rhel:~ # yum -y install redhat-upgrade-tool
	rhel:~ # yum -y install yum-utils
	rhel:~ # yum-config-manager --disable
	rhel:~ # redhat-upgrade-tool --network 7.0 --instrepo repo_location
	rhel:~ # redhat-upgrade-tool --device device_path
	rhel:~ # redhat-upgrade-tool --iso iso_path
	cat /etc/redhat-release
	yum repolist
	yum upgrade -y


`Setup Subscription Manager`

	rhel:~ # subscription-manager remove --all
	rhel:~ # subscription-manager unregister
	rhel:~ # subscription-manager register
	rhel:~ # subscription-manager attach --pool=poolID
	rhel:~ # subscription-manager repos --enable=repoID




* Boot Loader
	GRUB -> GRUB2
* Init System
	SysV init system -> systemd
* Installer
	Anaconda
* firstboot Implementation
	firstboot -> initial-setup
* mount behavior at boot
/dev/critical     /critical   xfs   defaults          1  2
/dev/optional     /optional   xfs   defaults,nofail   1  2

					-> udevd

In this example, the device mounted at /optional would not cause boot to fail if it could not be mounted successfully.

### File System Layout ###

`/bin, /sbin, /lib and /lib64 directory`

/bin		->		/usr/bin
/sbin		->		/usr/sbin
/lib		->		/usr/lib
/lib64		->		/usr/lib64


`/run directory`

/var/run	->		/run
/var/lock	->		/run/lock


`/tmp directory`

	rhel:~ # systemctl enable tmp.mount
	rhel:~ # systemctl disable tmp.mount
	rhel:~ # /etc/tmpfiles.d # man tmpfiles.d


	tmpfs /tmp tmpfs size=2G,nr_inodes=20k,defaults,noatime,mode=1777 0 0


### SYSTEM MANAGEMENT ###


`Default process maximums`

	cat /etc/security/limits.d/20-nproc.conf


`Logging Framework`

	/run/log/journal


/etc/sysconfig/i18n 		->		/etc/locale.conf
									/etc/vconsole.conf

/etc/sysconfig/network		->		/etc/hostname

/cgroup						->		/sys/fs/cgroup

XFS		user_xattr and acl
Btrfs	
LVM

```
rhel:~ # systemd-cgls
rhel:~ # systemd-cgtop
```


### Networking ###
NetworkManager
system-config-network-tui -> nmcli
netcat -> ncat
Postfix		2.6 -> 2.10
NFS			4.1, 4, 3
Apache		2.4
	/var/cache/mod_proxy	->		/var/cache/httpd
	/var/www				->		/usr/share/httpd
	/var/www/icons			->		/usr/share/httpd/icons
	/var/www/manual			->		/usr/share/httpd/manual
	/var/www/error			->		/usr/share/httpd/error
	/var/log/httpd/suexec.log
	/usr/sbin/apxs to /usr/bin/apxs.

Samba		4
BIND
	bind-chroot				->		named-chroot


### Desktop ###
GNOME 3
KDE Plasma


### Cluster And HA ###
Luci		->		pcs
Piranha		->		Keepalived
rgmanager	->		pacemaker
cman		->		corosync
qdiskd		->		votequorum