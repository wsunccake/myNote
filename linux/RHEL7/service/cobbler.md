# Cobbler #


## Prerequisites

```
# package
rhel:~ # yum install epel-release
rhel:~ # yum install httpd dnsmasq rsync tftp-server
rhel:~ # yum install syslinux mkisofs
rhel:~ # yum install createrepo yum-utils
rhel:~ # yum install mod_wsgi mod_ssl
rhel:~ # yum install python-cheetah python-django python-netaddr python-urlgrabber
rhel:~ # yum install pykickstart python2-simplejson PyYAML

# firewall
rhel:~ # firewall-cmd --add-port=4011/tcp --permanent
rhel:~ # firewall-cmd --add-service=http --permanent
rhel:~ # firewall-cmd --add-service=https --permanent
rhel:~ # firewall-cmd --add-service=dhcp --permanent
rhel:~ # firewall-cmd --add-service=dns --permanent
rhel:~ # firewall-cmd --add-service=tftp --permanent
rhel:~ # firewall-cmd --reload
```


## Pacakge ##

```
# package
rhel:~ # yum install cobbler cobbler-web
```


## Configuration

```
rhel:~ # vi /etc/cobbler/modules.conf
[authentication]
module = authn_configfile

[authorization]
module = authz_allowall

[dns]
module = manage_dnsmasq
  
[dhcp]
module = manage_dnsmasq

[tftpd]
module = manage_in_tftpd

rhel:~ # vi /etc/cobbler/settings
...
default_password_crypted: "$1$mF86/UHC$WvcIcX2t6crBz2onWxyac."
...
manage_dhcp: 1
manage_dns: 1
manage_tftpd: 1
...
next_server: 192.168.100.1
server: 192.168.100.1

rhel:~ # vi /etc/cobbler/dnsmasq.template
read-ethers
addn-hosts = /var/lib/cobbler/cobbler_hosts

# setup dhcp ip range
dhcp-range=192.168.100.50,192.168.100.100,255.255.255.0
dhcp-option=3,$next_server
dhcp-lease-max=1000
dhcp-authoritative
dhcp-boot=pxelinux.0
dhcp-boot=net:normalarch,pxelinux.0
dhcp-boot=net:ia64,$elilo

$insert_cobbler_system_definitions

# enable dnsmasq tftp
enable-tftp
tftp-root=/var/lib/tftpboot

rhel:~ # cobbler check
rhel:~ # cobbler sync

# change cobbler web user/password
rhel:~ # htdigest /etc/cobbler/users.digest Cobbler user

# os support
rhel:~ # vi /var/lib/cobbler/distro_signatures.json
rhel:~ # cobbler signature report
```

https://localhost/cobbler_web


## Import CD/DVD

### CentOS

```
rhel:~ # mount -oloop CentOS-7-x86_64-Minimal-1611.iso /mnt
rhel:~ # cobbler import --name=CentOS7 --arch=x86_64 --path=/mnt
```

### openSuSE Leap

```
rhel:~ # mount -oloop openSUSE-Leap-42.2-DVD-x86_64.iso /mnt
rhel:~ # cobbler import --name=openSuSELeap42.2 --arch=x86_64 --path=/mnt --breed=suse --kopt=install=http://192.168.100.1/cblr/links/openSuSELeap42.2-x86_64/
```

### Distro and Profile

```
rhel:~ # cobbler distro list
rhel:~ # cobbler distro report

rhel:~ # cobbler profile list
rhel:~ # cobbler profile report

rhel:~ # cobbler system add --name=test-pxe --profile=CentOS7-x86_64 --ip-address=192.168.100.51 --mac=08:00:27:01:02:03 --interface=eth0
```