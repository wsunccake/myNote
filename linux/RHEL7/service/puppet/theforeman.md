# The Foreman #


## Architecture ##

![Foreman Architecture](https://blog.codecentric.de/wp-content/blogs.dir/2/files/2014/03/Foreman-1024x589.png)


## Requirement ##


### FQDN ###

	# for /etc/hosts setting
	RHEL:~ # cat /etc/hosts
	192.168.31.161   foreman.test.com    foreman

	# 確認 hostname 跟 fqdn 相同
	RHEL~: # hostname -f
	RHEL~: # facter fqdn


### Firewall ###

Puppet 預設使用 8140 port 通訊, 若系統有防火牆設定, 需開通 8140 port. RHEL / CentOS 7 有兩種防火牆, 從 RHEL / CentOS 6 延生過的來的 iptables 和 RHEL / CentOS 7 新用的 firewalld. 在設定防火牆前, 需確定使用哪種


| Port			 | Protocol 	 | Required For 												 |
| -------------- | ------------- | ------------------------------------------------------------- |
| 53			 | TCP & UDP	 | DNS Server 													 |
| 67, 68		 | UDP			 | DHCP Server 													 |
| 69			 | UDP	* 		 | TFTP Server 													 |
| 80, 443		 | TCP	* 		 | HTTP & HTTPS access to Foreman web UI - Apache + Passenger 	 |
| 3000			 | TCP			 | HTTP access to Foreman web UI - WEBrick 						 |
| 3306			 | TCP			 | Separate MySQL database 										 |
| 5910 - 5930	 | TCP			 | Server VNC Consoles 											 |
| 5432			 | TCP			 | Separate PostgreSQL database 								 |
| 8140			 | TCP	* 		 | Puppet Master 												 |
| 8443			 | TCP			 | Smart Proxy, open only to Foreman 							 |


	# for firewalld
	RHEL:~ # firewall-cmd --permanent --add-port=53/tcp --add-port=53/udp
	RHEL:~ # firewall-cmd --permanent --add-port=67/udp --add-port=68/udp --add-port=69/udp
	RHEL:~ # firewall-cmd --permanent --add-port=80/tcp --add-port=443/tcp --add-port=3000/tcp --add-port=8443/tcp
	RHEL:~ # firewall-cmd --permanent --add-port=3306/tcp
	RHEL:~ # firewall-cmd --permanent --add-port=5910-5930/tcp
	RHEL:~ # firewall-cmd --permanent --add-port=5432/tcp
	RHEL:~ # firewall-cmd --permanent --add-port=8140/tcp
	RHEL:~ # firewall-cmd --reload
	RHEL:~ # firewall-cmd --list-all

	# 或是關掉 firewalld
	RHEL:~ # systemctl stop firewalld
	RHEL:~ # systemctl diable firewalld

	# for iptables, 以下三種方式任選一種
	RHEL:~ # iptables -I INPUT -p tcp –dport 53 -j ACCEPT
	RHEL:~ # iptables -I INPUT -p udp –dport 67:69 -j ACCEPT
	RHEL:~ # iptables -I INPUT -p tcp --match multiport –dports 80,433,3000,8443 -j ACCEPT
	RHEL:~ # iptables -I INPUT -p tcp –dport 3306 -j ACCEPT
	RHEL:~ # iptables -I INPUT -p tcp –dport 5910:5930 -j ACCEPT
	RHEL:~ # iptables -I INPUT -p tcp –dport 8140 -j ACCEPT

	# 或是關掉 iptables
	RHEL:~ # systemctl stop iptables
	RHEL:~ # systemctl diable iptables


### Package ###

* foreman

* foreman-installer

* foreman-proxy


## All In One Install ##

puppet master + foreman at same machine, 確認 foreman 以安裝好 puppet master 且可以運行


### Package ###

	foreman:~ # rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
	foreman:~ # yum install epel-release http://yum.theforeman.org/releases/1.9/el7/x86_64/foreman-release.rpm
	foreman:~ # yum install foreman-installer


### Install ###

`method 1`

使用互動模式, 安裝設定

	foreman:~ # foreman-installer -i


`method 2`

直接修改設定檔 (在此稱為 answears file)

	foreman:~ # tree /etc/foreman
	/etc/foreman
	|-- database.yml
	|-- email.yaml
	|-- foreman-debug.conf
	|-- foreman-installer-answers.yaml # 此檔為大部份模組設定
	|-- foreman-installer.yaml
	|-- logging.yaml
	|-- plugins
	\-- settings.yaml

	foreman:~ # vi /etc/foreman/foreman-installer-answers.yaml
	foreman:~ # foreman-install # 直接執行指令安裝設定


`method 3`

指令方式設定

	foreman:~ # foreman-install --enable-foreman --enable-foreman-cli --enable-foreman-proxy

`foreman-proxy`

	foreman:~ # systemctl restart foreman-proxy.service
	netstat -luntp | grep 8443

	/etc/foreman-proxy/settings.yml or config/settings.yml


在此建議使用 `互動模式` 或 `修改 answears file` 方式安裝

	foreman:~ # systemctl enable foreman.service
	foreman:~ # systemctl start foreman.service

安裝完成後可用瀏覽器開啟 http://foreman.test.com 網頁


## Provisioning ##

![Foreman boot sequence](https://blog.codecentric.de/wp-content/blogs.dir/2/files/2014/04/Foreman-boot-sequence.png)

1. Host boots with PXE-protocol

2. Host sends a broadcasts to search a DHCP-server that can handle PXE requests

3. DHCP-server (Smart-Proxy) answers and gives an ip-address to client

4. PXE-Server will be contacted, it knows route to TFTP-Server

5. TFTP-Server holds a boot image for host


Host -> Provisioning Templates

  kind: provision   Kickstart default

  kind: PXELinux    Kickstart default PXELinux

Host -> Partition Tables

Host -> Installation Media
Host -> Operating systems

Infrastructure -> Subnets


## Usage ##

Infrasture -> Smart proxies

Hosts -> New host


agent:
/var/lib/puppet/classes.txt
               /state/resource.txt


## Compute Resources and Profiles ##


| Provider 					 | Package 			 | Unattended installation 	 | Image-based 	 | Console 			 | Power management 	 |
| -------------------------- | ----------------- | ------------------------- | ------------- | ----------------- | --------------------- |
| EC2 						 | foreman-ec2 		 | no 						 | yes 			 | read-only 		 | yes 					 |
| Google Compute Engine 	 | foreman-gce 		 | no 						 | yes 			 | no 				 | yes 					 |
| Libvirt 					 | foreman-libvirt 	 | yes 						 | yes 			 | VNC or SPICE 	 | yes 					 |
| OpenStack Nova 			 | foreman-compute 	 | no 						 | yes 			 | no 				 | yes 					 |
| oVirt / RHEV 				 | foreman-ovirt 	 | yes 						 | yes 			 | VNC or SPICE 	 | yes 					 |
| Rackspace 				 | foreman-compute 	 | no 						 | yes 			 | no 				 | yes 					 |
| VMware 					 | foreman-vmware 	 | yes 						 | yes 			 | VNC 				 | yes 					 |


### Libvirt ###

foreman 支援 libvirt 架構, 但也是透過 ssh 方式, 所以要啟用 foreman 帳號可使用 key 登入 libvirtd 主機

	foreman:~ # mkdir /usr/share/foreman/.ssh
	foreman:~ # chmod 700 /usr/share/foreman/.ssh
	foreman:~ # chown foreman:foreman /usr/share/foreman/.ssh

	foreman:~ # su foreman -s /bin/bash # 切換成 foreman 帳號
	foreman:~ $ ssh-keygen
	foreman:~ $ ssh-copy-id root@libvirtd.test.com
	foreman:~ $ restorecon -RvF /usr/share/foreman/.ssh
	foreman:~ $ virsh -c qemu+ssh://root@libvirtd.test.com/system list # 確認 virsh 可否正常執行


### VMware ###


## Smart Proxy ##

The Smart Proxy is a project which provides a restful API to various sub-systems. Its goal is to provide an API for a higher level orchestration tools (such as Foreman). The Smart proxy provides an easy way to add or extended existing subsystems and APIs using plugins. Currently supported (Click on the links below for more details).

DHCP - ISC DHCP and MS DHCP Servers

DNS - Bind and MS DNS Servers

Puppet - Any Puppet server from 0.24.x

Puppet CA - Manage certificate signing, cleaning and autosign on a Puppet CA server

Realm - Manage host registration to a realm (e.g. FreeIPA)

TFTP - any UNIX based tftp server

### install ##

	foreman:~ # systemctl enable foreman-proxy.service
	foreman:~ # systemctl start foreman-proxy.service

	foreman:~ # tree /etc/foreman-proxy
	settings.yml


### TFTP ###

	foreman:~ # yum install tftp-server
	foreman:~ # cat /etc/foreman-proxy/settings.yaml
	:enabled: https
	:tftproot: /var/lib/tftpboot/

	foreman:~ # systemctl restart foreman-proxy.service


### DHCP ###

	foreman:~ # yum install dhcp
	systemctl enable dhcpd
	systemctl start dhcpd


### Provisioning ###

1. Smart Proxies

	Infrastructure -> Smart Proxies

2. Operating systems

	Hosts -> Operating systems

	設定為CentOS 6

3. Provisioning Templates

	Hosts -> Provisioning Templates

	設定 provision 和 PXELinux, 並 associate 剛剛設定的 CentOS

  kind: provision   Kickstart default
  kind: PXELinux    Kickstart default PXELinux
                    epel

4. Partition Tables

	Hosts -> Partition Tables
	  Kickstart default

5. Installation Media

	Host -> Installation Media
	  CentOS mirror

6. Subnets

	Infrastructure -> Subnets



subnet:
foreman-installer \
  --enable-foreman-proxy \
  --foreman-proxy-tftp=true \
  --foreman-proxy-tftp-servername=10.10.10.11 \
  --foreman-proxy-dhcp=true \
  --foreman-proxy-dhcp-interface=ens9 \
  --foreman-proxy-dhcp-gateway= \
  --foreman-proxy-dhcp-range="10.10.10.100 10.10.10.150" \
  --foreman-proxy-dhcp-nameservers="" \
  --foreman-proxy-dns=true \
  --foreman-proxy-dns-interface=ens9 \
  --foreman-proxy-dns-zone=test.com \
  --foreman-proxy-dns-reverse=10.10.10.in-addr.arpa \
  --foreman-proxy-dns-forwarders=172.17.17.16 \
  --foreman-proxy-foreman-base-url=https://master.test.com \
  --foreman-proxy-oauth-consumer-key=Dp9wKif3FwUhgwKA66kwvSb9kWduX8Vm \
  --foreman-proxy-oauth-consumer-secret=U6d5xdmVuqNztrrJyCTyGjMtESbtd8WL
https://www.youtube.com/watch?v=eHjpZr3GB6s


更新 image
/var/lib/tftpboot/boot/CentOS-7.0-x86_64-initrd.img
/var/lib/tftpboot/boot/CentOS-7.0-x86_64-vmlinuz


## Ref ##

[Introduction to Foreman](https://prezi.com/heph6y7kzole/introduction-to-foreman/)

[Foreman 1.9 Manual](http://theforeman.org/manuals/1.9/index.html)
