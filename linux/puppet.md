# Puppet #

## Network ##

server / puppet master  ----   client / puppet agent

master.test.com                agent.test.com

192.168.31.150                 192.168.31.151

### Note ###

- FQDN:

Puppet master 和 agent 間都使用主機名稱做設定, 故需要能解析 master 和 agent 的 hostname <-> ip 關係, 可以在 /etc/hosts 或使用 DNS

- Firewall:

Puppet 預設使用 8140 port 通訊, 若系統有防火牆設定, 需開通 8140 port

- certificate:

Puppet master 和 agent 間通訊有使用到 SSL, 各主機間時間需要同步, 可使用 NTP

- SELinux:

RHEL 建議關掉 SELinux

	RHEL:~ # vi /etc/selinux/config
	...
	SELINUX=disabled # 將此設定改為 disable
	...
	RHEL:~ # reboot # 設定後需重開機才會生效

	# 確認當前 seliunx 設定, Disable 表示關閉
	RHEL:~ # getenforce 


## package ##

* ruby, ruby-libs, ruby-shadow

* puppet-server (server)

* puppet (client)


## Install ##

以下將使用 CentOS 7.1 上安裝 Puppet 為範例

### puppet master server ###


`FQDN`

	# for /etc/hosts setting
	master:~ # cat /etc/hosts
	192.168.31.151  agent   agent.test.com
	192.168.31.150  master  master.test.com


`firewall`

CentOS 7 有兩種防火牆, 從 CentOS 6 延生過的來的 iptables 和 CentOS 7 新用的 firewalld. 在設定防火牆前, 需確定使用哪種

	# for firewalld
	master:~ # firewall-cmd --permanent --add-port=8140/tcp --add-port=8140/udp
	master:~ # firewall-cmd --reload
	master:~ # firewall-cmd --list-all

	# 或是關掉 firewalld
	master:~ # systemctl stop firewalld
	master:~ # systemctl diable firewalld

	# for iptables, 以下三種方式任選一種
	master:~ # iptables -I INPUT -p tcp -m tcp –dport 8140 -j ACCEPT
	master:~ # iptables -A RH-Firewall-1-INPUT -p tcp -m tcp --dport 8140 -j ACCEPT
	master:~ # iptables -A RH-Firewall-1-INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

	# 或是關掉 iptables
	master:~ # systemctl stop iptables
	master:~ # systemctl diable iptables


`package`

	# install package
	master:~ # rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
	master:~ # yum install puppet-server

	# puppet master service
	master:~ # systemctl enable puppetmaster.service
	master:~ # systemctl start puppetmaster.service

	# 指令方式執行
	master:~ # puppet master --verbose --no-daemonize # 同上, 實際使用執行指令方式


### puppet agent server ###


`FQDN`

同 puppet master server

	# for /etc/hosts setting
	agent:~ # cat /etc/hosts
	192.168.31.151  agent   agent.test.com
	192.168.31.150  master  master.test.com


`firwall`

同 puppet master server

	# for firewalld
	agent:~ # firewall-cmd --permanent --add-port=8140/tcp --add-port=8140/udp
	agent:~ # firewall-cmd --reload
	agent:~ # firewall-cmd --list-all

	# 或是關掉 firewalld
	agent:~ # systemctl stop firewalld
	agent:~ # systemctl diable firewalld

	# for iptables, 以下三種方式任選一種
	agent:~ # iptables -I INPUT -p tcp -m tcp –dport 8140 -j ACCEPT
	agent:~ # iptables -A RH-Firewall-1-INPUT -p tcp -m tcp --dport 8140 -j ACCEPT
	agent:~ # iptables -A RH-Firewall-1-INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

	# for iptables
	agent:~ # systemctl stop iptables
	agent:~ # systemctl diable iptables


`package`

	# install package
	agent:~ # rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
	agent:~ # yum install puppet

	# puppet agent service
	# 第一次安裝後, 並不建議直接啟動 agent. 設定測試完之後, 在使用 daemon 方式比較適合
	agent:~ # systemctl enable puppet.service
	agent:~ # systemctl start puppet.service

	# 使用執行指令方式並寫入到 crontab
	agent:~ # puppet resource cron puppet-agent ensure=present user=root minute=30 command='/usr/bin/puppet agent --onetime --no-daemonize --splay'
	agent:~ # crontab -e

	# configuration
	agent:~ # vim /etc/
	[main]
	...
	    server = master.test.com
	...

	# 修改設定後, 需重啟 puppet agent service
	agent:~ # systemctl restart puppet.service


