# Puppet #


## Architecture ##

![Puppet Master / Agent Architecture](https://docs.puppetlabs.com/learning/images/manifest_to_defined_state_split.png)


## Network ##

server / puppet master  ----   client / puppet agent

master.test.com                agent.test.com

192.168.31.150                 192.168.31.151


![Manifest](https://docs.puppetlabs.com/ja/learning/images/manifest_to_defined_state_unified.png)

## Requirement ##


### FQDN ###

Puppet master 和 agent 間都使用主機名稱做設定, 故需要能解析 master 和 agent 的 hostname <-> ip 關係, 可以在 /etc/hosts 或使用 DNS

	# for /etc/hosts setting
	RHEL:~ # cat /etc/hosts
	192.168.31.151     agent.test.com   agent
	192.168.31.150     master.test.com  master


### Firewall ###

Puppet 預設使用 8140 port 通訊, 若系統有防火牆設定, 需開通 8140 port. RHEL / CentOS 7 有兩種防火牆, 從 RHEL / CentOS 6 延生過的來的 iptables 和 RHEL / CentOS 7 新用的 firewalld. 在設定防火牆前, 需確定使用哪種

	# for firewalld
	RHEL:~ # firewall-cmd --permanent --add-port=8140/tcp --add-port=8140/udp
	RHEL:~ # firewall-cmd --reload
	RHEL:~ # firewall-cmd --list-all

	# 或是關掉 firewalld
	RHEL:~ # systemctl stop firewalld
	RHEL:~ # systemctl diable firewalld

	# for iptables, 以下三種方式任選一種
	RHEL:~ # iptables -I INPUT -p tcp -m tcp –dport 8140 -j ACCEPT
	RHEL:~ # iptables -A RH-Firewall-1-INPUT -p tcp -m tcp --dport 8140 -j ACCEPT
	RHEL:~ # iptables -A RH-Firewall-1-INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

	# 或是關掉 iptables
	RHEL:~ # systemctl stop iptables
	RHEL:~ # systemctl diable iptables


### certificate ###

Puppet master 和 agent 間通訊有使用到 SSL, 各主機間時間需要同步, 可使用 NTP


### SELinux ###

RHEL 建議關掉 SELinux

	RHEL:~ # vi /etc/selinux/config
	...
	SELINUX=disabled # 將此設定改為 disable
	...
	RHEL:~ # reboot # 設定後需重開機才會生效

	# 確認當前 seliunx 設定, Disable 表示關閉
	RHEL:~ # getenforce 


### Package ###

* ruby, ruby-libs, ruby-shadow

* puppet-server (server)

* puppet (client)


## Install ##

以下將使用 CentOS 7.1 上安裝 Puppet 為範例

### puppet master server ###


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


## language ##


### Data Type ###


#### String ####

`Syntax`

String[<MIN LENGTH>, <MAX LENGTH>]

example

	$foo = 'abcdef'
	notice( $foo )
	notice( $foo[0] )
	notice( $foo[1,3] )


`Bare Words`

	service { "ntp":
	  ensure => running, # bare word string
	}


`Single-Quoted Strings`

	if $autoupdate {
	  notice('autoupdate parameter has been deprecated and replaced with package_ensure.  Set this to latest for the same behavior as autoupdate => true.')
	}


`Double-Quoted Strings`

	if $autoupdate {
	  notice("autoupdate parameter has been deprecated and replaced with package_ensure.  Set this to latest for the same behavior as autoupdate => true."")
	}

| Sequence 		 | Result 							 |
| -------------- | --------------------------------- |
| \\ 			 | Single backslash 				 |
| \n 			 | Newline 							 |
| \r 			 | Carriage return 					 |
| \t 			 | Tab 								 |
| \s 			 | Space 							 |
| \$ 			 | Literal dollar sign 				 |
| \uXXXX 		 | Unicode character number XXXX 	 |
| \u{XXXXXX} 	 | Unicode character XXXXXX 		 |
| \" 			 | Literal double quote 			 |
| \' 			 | Literal single quote 			 |


`Heredocs`

	$mytext = @(EOT)
	    [user]
	        name = ${displayname}
	        email = ${email}
	    [color]
	        ui = true
	    [alias]
	        lg = "log --pretty=format:'%C(yellow)%h%C(reset) %s %C(cyan)%cr%C(reset) %C(blue)%an%C(reset) %C(green)%d%C(reset)' --graph"
	        wdiff = diff --word-diff=color --ignore-space-at-eol --word-diff-regex='[[:alnum:]]+|[^[:space:][:alnum:]]+'
	    [merge]
	        defaultToUpstream = true
	    [push]
	        default = upstream
	    | EOT

	$gitconfig = @("GITCONFIG"/L)
	    [user]
	        name = ${displayname}
	        email = ${email}
	    [color]
	        ui = true
	    [alias]
	        lg = "log --pretty=format:'%C(yellow)%h%C(reset) %s \
	    %C(cyan)%cr%C(reset) %C(blue)%an%C(reset) %C(green)%d%C(reset)' --graph"
	        wdiff = diff --word-diff=color --ignore-space-at-eol \
	    --word-diff-regex='[[:alnum:]]+|[^[:space:][:alnum:]]+'
	    [merge]
	        defaultToUpstream = true
	    [push]
	        default = upstream
	    | GITCONFIG

	file { "${homedir}/.gitconfig":
	  ensure  => file,
	  content => $gitconfig,
	}


#### Integer, Float, and Numeric ####

`Integers`

	$number = 2
	$number / 3 # evaluates to 0


`Floating Point Numbers`

	$some_number = 8 * -7.992           # evaluates to -63.936
	$another_number = $some_number / 4  # evaluates to -15.984
	$product = 8 * .12 # syntax error
	$product = 8 * 0.12 # OK
	$product = 8 * 3e5  # evaluates to 240000.0


`Octal and Hexadecimal Integers`

	# octal
	$value = 0777   # evaluates to decimal 511
	$value = 0789   # Error, invalid octal
	$value = 0777.3 # Error, invalid octal

	# hexadecimal
	$value = 0x777 # evaluates to decimal 1911
	$value = 0xdef # evaluates to decimal 3567
	$value = 0Xdef # same as above
	$value = 0xDEF # same as above
	$value = 0xLSD # Error, invalid hex


`Converting Numbers to Strings`

	printf


`Converting Strings to Numbers`

example1

	$mystring = "85"
	$mynum = 0 + mystring.

example2

	scanf


#### Boolean ####

It matches only the values true or false


#### Array ####

`Syntax`

	[ 'one', 'two', 'three' ]
	# Equivalent:
	[ 'one', 'two', 'three', ]


`Accessing Values`

	$foo = [ 'one', {'second' => 'two', 'third' => 'three'} ]
	notice( $foo[0])
	notice( $foo[1]['third'] )
	notice( $foo[-2] )


`Array Sectioning`

	$foo = [ 'one', 'two', 'three', 'four', 'five' ]
	notice( $foo[2,1] )  # evaluates to ['three']
	notice( $foo[2,2] )  # evaluates to ['three', 'four']
	notice( $foo[2,-1] ) # evaluates to ['three', 'four', 'five']
	notice( $foo[-2,1] ) # evaluates to ['four']


`Additional Functions`

* delete
* delete_at
* flatten
* grep
* hash
* is_array
* join
* member
* prefix
* range
* reverse
* shuffle
* size
* sort
* unique
* validate_array
* values_at
* zip


#### Hash ####

`Syntax`

	{ key1 => 'val1', key2 => 'val2' }
	# Equivalent:
	{ key1 => 'val1', key2 => 'val2', }


`Accessing Values`

	$myhash = { key       => "some value",
	            other_key => "some other value" }
	notice( $myhash[key] )


`Additional Functions`

* has_key
* is_hash
* keys
* merge
* validate_hash
* values


#### Regexp ####


#### Undef ####


#### Default ####


### Abstract Data Types ###

#### Scalar ####
#### Collection ####
#### Variant ####
#### Data ####
#### Pattern ####
#### Enum ####
#### Tuple ####
#### Struct ####
#### Optional ####
#### Catalogentry ####
#### Type ####
#### Any ####
#### Callable ####

### Variables ###

`Variables`

	$content = "some content\n"


`Arrays`

	[$a, $b, $c] = [1,2,3] 


`Hashes`

	[$a, $b] = {a => 10, b => 20}


`Resolution`

	file {'/tmp/testing':
	  ensure  => file,
	  content => $content,
	}
	
	$address_array = [$address1, $address2, $address3]


`Interpolation`

	$rule = "Allow * from $ipaddress"
	file { "${homedir}/.vim":
	  ensure => directory,
	  ...
	}


### Scope ###

![scope-euler-diagram](https://docs.puppetlabs.com/puppet/latest/reference/images/scope-euler-diagram.png)

#### Top Scope ####

`/etc/puppet/manifests/site.pp`

	$variable = "Hi!" # 宣告變數

	class foo { # 宣告類別
	  notify {"Message from elsewhere: $variable":}
	}

	include foo # 載入類別

`執行`

	puppet:~ # puppet /etc/puppet/manifests/site.pp


#### Node scope ####

`/etc/puppet/manifests/site.pp`

	$top_variable = "Available!"

	node 'puppet.example.com' {
	  $variable = "Hi!"
	  notify {"Message from here: $variable":}
	  notify {"Top scope: $top_variable":}
	}

	notify {"Message from top scope: $variable":}


#### Local Scopes ####

`/etc/puppet/modules/foo/manifests/init.pp`

	class foo {
	  $variable = "Hi!"
	  notify {"Message from here: $variable":}
	  notify {"Node scope: $node_variable Top scope: $top_variable":}
	}

`/etc/puppet/manifests/site.pp`

	$top_variable = "Available!"
	node 'puppet.example.com' { # 指定執行 nocde
	  $node_variable = "Available!"
	  include foo # 載入 module 中的 foo 類別
	  notify {"Message from node scope: $variable":}
	}
	notify {"Message from top scope: $variable":}


#### Overriding Received Values ####

`/etc/puppet/modules/foo/manifests/init.pp`

	class foo {
	  $variable = "Hi, I'm local!"
	  notify {"Message from here: $variable":}
	  notify {"Message from here: $::variable":} # $::variable 表示 top scope 的 變數

	  File { ensure => directory, }
	  file {'/tmp/example':}
	}

`/etc/puppet/modules/foo/manifests/params.pp`

	class foo::params {
	  $config_dir = "/etc/foo"
	}

`/etc/puppet/manifests/site.pp`

	$variable = "Hi, I'm top!"
	
	File {
	  ensure => file,
	  owner  => 'puppet',
	}

	node 'puppet.example.com' {
	  $variable = "Hi, I'm node!"
	  include foo

	  notify {"Message from node: $::variable":} # $::variable 表示 top scope 的 變數
	  notify {"Message from node: $foo::variable":} # foo class 底下的 $variable
	  notify {"Message from node: $foo::params::config_dir":} # foo class 底下的 $variable
	}

	notify {"Message from top: $::variable":} # $::variable 表示 top scope 的 變數


### Resource ###

`Simplified Syntax`

	<TYPE> { '<TITLE>':
	  <ATTRIBUTE> => <VALUE>,
	}

example

	file { '/etc/passwd':
	  ensure => file,
	  owner  => 'root',
	  group  => 'root',
	  mode   => '0600',
	}


`Full Syntax`

	<TYPE> {
	  default:
	    *           => <HASH OF ATTRIBUTE/VALUE PAIRS>,
	    <ATTRIBUTE> => <VALUE>,
	  ;
	  '<TITLE>':
	    *           => <HASH OF ATTRIBUTE/VALUE PAIRS>,
	    <ATTRIBUTE> => <VALUE>,
	  ;
	  '<NEXT TITLE>':
	    ...
	  ;
	  ['<TITLE'>, '<TITLE>', '<TITLE>']:
	    ...
	  ;
	}

exmaple

	$file_ownership = {
	  "owner" => "root",
	  "group" => "wheel",
	  "mode"  => "0600",
	}

	file {
	  default:
	    ensure => file,
	    * => $file_ownership,
	  ;
	  ['ssh_host_dsa_key', 'ssh_host_key', 'ssh_host_rsa_key']:
	    # use all defaults
	  ;
	  ['ssh_config', 'ssh_host_dsa_key.pub', 'ssh_host_key.pub', 'ssh_host_rsa_key.pub', 'sshd_config']:
	    # override mode
	    mode => "0644",
	  ;
	}


`Abstract Resource Type`

	file { "/tmp/foo": ensure => file, }
	File { "/tmp/foo": ensure => file, }
	Resource[File] { "/tmp/foo": ensure => file, }

	$mytype = File
	Resource[$mytype] { "/tmp/foo": ensure => file, }

	$mytypename = "file"
	Resource[$mytypename] { "/tmp/foo": ensure => file, }


`Arrays of Titles`

	$rc_dirs = [
	  '/etc/rc.d',       '/etc/rc.d/init.d','/etc/rc.d/rc0.d',
	  '/etc/rc.d/rc1.d', '/etc/rc.d/rc2.d', '/etc/rc.d/rc3.d',
	  '/etc/rc.d/rc4.d', '/etc/rc.d/rc5.d', '/etc/rc.d/rc6.d',
	]

	file { $rc_dirs:
	  ensure => directory,
	  owner  => 'root',
	  group  => 'root',
	  mode   => '0755',
	}


`Adding or Modifying Attributes`

Amending Attributes With a Resource Reference

	file {'/etc/passwd':
	  ensure => file,
	}

	File['/etc/passwd'] {
	  owner => 'root',
	  group => 'root',
	  mode  => '0640',
	}

Amending Attributes With a Collector

	# class
	class base::linux {
	  file {'/etc/passwd':
	    ensure => file,
	  }
	  ...
	}

	# 
	include base::linux
	
	File <| tag == 'base::linux' |> {
	  owner => 'root',
	  group => 'root',
	  mode  => '0640',
	}

Local Resource Defaults

	# mymodule pp
	class mymodule::params {
	  $file_defaults = {
	    mode  => "0644",
	    owner => "root",
	    group => "root",
	  }
	  # ...
	}

	#
	class mymodule inherits mymodule::params {
	  file { default: *=> $mymodule::params::file_defaults;
	    "/etc/myconfig":
	      ensure => file,
	    ;
	  }
	}

create_resources

	#
	$type = "user"
	$resources = {
	  'nick' => { uid    => '1330',
	              groups => ['developers', 'operations', 'release'], },
	  'dan'  => { uid    => '1308',
	              groups => ['developers', 'prosvc', 'release'], },
	}
	$defaults = { gid => 'allstaff',
	              managehome => true,
	              shell      => 'bash',
	            }

	#
	$resources.each |String $resource, Hash $attributes| {
	  Resource[$type] {
	    $resource: * => $attributes;
	    default:   * => $defaults;
	  }
	}


### Relationships and Ordering ###


#### Relationship Metaparameters ####

	<resource> { '<TITLE>':
	  <relationship> => <target resource>,
	}

- before:

resource 必須比 target resource 先執行 (apply)

- require

target resource 必須先執行, resource 才能執行

- notify

resource 只要更新 (refresh), target resource 也會跟執行

- subscribe

resource 會根據 target reousrce 狀態去判斷是否要執行

before and require example

	# install.pp
	package { 'openssh-server':
	  ensure => present,
	  before => File['/etc/ssh/sshd_config'], # Pacage['openssh-server'] 必須比 File['/etc/ssh/sshd_config'] 先執行
	}

意義同上

	# config.pp
	file { '/etc/ssh/sshd_config':
	  ensure  => file,
	  mode    => '0600',
	  source  => 'puppet:///modules/sshd/sshd_config',
	  require => Package['openssh-server'], # Pacage['openssh-server'] 必須執行才能使用 File['/etc/ssh/sshd_config']
	}


notify and subscribe example

	# config.pp
	file { '/etc/ssh/sshd_config':
	  ensure => file,
	  mode   => '0600',
	  source => 'puppet:///modules/sshd/sshd_config',
	  notify => Service['sshd'], # File['/etc/ssh/sshd_config'] 更新後會通知 Service['sshd'] 動作
	}

意義同上

	# service.pp
	 service { 'sshd':
	  ensure    => running,
	  enable    => true,
	  subscribe => File['/etc/ssh/sshd_config'], # Service['sshd'] 會去確認 File[''/etc/ssh/sshd_config'] 狀態而動作
	}

mixed example

	# service.pp
	service { 'sshd':
	  ensure  => running,
	  require => [
	    Package['openssh-server'],
	    File['/etc/ssh/sshd_config'],
	  ],
	}

意義同上

	# install.pp
	package { 'openssh-server':
	  ensure => present,
	  before => Service['sshd'],
	}

	# config.pp
	file { '/etc/ssh/sshd_config':
	  ensure => file,
	  mode   => '0600',
	  source => 'puppet:///modules/sshd/sshd_config',
	  before => Service['sshd'],
	}


#### Chaining Arrows ####

- ->

功能同 before

- ~>

功能同 notify

example1

	Package['ntp'] -> File['/etc/ntp.conf'] ~> Service['ntpd']

example2

	package { 'openssh-server':
	  ensure => present,
	} ->
	file { '/etc/ssh/sshd_config':
	  ensure => file,
	  mode   => '0600',
	  source => 'puppet:///modules/sshd/sshd_config',
	} ~>
	service { 'sshd':
	  ensure => running,
	  enable => true,
	}


#### Dependency ####

當 resource 間有相依性, 可使用 require 檢查

- require

example1

	class wordpress {
	  require apache
	  require mysql
	  ...
	}

example2

	class apache::ssl {
	  include site::certificates
	  Class['site::certificates'] ~> Class['apache::ssl']
	}


#### Refresh ####

通常 service, mount, exec 在狀態改變時, 只需要重新執行該 resource, 只要加上 refreshonly

- refreshonly


### Class ###

`Syntax`

	# A class with no parameters
	class base::linux {
	  file { '/etc/passwd':
	    owner => 'root',
	    group => 'root',
	    mode  => '0644',
	  }
	  file { '/etc/shadow':
	    owner => 'root',
	    group => 'root',
	    mode  => '0440',
	  }
	}

	# A class with parameters
	class apache (String $version = 'latest') { # String 是指定給定 argument type, 預設是 Any. = 是預設 argument 值
	  package {'httpd':
	    ensure => $version, # Using the class parameter from above
	    before => File['/etc/httpd.conf'],
	  }
	  file {'/etc/httpd.conf':
	    ensure  => file,
	    owner   => 'httpd',
	    content => template('apache/httpd.conf.erb'), # Template from a module
	  }
	  service {'httpd':
	    ensure    => running,
	    enable    => true,
	    subscribe => File['/etc/httpd.conf'],
	  }
	}

$title, $name 這兩個參數是自動為 class 名稱, 所以不能令為變數名稱


#### Inheritance ####

`Overriding Resource Attributes`

	class base::unix {
	  File['/path/file1'] {
	    group => 'root'
	  }
	  File['/path/file2'] {
	    group => 'root'
	  }
	}

	class base::freebsd inherits base::unix {
	  File['/path/file1'] {
	    group => 'wheel' # overriding attribute
	  }
	  File['/path/file2'] {
	    group => undef # remove attribute
	  }
	}


`Appending to Resource Attributes`

	class apache {
	  service {'apache':
	    require => Package['httpd'],
	  }
	}

	class apache::ssl inherits apache {
	  # host certificate is required for SSL to function
	  Service['apache'] {
	    require +> [ File['apache.pem'], File['httpd.conf'] ],
	    # Since `require` will retain its previous values, this is equivalent to:
	    # require => [ Package['httpd'], File['apache.pem'], File['httpd.conf'] ],
	  }
	}


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

manifests 底下存放 agent node 的資訊

	master:~ # touch /etc/puppet/modules/foo/manifests/{init.pp,config.pp,install.pp,service.pp,params.pp}
	master:~ # tree /etc/puppet/modules/foo/manifests
	/etc/puppet/modules/foo/manifests
	├── config.pp
	├── init.pp 
	├── install.pp
	├── params.pp
	└── service.pp

基本上只要有 init.pp 就可以, 一般針對不同的行為 可分類成 config, install, params, service 等檔案



`package`

	master:~ # cat /etc/puppet/modules/foo/manifests/install.pp 
	class foo::install{
	  file {
	    "/tmp/puppet.txt":
	    content => "test";
	  }
	
	  package { 'mlocate':
	    ensure => '0.26-5.el7',
	  }
	
	  package { 'tree':
	    ensure => installed,
	  }
	}

	master:~ # cat /etc/puppet/modules/foo/manifests/init.pp 
	class foo{
	  include foo::install
	}


### node ###

	master:~ # /etc/puppet/manifests/nodes/agent.test.com 
	node "agent.test.com" {
	  include foo
	}

	msater:~ # /etc/puppet/manifests/site.pp
	import 'nodes/agent.test.com'

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

* [Puppet 3.8 Reference Manual](https://docs.puppetlabs.com/puppet/3.8/reference/)