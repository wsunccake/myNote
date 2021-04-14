# Bash and Bash Scripts


## What is “The Shell”

`BASH CONFIGURATION FILES FOR LOGIN SHELLS`

```
/etc/profile

/etc/profile.local

/etc/profile.d/

~/.profile
```


`BASH CONFIGURATION FILES FOR NON-LOGIN SHELLS`

```
/etc/bash.bashrc

/etc/bash.bashrc.local

~/.bashrc
```


`SPECIAL FILES FOR BASH`

```
~/.bash_history

~/.bash_logout

~/.alias
```


## Writing Shell Scripts


```bash
sle:~ $ vi hello.sh
#!/bin/sh 
echo "Hello World"

sle:~ $ chmod +x ./hello.sh
```


## Redirecting Command Events

```bash
sle:~ $ ls > listing.txt
sle:~ $ ls >> listing.txt
sle:~ $ read a < foo
sle:~ $ cat /proc/cpuinfo | grep cpu
sle:~ $ find / -name "foo*" 2>/dev/null
```


## Using Aliases

```bssh
sle:~ $ alias lt='ls -ltr'
```


## Using Variables in Bash

```bash
sle:~ $ printenv PATH
sle:~ $ echo $PATH
sle:~ $ PROJECT="SLED"
sle:~ $ export NAME="tux"
sle:~ $ unset NAME
```

`USEFUL ENVIRONMENT VARIABLES`

```
HOME

HOST

LANG

PATH

PS1

PS2

PWD

USER
```


## Using Argument Variables

```bash
sle:~ $ cat foo.sh
#!/bin/sh
echo \"$1\" \"$2\" \"$3\" \"$4\"

sle:~ $ foo.sh "Tux Penguin" 2000

# ${VAR#pattern}
sle:~ $ file=/home/tux/book/book.tar.bz2
sle:~ $ echo ${file#*/}

# ${VAR##pattern}
sle:~ $ file=/home/tux/book/book.tar.bz2
sle:~ $ echo ${file##*/}

# ${VAR%pattern}
sle:~ $ file=/home/tux/book/book.tar.bz2
sle:~ $ echo ${file%.*}

# ${VAR%%pattern}
sle:~ $ file=/home/tux/book/book.tar.bz2
sle:~ $ echo ${file%%.*}

# ${VAR/pattern_1/pattern_2}
sle:~ $ file=/home/tux/book/book.tar.bz2
sle:~ $ echo ${file/tux/wilber}
```


## Grouping and Combining Commands

```bash
# Command1 ; Command2
sle:~ $ cat filelist.txt ; ls -l filelist.txt

# Command1 && Command2
sle:~ $ cat filelist.txt && ls -l filelist.txt

# Command1 || Command2
sle:~ $ mkdir /home/tux/foo || mkdir /home/wilber/bar

# funcname(){ ... }
sle:~ $ hello() { echo "Hello $1"; }
sle:~ $ hello Tux
sle:~ $ Hello Tux
```


### Working with Common Flow Constructs

```bash
# if else fi
if test $USER = "tux"; then
  echo "Hello Tux."
else
  echo "You are not Tux."
fi

if test -e /tmp/foo.txt ; then
  echo "Found foo.txt"
fi

if [ -e /tmp/foo.txt ] ; then
  echo "Found foo.txt"
fi

# for do ... done
for i in *.png; do
 ls -l $i
done
```


---

# sudo Basics

## Basic sudo Usage

```bash
sle:~ $ id -un
sle:~ $ sudo id -un

# sudo -s (<command>)
sle:~ $ sudo -s

# sudo -i (<command>)
sle:~ $ sudo -i
```


## Configuring sudo

```bash
sle:~ # EDITOR=/usr/bin/nano visudo
sle:~ # EDITOR=/usr/bin/nano visudo -f /etc/sudoers.d/<user>
sle:~ # usermod -aG wheel <user>
```

