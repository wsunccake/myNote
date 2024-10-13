# Puppet Language #


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


## Ref ##

* [Puppet 實戰](http://www.m.sanmin.com.tw/Product/index/99M155F6c102e39c109H72T108R127CAIuHGm513IbM)

* [Puppet 3.8 Reference Manual](https://docs.puppetlabs.com/puppet/3.8/reference/)