### puppet test ###

Puppet master 和 agent 間的通訊使用 SSL, 所以要設定 certificate. 預設是將相關檔案放置 /var/lib/puppet/ssl 目錄底下

	# agent 向 master 申請 certicate
	agent:~ # puppet agent --server master.test.com --test

	# 建立測試檔案
	master:~ # cat /etc/puppet/manifests/site.pp
	node default { file { "/tmp/$hostname.txt": content => "Hello Puppet"; } }

	master:~ # puppet cert list # list uncert agent
	master:~ # puppet cert sign agent.test.com # sign agent
	master:~ # puppet cert sign --all # sing all

	# agent 測試
	agent:~ # puppet agent --server master.test.com --test
	agent:~ $ ls /tmp # 此時可以看到 agent.txt


### puppet certificate ###

`manual sign`

	agent:~ # puppet agent --server master.test.com --test # agent 申請註冊

	master:~ # puppet cert list # 顯示所有申請認證主機
	"agent.test.com" (SHA256) A9:D1:96:76:C5:1C:4A:0F:E4:D1:28:09:88:1D:13:F6:97:CB:E2:50:10:74:7E:EC:3F:4D:70:0A:1D:D0:F7:8D
	master:~ # puppet cert list --all # 顯示所有認證主機 (包括以認證和未認證)
	  "agent.test.com"  (SHA256) A9:D1:96:76:C5:1C:4A:0F:E4:D1:28:09:88:1D:13:F6:97:CB:E2:50:10:74:7E:EC:3F:4D:70:0A:1D:D0:F7:8D
	+ "master.test.com" (SHA256) 65:4A:5C:C7:23:53:32:60:95:A4:15:76:A5:97:A0:17:09:32:7C:8C:C6:A7:CC:82:D6:1B:85:65:1E:75:5D:A3 (alt names: "DNS:master.test.com", "DNS:puppet", "DNS:puppet.test.com")

	master:~ # puppet cert sign agent.test.com # 手動註冊

	master:~ # tree /var/lib/puppet/ssl/ca/signed # 另一種確認認證主機方式
	/var/lib/puppet/ssl/ca/signed
	├── agent.test.com.pem
	└── master.test.com.pem


`auto sign`

	master:~ # echo "*.test.com" >> /etc/puppet/autosign.conf
	master:~ # systemctl restart puppetmaster.service
	master:~ # puppet cert list --all
	+ "master.test.com" (SHA256) 65:4A:5C:C7:23:53:32:60:95:A4:15:76:A5:97:A0:17:09:32:7C:8C:C6:A7:CC:82:D6:1B:85:65:1E:75:5D:A3 (alt names: "DNS:master.test.com", "DNS:puppet", "DNS:puppet.test.com")

	agent:~ # puppet agent --server master.test.com --test

	puppet cert list --all
	+ "agent.test.com"  (SHA256) 1F:18:8A:5E:9D:0D:9F:1E:A5:AF:83:2B:70:3F:01:43:06:7C:1D:65:81:D2:6F:D6:DB:41:2A:8C:AA:4D:23:FD
	+ "master.test.com" (SHA256) 65:4A:5C:C7:23:53:32:60:95:A4:15:76:A5:97:A0:17:09:32:7C:8C:C6:A7:CC:82:D6:1B:85:65:1E:75:5D:A3 (alt names: "DNS:master.test.com", "DNS:puppet", "DNS:puppet.test.com")


