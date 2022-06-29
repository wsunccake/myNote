# VMWare Tools

```
# require gcc
debian8:~ # apt-get install gcc

# install vmware-tools
debian8:~ # mount /dev/cdrom /mnt
debian8:~ # tar zxf /mnt/VMwareTools-10.0.10-4301679.tar.gz -C /tmp
debian8:~ # /tmp/vmware-tools-distrib/vmware-install.pl

# show vmware shared folder
debian8:~ # vmware-hgfsclient
```


# dpkg

```
rpm -ivh <pkg>.rpm     dpkg -i <pkg>.dev
rpm -e <pkg>           dpkg -r <pkg>, dpkg -P <pkg>
rpm -qa                dpkg -l
rpm -ql <pkg>          dpkg -L <pkg>
rpm -qf <file>         dpkg -S <file>
rpm -qip <pkg>.rpm     dpkg -l <pkg>.deb
rpm -qlp <pkg>.rpm     dpkg -c <pkg>.deb
rpm -qiR <pkg>         dpkg -s <pkg>, dpkg -p <pkg>
```


# apt

## config

```
debian8:~ # cat /etc/apt/sources.list
# deb cdrom:[Debian GNU/Linux 8.7.1 _Jessie_ - Official amd64 DVD Binary-1 20170116-11:01]/ jessie contrib main
deb http://ftp.debian.org/debian/ jessie-updates main contrib
deb-src http://ftp.debian.org/debian/ jessie-updates main contrib


# add iso to cdrom
debian8:~ # mount -oloop -t iso9660 debian-8.7.1-amd64-DVD-1.iso /media/dvd1
debian8:~ # apt-cdrom -m -d /media/dvd1 add
debian8:~ # cat /etc/apt/sources.list
deb cdrom:[Debian GNU/Linux 8.7.1 _Jessie_ - Official amd64 DVD Binary-1 20170116-11:01]/ jessie contrib main
->
deb file:///media/dvd1 jessie contrib main
```

## apt-get

```
debian8:~ # apt-get update
debian8:~ # apt-get install <pkg>
debian8:~ # apt-get remove <pkg>

# upgrade
debian8:~ # apt-get upgrade
debian8:~ # apt-get dist-upgrade

# clean download deb in /var/cache/apt/archives
debina8:~ # apt-get download <pkg>
debina8:~ # apt-get clean
debina8:~ # apt-get autoclean
```


## apt-cache

```
# search package
debian8:~ # apt-cache search <pkg>
debian8:~ # apt-cache pkgnames <pkg>

# info package
debian8:~ # apt-cache show <pkg>
debian8:~ # apt-cache showpkg <pkg>
debian8:~ # apt-cache depends <pkg>
debian8:~ # apt-cache madison <pkg>

debina8:~ # apt-cache policy
debina8:~ # apt-cache dumpavail
```

## apt

```
debian8:~ # apt update
debian8:~ # apt install <pkg>
debian8:~ # apt remove <pkg>

debian8:~ # apt install <pkg1> <pkg2>-  # 安裝 <pkg1>, 移除 <pkg2>
debian8:~ # apt remove <pkg1> <pkg2>    # 移除 <pkg1>, 安裝 <pkg2>
```


## apt-key

```
debian8:~ # apt-key list
debian8:~ # apt-key finger
debian8:~ # apt-key add <file>
debian8:~ # apt-key del <keyid>
```


# aptitude

```
debian8:~ # aptitude install <pkg>
debian8:~ # aptitude remove <pkg>
debian8:~ # aptitude purge <pkg>
debian8:~ # aptitude search <str>
debian8:~ # aptitude show <pkg>
debian8:~ # aptitude update
debian8:~ # aptitude upgrade
debian8:~ # aptitude dist-upgrade
debian8:~ # aptitude 
```


# tasksel

```
debian8:~ # tasksel --list-tasks
debian8:~ # tasksel install desktop
```



# dpkg-reconfigure

```
debian8:~ # dpkg-query -l

debian8:~ # dpkg-reconfigure <pkg>
debian8:~ # dpkg-reconfigure locales  # /etc/default/ 
debian8:~ # dpkg-reconfigure tzdata

debian8:~ # debconf-show <pkg>
debian8:~ # debconf-show locales
```