```bash
sle:~ # cat /etc/sudoers

# enter the password of the target user
Defaults targetpw

# prompts for the root password
Defaults !rootpw

# constructs a minimal environment 
Defaults env_reset

# environment variables to keep when the env_reset on
Defaults env_keep = "EDITOR PROMPT"
Defaults env_keep += "JRE_HOME" # Add JRE_HOME

# environment variables to remove when the env_reset flag OFF
Defaults env_delete = "EDITOR PROMPT"
Defaults env_delete += "JRE_HOME" 


# Who      Where         As whom      Tag                What
# User_List Host_List = [(User_List)] [NOPASSWD:|PASSWD:] Cmnd_List
<user> ALL = PASSWD: /usr/bin/foo, NOPASSWD: /usr/bin/bar
# tux ALL = NOPASSWD: ALL
<user> ALL = /usr/bin/systemctl restart apache2
<user> ALL = (admin) /usr/bin/wall ""
```


### Using sudo with X.Org Applications

```bash
sle:~ $ sudo xterm

sle:~ $ xhost si:localuser:root   # allow the root user to access the local user's X session
sle:~ $ xhost -si:localuser:root  # removes the granted access
```


---

# YaST


---

# YaST in Text Mode


## YaST Command Line Options

```bash
sle:~ # yast -h
sle:~ # yast -i <package>  # install package

# module
sle:~ # yast -l                 # list module
sle:~ # yast <module>      # work moudle
sle:~ # yast <module> help
```


## YaST Command Line Options