`preprovision sign`

	master:~ # puppet ca generate agent.test.com
	master:~ # tree /var/lib/puppet/ssl
	/var/lib/puppet/ssl
	├── ca
	│   ├── ca_crl.pem
	│   ├── ca_crt.pem
	│   ├── ca_key.pem
	│   ├── ca_pub.pem
	│   ├── inventory.txt
	│   ├── private
	│   │   └── ca.pass
	│   ├── requests
	│   ├── serial
	│   └── signed
	│       ├── agent.test.com.pem
	│       └── master.test.com.pem
	├── certificate_requests
	├── certs
	│   ├── agent.test.com.pem*
	│   ├── ca.pem*
	│   └── master.test.com.pem
	├── crl.pem
	├── private
	├── private_keys
	│   ├── agent.test.com.pem*
	│   └── master.test.com.pem
	└── public_keys
	    ├── agent.test.com.pem
	    └── master.test.com.pem

	agent:~ # puppet agent --server master.test.com --test
	agent:~ # tree /var/lib/puppet/ssl/
	/var/lib/puppet/ssl/
	├── certificate_requests
	├── certs
	│   ├── agent.test.com.pem
	│   └── ca.pem
	├── private
	├── private_keys
	│   └── agent.test.com.pem
	└── public_keys
	    └── agent.test.com.pem

	master:~ # scp /var/lib/puppet/ssl/private_keys/agent.test.com.pem agent.test.com:/var/lib/puppet/ssl/private_keys/
	master:~ # scp /var/lib/puppet/ssl/certs/agent.test.com.pem agent.test.com:/var/lib/puppet/ssl/certs/
	master:~ # scp /var/lib/puppet/ssl/certs/ca.pem agent.test.com:/var/lib/puppet/ssl/certs/


`clean sign`

	agent:~ # rm -rf /var/lib/puppet/ssl/*

	master:~ # puppet cert clean agent.test.com


## configuration ##


### command ###

常用指令

`help`

	puppet:~ # puppet help
	puppet:~ # puppet help master


`master`

	master:~ # puppet master --getconfig
	master:~ # puppet master --no--daemonize --debug


`agent`

	agent:~ # puppet agent --server=master.test.com --test
	agent:~ # puppet agent --noop # dry-run, no-op


`apply`

apply 功能上跟 agent 一樣, 只是使用 apply 僅在 puppet agent 上執行, 而 agent 是 puppet agent 向 puppet master

	master:~ # cat /etc/puppet/modules/foo/manifests/init.pp
	class test { file { "/tmp/$hostname.txt": content => "Hello Puppet"; } }

	master:~ # puppet apply /etc/puppet/modules/foo/manifests/init.pp


	master:~ # puppet master --compile agent.test.com > agent.test.com.json
	master:~ # scp agent.test.com.json agent.test.com:~/

	agent:~ # puppet apply --catalog agent.auto.com.json


`cert`

	master:~ # puppet cert list
	master:~ # puppet cert list --all
	master:~ # puppet cert sign agent.test.com
	master:~ # puppet cert clean agent.test.com


`kick`

	mater:~ # puppet kick


`parser`

確認設定檔

	master:~ # cat /etc/puppet/manifests/site.pp 
	node default { file { "/tmp/$hostname.txt": content => "Hello Puppet\n"; } }
	master:~ # puppet parser validate /etc/puppet/manifests/site.pp


`resource`

	master:~ # puppet resource --type
	master:~ # puppet resource package mlocate # 顯示目前系統 package 設定
	master:~ # puppet resource user root # 顯示目前系統 user 設定


`describe`

	master:~ # puppet describe --list


### module ###

	master:~ # mkdir -p /etc/puppet/modules/foo/{files,manifests,templates}
	msater:~ # tree /etc/puppet/modules/
	/etc/puppet/modules/
	└── foo
	    ├── files # 存放下載檔案
	    ├── manifests # pp
	    └── templates # erb

	master:~ # touch /etc/puppet/modules/foo/manifests/{init.pp,config.pp,install.pp,service.pp,params.pp}
	master:~ # tree /etc/puppet/modules/foo/manifests
	/etc/puppet/modules/foo/manifests
	├── config.pp
	├── init.pp
	├── install.pp
	├── params.pp
	└── service.pp


### node ###

	msater:~ # tree /etc/puppet/manifests/site.pp


## update mode ##


### pull mode ###

	agent:~ # vi /etc/puppet/puppet.conf
	...
	[agent]
	...
	    runinterval = 10 # 每 10 秒更新, 預設值為 30 分鐘
	...

### push mode ###


## Ref ##

* [零基礎學習 Puppet 自動化配置管理](http://kisspuppet.com)

* [Puppet 運維實戰](http://kisspuppet.gitbooks.io/puppet/content)

* [Puppet 實戰](http://www.m.sanmin.com.tw/Product/index/99M155F6c102e39c109H72T108R127CAIuHGm513IbM)

* [Puppet Tutorial](http://www.example42.com/tutorials/PuppetTutorial/)