
# Foreman #

![Foreman Architecture](http://theforeman.org/static/images/foreman_architecture.png)


## Requirement ##

### FQDN ###

	# for /etc/hosts setting
	RHEL:~ # cat /etc/hosts
	192.168.31.151   foreman.test.com    foreman

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


## Install ##

### All in one ###

puppet master + foreman at same machine


`package`

	foreman:~ # rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
	foreman:~ # yum install epel-release http://yum.theforeman.org/releases/1.9/el7/x86_64/foreman-release.rpm
	foreman:~ # yum install foreman-installer
	foreman:~ # yum install puppet-server puppet facter


`config ca`

	foreman:~ # cat /etc/puppet/puppet.conf
	[master]
	    certname = foreman.test.coms # 設定 puppet master 主機

	foreman:~ # systemctl restart puppetmaster.service


`foreman`

	foreman:~ # foreman-installer -i
	--foreman-proxy-dns --foreman-proxy-dhcp

answer file 是 /etc/foreman/foreman-installer-answers.yaml (包括 web 的帳號密碼)

settings.yaml
email.yaml
logging.yaml


`foreman-proxy`

	foreman:~ # systemctl restart foreman-proxy.service
	netstat -luntp | grep 8443

	/etc/foreman-proxy/settings.yml or config/settings.yml


`tftp on foreman-proxy`

	foreman:~ # yum install tftp-server
	foreman:~ # cat /etc/foreman-proxy/settings.d
	:enabled: https
	:tftproot: /var/lib/tftpboot/

	foreman:~ # systemctl restart foreman-proxy.service


`dhcp on foreman-proxy`

	yum install dhcp
	systemctl enable dhcpd
	systemctl start dhcpd

dns:

bind bind-chroot



## Usage ##

0. Infrasture -> Smart proxies

1. Hosts -> New host

將 puppet agent 加入 host 中
確認 

agent:~ # systemctl enable puppetagent
agent:~ # systemctl start puppetagent


2. Configur -> Puppet classes

master:~ # puppet module install -i /etc/puppet/environments/production/modules puppetlabs/ntp



->
agent:
/var/lib/puppet/classes.txt
               /state/resource.txt