```bash
# lan
sle:~ # yast lan help
sle:~ # yast lan longhelp
sle:~ # yast lan xmlhelp xmlfile=/tmp/yast_lan.xml

# add-on
sle:~ # yast add-on <uri>
# uri: http:// ftp:// nfs:// disk:// cd:// or dvd://
# ie: http://server.name/directory/Lang-AddOn-CD1/

# audit-laf
sle:~ # yast audit-laf set log_file=/tmp/audit.log
sle:~ # yast audit-laf show diskspace

# dhcp-server
sle:~ # yast dhcp-server interface current

# dns-server
sle:~ # yast dns-server acls show
sle:~ # yast dnsrecord add zone=example.org query=office.example.org type=NS value=ns3
sle:~ # yast dns-server forwarders add ip=10.0.0.100
sle:~ # yast dns-server forwarders show
sle:~ # yast dns-server host show zone=example.org
sle:~ # yast dns-server logging set updates=no transfers=yes
sle:~ # yast dns-server mailserver add zone=example.org mx=mx1 priority=100
sle:~ # yast dns-server nameserver add zone=example.com ns=ns1
sle:~ # yast dns-server soa set zone=example.org serial=2006081623 ttl=2D3H20S
sle:~ # yast dns-server startup atboot
sle:~ # yast dns-server zones add name=example.org zonetype=master

# disk
sle:~ # yast disk list disks
sle:~ # yast disk list partitions

# ftp-server
sle:~ # yast ftp-server SSL enable
sle:~ # yast ftp-server TLS disable
sle:~ # yast ftp-server access authen_only
sle:~ # yast ftp-server anon_access can_upload
sle:~ # yast ftp-server anon_dir set_anon_dir=/srv/ftp
sle:~ # yast ftp-server chroot enable
sle:~ # yast ftp-server chroot disable
sle:~ # yast ftp-server idle-time set_idle_time=15
sle:~ # yast ftp-server logging enable
sle:~ # yast ftp-server logging disable
sle:~ # yast ftp-server max_clients set_max_clients=1500
sle:~ # yast ftp-server max_clients_ip set_max_clients=20
sle:~ # yast ftp-server max_rate_anon set_max_rate=10000
sle:~ # yast ftp-server max_rate_authen set_max_rate=10000
sle:~ # yast ftp-server port_range set_min_port=20000 set_max_port=30000
sle:~ # yast ftp-server show
sle:~ # yast ftp-server startup atboot
sle:~ # yast ftp-server umask set_umask=177:077
sle:~ # yast ftp-server welcome_message set_message="hello everybody"

# http-server
sle:~ # yast http-server configure help
sle:~ # yast http-server configure host=main \
  servername=www.example.com
  serveradmin=admin@example.com
sle:~ # yast http-server hosts create \
  servername=www.example.com \
  serveradmin=admin@example.com \
  documentroot=/var/www
sle:~ # yast http-server listen help
sle:~ # yast http-server listen add=81
sle:~ # yast http-server listen list
sle:~ # yast http-server delete=80
sle:~ # yast http-server mode wizard=on
sle:~ # yast http-server modules enable=php5,rewrite
sle:~ # yast http-server modules disable=ssl
sle:~ # yast http-server modules list

# kdump
sle:~ # yast kdump customkernel help
sle:~ # yast kdump customkernel kernel=kdump
sle:~ # yast kdump dumpformat dump_format=ELF
sle:~ # yast kdump dumplevel dump_level=24
sle:~ # yast kdump dumptarget taget=ssh server=<server> port=22 \
  dir=/var/log/dump user=<user>
sle:~ # yast kdump immediatereboot enable
sle:~ # yast kdump immediatereboot disable
sle:~ # yast kdump keepolddumps no=5
sle:~ # yast kdump kernelcommandline command="ro root=LABEL=/"
sle:~ # yast kdump kernelcommandlineappend command="ro root=LABEL=/"
sle:~ # yast kdump notificationcc email="user1@example.com user2@example.com"
sle:~ # yast kdump notificationto email="user1@example.com user2@example.com"
sle:~ # yast kdump show
sle:~ # yast kdump smtppass pass=/path/to/file
sle:~ # yast kdump smtpserver server=smtp.server.com
sle:~ # yast kdump smtpuser user=smtp_user
sle:~ # yast kdump startup enable alloc_mem=128,256
sle:~ # yast kdump startup disable

# keyboard
sle:~ # yast keyboard list
sle:~ # yast keyboard set layout=czech
sle:~ # yast keyboard summary

# lan
sle:~ # yast lan add name=vlan50 ethdevice=eth0 bootproto=dhcp
sle:~ # yast lan delete id=0
sle:~ # yast lan edit id=0 bootproto=dhcp
sle:~ # yast lan list

# language
sle:~ # yast language list
sle:~ # yast language set lang=cs_CZ languages=en_US,es_ES no_packages

# mail
sle:~ # yast mail summary

# nfs
sle:~ # yast nfs add spec=remote_host:/path/to/nfs/share file=/local/mount/point
sle:~ # yast nfs delete spec=remote_host:/path/to/nfs/share file=/local/mount/point
sle:~ # yast nfs edit spec=remote_host:/path/to/nfs/share \
  file=/local/mount/point type=nfs4
sle:~ # yast nfs list

# nfs-server
sle:~ # yast nfs-server add mountpoint=/nfs/export hosts=*.allowed_hosts.com
sle:~ # yast nfs-server delete mountpoint=/nfs/export
sle:~ # yast nfs-server set help
sle:~ # yast nfs-server set enablev4=yes security=yes
sle:~ # yast nfs-server start
sle:~ # yast nfs-server summary
sle:~ # yast nfs-server stop

# nis
sle:~ # yast nis configure server=nis.example.com broadcast=yes
sle:~ # yast nis disable
sle:~ # yast nis enable help
sle:~ # yast nis enable server=nis.example.com broadcast=yes automounter=yes
sle:~ # yast nis find domain=nisdomain.com
sle:~ # yast nis summary

# nis-server
sle:~ # yast nis-server master help
sle:~ # yast nis-server master domain=nisdomain.com yppasswd=yes
sle:~ # yast nis-server slave help
sle:~ # yast nis-server slave domain=nisdomain.com master_ip=10.100.51.65
sle:~ # yast nis-server stop
sle:~ # yast nis-server summary

# proxy
sle:~ # yast proxy authentication help
sle:~ # yast proxy authentication username=tux password=secret
sle:~ # yast proxy disable
sle:~ # yast proxy enable
sle:~ # yast proxy set help
sle:~ # yast proxy set https=proxy.example.com
sle:~ # yast proxy summary

# rdp
sle:~ # yast rdp allow set=yes
sle:~ # yast rdp list

# samba-client
sle:~ # yast samba-client configure workgroup=FAMILY
sle:~ # yast samba-client isdomainmember domain=SMB_DOMAIN
sle:~ # yast samba-client joindomain domain=SMB_DOMAIN user=username password=pwd
sle:~ # yast samba-client winbind enable
sle:~ # yast samba-client winbind disable

# samba-server
sle:~ # yast samba-server backend help
sle:~ # yast samba-server backend smbpasswd
sle:~ # yast samba-server configure help
sle:~ # yast samba-server configure workgroup=FAMILY description='Home server'
sle:~ # yast samba-server list
sle:~ # yast samba-server role standalone
sle:~ # yast samba-server service enable
sle:~ # yast samba-server service disable
sle:~ # yast samba-server share help
sle:~ # yast samba-server share name=movies browseable=yes guest_ok=yes

# security
sle:~ # yast security level help
sle:~ # yast security level server
sle:~ # yast security set help
sle:~ # yast security set passwd=sha512 crack=yes
sle:~ # yast security summary

# sound
sle:~ # yast sound add help
sle:~ # yast sound add card=0 volume=75
sle:~ # yast sound channels card=0
sle:~ # yast sound modules
sle:~ # yast sound playtest card=0
sle:~ # yast sound remove card=0
sle:~ # yast sound remove all
sle:~ # yast sound set card=0 volume=80
sle:~ # yast sound show card=0
sle:~ # yast sound volume card=0 play
sle:~ # yast sound summary

# sysconfig
sle:~ # yast sysconfig clear=POSTFIX_LISTEN
sle:~ # yast sysconfig clear=CONFIG_TYPE$/etc/sysconfig/mail
sle:~ # yast sysconfig details variable=POSTFIX_LISTEN
sle:~ # yast sysconfig list all
sle:~ # yast sysconfig set DISPLAYMANAGER=gdm
sle:~ # yast sysconfig set CONFIG_TYPE$/etc/sysconfig/mail=advanced

# tftp-server
sle:~ # yast tftp-server directory path=/srv/tftp
sle:~ # yast tftp-server directory list
sle:~ # yast tftp-server status disable
sle:~ # yast tftp-server status enable
sle:~ # yast tftp-server status show

# timezone
sle:~ # yast timezone list
sle:~ # yast timezone set timezone=Europe/Prague hwclock=local
sle:~ # yast timezone summary

# users
sle:~ # yast users add help
sle:~ # yast users add username=user1 password=secret home=/home/user1
sle:~ # yast users delete help
sle:~ # yast users delete username=user1 delete_home
sle:~ # yast users edit help
sle:~ # yast users edit username=user1 password=new_secret
sle:~ # yast users list help
sle:~ # yast users list system
sle:~ # yast users show help
sle:~ # yast users show username=wwwrun
```


---

# YaST Online Update


---

# Managing Software with Command Line Tools

## Using Zypper

```bash
sle:~ # zypper patch
sle:~ # zypper --non-interactive patch
sle:~ # zypper patch --auto-agree-with-licenses
sle:~ # zypper install mplayer
sle:~ # zypper search -t pattern
sle:~ # zypper -v install --from factory mc vim
sle:~ # zypper remove --dry-run MozillaFirefox
sle:~ # zypper --userdata <STRING> patch

# subcommand
sle:~ # zypper help subcommand
sle:~ # zypper help appstream-cache

# install & remove
sle:~ # zypper install <PACKAGE>
sle:~ # zypper remove <PACKAGE>
sle:~ # zypper in MozillaFirefox
sle:~ # zypper in MozillaFirefox-52.2
sle:~ # zypper in mozilla:MozillaFirefox
sle:~ # zypper in 'Moz*'
sle:~ # zypper rm '*-debuginfo'
sle:~ # zypper in firefox
sle:~ # zypper in 'firefox.x86_64'
sle:~ # zypper in 'firefox>=74.2'
sle:~ # zypper in 'firefox.x86_64>=74.2'
sle:~ # zypper in /tmp/install/MozillaFirefox.rpm
sle:~ # zypper in http://download.example.com/MozillaFirefox.rpm
sle:~ # zypper in emacs -vim
sle:~ # zypper rm emacs +vim
sle:~ # zypper in -emacs +vim         # Wrong
sle:~ # zypper in vim -emacs          # Correct
sle:~ # zypper in -- -emacs +vim      # Correct
sle:~ # zypper rm emacs +vim          # Correct
sle:~ # zypper rm --clean-deps <PACKAGE>
sle:~ # zypper in --non-interactive <PACKAGE>
sle:~ # zypper source-install <PACKAGE>
sle:~ # zypper source-install -D <PACKAGE>
sle:~ # zypper source-install -d <PACKAGE>
sle:~ # zypper search -t srcpackage
sle:~ # zypper source-download  # /var/cache/zypper/source-download
sle:~ # zypper --plus-content debug \
   install "debuginfo(build-id)=eb844a5c20c70a59fc693cd1061f851fb7d046f4"

# utility
sle:~ # zypper verify
sle:~ # zypper install-new-recommends

# patch
sle:~ # zypper patch
sle:~ # zypper patch --with-update
sle:~ # zypper patch --with-optional
sle:~ # zypper patch --bugzilla=<NUMBER>
sle:~ # zypper patch --cve=<NUMBER>
sle:~ # zypper patch --updatestack-only
sle:~ # zypper patch --cve=CVE-2010-2713
sle:~ # zypper patch-check
sle:~ # zypper list-patches
sle:~ # zypper list-patches --bugzilla=972197,956917
sle:~ # zypper list-patches --bugzilla=CVE-2016-2315,CVE-2016-2324
sle:~ # zypper list-patches --all --cve
sle:~ # zypper update
sle:~ # zypper update <PACKAGE>
sle:~ # zypper install <PACKAGE>
sle:~ # zypper list-updates
sle:~ # zypper list-updates --all
sle:~ # zypper packages --orphaned
sle:~ # zypper ps
sle:~ # zypper ps -s
sle:~ # zypper ps -ss
sle:~ # zypper ps -sss
sle:~ # zypper ps--print "systemctl status %s"

# repo
sle:~ # zypper repos
sle:~ # zypper repos -d
sle:~ # zypper addrepo <URI> <ALIAS>
sle:~ # zypper refresh
sle:~ # zypper --plus-content refresh
sle:~ # zypper removerepo 1
sle:~ # zypper removerepo "SLEHA-12-GEO"
sle:~ # zypper modifyrepo -er -p 20 'updates'
sle:~ # zypper renamerepo 'Mozilla Firefox' firefox

# querying repo and package
sle:~ # zypper products
sle:~ # zypper patterns
sle:~ # zypper packages
sle:~ # zypper patches
zypper search "fire"
zypper search --match-exact "MozillaFirefox"
zypper search -d fire
zypper search -u fire
zypper se "/fir[^e]/"
zypper search-packages <package1> <package2>
zypper what-provides 'perl(SVN::Core)'
zypper info --requires MozillaFirefox

# lifecycle
sle:~ # zypper lifecycle

# config
sle:~ # ls /etc/zypp/zypper.conf
sle:~ # ls ~/.zypper.conf

# troubleshooting
sle:~ # zypper refresh
sle:~ # zypper refresh -fdb
```


## RPM — the Package Manager

```bash
sle:~ # rpm --checksig <PACKAGE>-x.y.z.rpm 
sle:~ # rpm --import /usr/share/doc/packages/suse-build-key/suse_ptf_key.asc
sle:~ # rpm -i <PACKAGE>.rpm
sle:~ # rpm -e <PACKAGE>

sle:~ # rpm -q -i wget
sle:~ # rpm -q -f /bin/rpm /usr/bin/wget
sle:~ # rpm -q --changelog <PACKAGE>

sle:~ # rpm -V wget
```

`THE MOST IMPORTANT RPM QUERY OPTIONS`

```
-i                Package information
-l                File list
-f FILE           Query the package that contains the file FILE (the full path must be specified with FILE)
-s                File list with status information (implies -l)
-d                List only documentation files (implies -l)
-c                List only configuration files (implies -l)
--dump            File list with complete details (to be used with -l, -c, or -d)
--provides        List features of the package that another package can request with --requires
--requires, -R    Capabilities the package requires
--scripts         Installation scripts (preinstall, postinstall, uninstall)
```


### Installing and Compiling Source Packages

```bash
sle:~ # rpmbuild -bX /usr/src/packages/SPECS/wget.spec

sle:~ # cd /usr/src/packages/SOURCES/
sle:~ # mv ../SPECS/wget.spec .
sle:~ # build --rpms /media/dvd/suse/ wget.spec
```

```
-bp   sources in /usr/src/packages/BUILD: unpack and patch.
-bc   same -bp, additional compilation.
-bi   same -bp, additional installation of the built software
-bb   same -bi, additional creation of the binary package. binary should be in /usr/src/packages/RPMS.
-ba   same -bb, additional creation of source RPM, binary should be in /usr/src/packages/SRPMS.
```


---

# System Recovery and Snapshot Management with Snapper
