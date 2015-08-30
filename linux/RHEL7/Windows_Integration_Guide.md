# Single Linux machine join Windows workgroup #


## Environment ##

RHEL (rhel)	 --------- 	 Widows Server (ws)
192.168.0.10 			 192.168.0.20


## Windows net command ##

| option 			 | description 											 |
| ------------------ | ----------------------------------------------------- |
| net view 			 | 顯示域列表, 電腦列表或指定電腦的共享資源列表 					 |
| net config 		 | 顯示當前執行的可配置服務或顯示並更改某項服務的設定 			 |
| net localgroup 	 | 增加, 顯示或更改本機組 									 |
| net group 		 | 在 Windows NT Server 域中增加、顯示或更改全局組 			 |
| net user 			 | 增加或更改用戶帳號或顯示用戶帳號信息 						 |
| net accounts 		 | 更新用戶帳號資料庫, 更改密碼及所有帳號的登入要求 				 |
| net use 			 | 連接電腦或中斷連線電腦與共享資源的連接, 或顯示電腦的連接信息 	 |
| net share 		 | 新增, 刪除或顯示共享資源 									 |
| net print 		 | 顯示或控制列印作業及列印貯列 								 |
| net time 			 | 使電腦的時間與另一台電腦或域的時間同步 						 |
| net start 		 | 啟動服務, 或顯示已啟動服務 								 |
| net stop 			 | 停止服務 												 |
| net continue 		 | 重新啟動掛起的服務 										 |
| net pause 		 | 暫停正在執行的服務 										 |
| net statistics 	 | 顯示本機服務統計記錄 									 |
| net session 		 | 列出或中斷連線本機電腦和與之連接的客戶端的 					 |
| net send 			 | 向網路的其他用戶, 電腦或通信名傳送消息 						 |
| net name 			 | 增加或刪除消息名( 有時也稱別名), 或顯示電腦接收消息的名稱列表 	 |
| net computer 		 | 從域資料庫中增加或刪除電腦 								 |


### net view ##

	C:\windows> net view /all
	C:\windows> net view # 顯示 workgroup 中的 member
	C:\windows> net view \\machaine # 顯示 machine
	C:\windows> net view //domain:workgroup # 顯示 machine


### net config ###

	C:\windows> net config workstation # 顯示工作站配置
	C:\windows> net config server # 顯示伺服器配置


### net localgroup ###
### net group ###

### net user ###

	C:\windows> net user # 顯示本機所有使用者
	C:\windows> net user newuser * /add # 新增使用者
	C:\windows> net user newuser /delete # 刪除使用者
	C:\windows> net user newuser * # 改密碼
	C:\windows> net user guest /active:no # 禁用帳號
	C:\windows> net user guest /active:yes # 啟用帳號


### net accounts ###
### net use ###

	C:\windows> net use # 顯示已掛載 shared folder
	C:\windows> net use Z: \\machaine\sharename # 掛載 shared folder
	C:\windows> net use /delelte # 卸載 shared folder


### net share ###

	C:\windows> net share # 顯示所有 shared folder
	C:\windows> net share sharename # 顯示 shared folder 設定
	C:\windows> net share sharename=Z:\shared_folder /grant:user,read|change|full # 新增 shared folder
	C:\windows> net share sharename /delete # 刪除 shared folder

### net print ###
### net time ###

	C:\windows> net time \\ntp_server


### net start ###

	C:\windows> net start
	C:\windows> net start "Theme"


### net stop ###

	C:\windows> net stop "Theme"


### net continue ###


## 免帳密 / 匿名 / guest 分享資料 ##

	C:\w1> net user guset /active:yes
	C:\w1> net share sharename=Z:\shared_folder /grant:everyone,read

	C:\w2> net view \\w1
	C:\w2> net use \\w1\sharename


## Samba Server ##


### package ###

	rhel:~ # yum install samba


### configuration ###

	rhel:~ # cat /etc/samba/smb.conf 
	[global] 
	        netbios name = workgroup
	        workgroup = Workgroup
	        security = share # user, server, domain, share 四選一
	        server string = Samba %v
	        wins support = Yes
	[netlogon] 
	        path = /tmp/share
	        comment = temp dir
	        browseable = Yes
	        read only = Yes
	        public = Yes

	rhel:~ # cat /etc/samba/lmhosts
	192.168.0.20       ws
	192.168.0.10       rhel


	rhel:~ # systemctl enable smb.service
	rhel:~ # systemctl start smb.service

### test ###

	net -l share -S samba_server
	net -l user -S samba_server

	nmblookup hostname

	pdbedit -a new_user
	pdbedit -v -L new_user

	rpcclient

	smbcacls //server/share filename
	smbcontrol -i
	smbpasswd
	smbspool
	smbstatus
	smbtar

	testparm

	wbinfo

## Samba Client ##


### package ###

	rhel:~ # yum install smbclient cifs-utils


### cli & confiugration ###

	# view shared folder
	rhel:~ # smbclient [-U Aministrator[%password]] -L samba_server

	# method 1: use smbclient cmd for user
	rhel:~ # smbclient [-U Administrator[%password]] //samba_server/Users

	# method 2: use mount utils for root
	rhel:~ # mount -t cifs -o user=Administrator,pass='password' //samba_server/Users /mnt/smb

	# method 3: use mount fstab for root
	rhel:~ # cat /etc/smb_info
	username=Administrator
	password=password
	rhel:~ # cat /etc/fstab
	\\\\samba_server\\Users    /mnt/smb    cifs    credentials=/etc/smb_info,uid=5000,gid=6000    0    0
	rhel:~ # mount -a



# Single Linux machaine join Windows AD domain #


## Environment ##

RHEL (ad client)  ----  Widows Server (ad server)
192.168.0.10 			192.168.0.1/ad.contoso.com

client is necessary to resolve domain name (contoso.com in example, recommend setup dns)

	# network
	rhel:~ # cat /etc/resolv.conf
	search contoso.com # ad domain/realm
	nameserver 198.168.0.1


## sssd and realmd ##

SSSD (System Security Services Daemon)
AD (Active Directory)
IdM (Identity Management)
HBAC (Host-Based Access Control) 
GPO (Group Policy Object)

Linux/Unix systems:  user ID (UID) and group ID number (GID)
Microsoft Windows Active Directory: Security Identifier (SID)

S-1-5-21-3623811015-3361044348-30300820-1013
reserve word: S
os version: 1

domain/machine id: 3623811015-3361044348-30300820
relative identifier (RID): 1013, 500 (Administrator), 501 (Guest)


### package ###

	rhel:~ # yum install realmd
	rhel:~ # yum install oddjob oddjob-mkhomedir
	rhel:~ # yum install sssd
	rhel:~ # yum install adcli
	rhel:~ # yum install samba-common


### CLI ###

	# realm command
	rhel:~ # realm discover -v contoso.com
	rhel:~ # realm discover -v ad.contoso.com
	rhel:~ # realm join contoso.com # 加入 domain/realm, 會自動修改 /etc/sssd/sssd.conf
	rhel:~ # realm join contoso.com -U contoso.com\administrator # join ad with administrator
	rhel:~ # realm list
	rhel:~ # realm list --all --name-only
	rhel:~ # realm leave
	rhel:~ # realm leave ad.contoso.com # 離開 domain/realm
	rhel:~ # realm leave ad.contoso.com -U contoso.com\administrator

	# login command
	rhel:~ # realm permit --all
	rhel:~ # realm permit -a -R contoso.com
	rhel:~ # realm permit user@contoso.com
	rhel:~ # realm permit -x AD.CONTOSO.COM\jsmith -R contoso.com 
	rhel:~ # realm demy --all

	# realmd configuration
	rhel:~ # /etc/realmd.conf
	[users]
	default-home = /home/%u
	default-shell = /bin/bash


### configuration ###

只要使用上述 realm 指令加入過 ad server, /etc/sssd/sssd.conf 設定檔會自動產生, 之後只需要使用 sssd 就可以開機時自動加入 ad server

	rhel:~ # cat /etc/sssd/sssd.conf
	[sssd]
	domains = contoso.com
	config_file_version = 2
	services = nss, pam
	
	[domain/contoso.com]
	ad_domain = contoso.com
	krb5_realm = CONTOSO.COM
	realmd_tags = manages-system joined-with-samba 
	cache_credentials = True
	id_provider = ad
	krb5_store_password_if_offline = True
	default_shell = /bin/bash
	ldap_id_mapping = True
	use_fully_qualified_names = True # 改為 False, 則不需要輸入 domain/realm
	fallback_homedir = /home/%d/%u

	rhel:~ # systemctl enable sssd
	rhel:~ # systemctl start sssd


### test ###

	# test ad account
	rhel:~ # id contoso.com\\administrator # 確認 AD 帳號使否存在
	rhel:~ # su - contoso.com\\administrator
	rhel:~ # ssh -lcontoso.com\\administrator localhost


## winbind ##


### package ###

	rhel:~ # yum install samba-winbind samba-winbind-clients samba-winbind-krb5-locator
	rhel:~ # yum isntall pam_krb5 krb5-workstation


### CLI ###

	rhel:~ # authconfig 
	\ --enablewinbind --enablewins # nss
	\ --enablewinbindauth  --enablemkhomedir # pam
	\ --smbsecurity ads --smbworkgroup=CONTOSO --smbrealm CONTOSO.COM # samba
	\ --smbservers=ad.contoso.com --krb5realm=CONTOSO.COM # kerberbos
	\ --enablewinbindoffline --enablewinbindkrb5 --winbindtemplateshell=/bin/sh # winbind
	\ --winbindjoin=Administrator --update --enablelocauthorize # general

	rhel:~ # net join -w CONTOSO -S ad.contoso.com -U Administrator # 執行 authconfig, 會自動執行此指令

	rhel:~ # systecmctl enable winbind
	rhel:~ # systecmctl start winbind

在執行 authoconfig 時可加 --savebackup=/backups, 先將所有會用到的設定檔備份


### configuration ###

執行上述步驟, 就是設定底下這些服務

	# samba
	rhel:~ # cat /etc/samba/smb.conf
	[global]
	  workgroup = CONTOSO # NetBIOS 名稱
	  security = ads
	  realm = CONTOSO.COM
	  password server = ad.contoso.com

	  idmap config * : range = 16777216-33554431
	  template shell = /bin/sh
	  template homedir = /home/%D/%U
	  kerberos method = secrets and keytab
	  winbind use default domain = false # true 則不顯示 domain/realm
	  winbind offline logon = true
	  winbind separator = +
	  winbind enum users = yes # 在 getnet passwd 顯示 ad user
	  winbind enum groups = yes # 在 getnet passwd 顯示 ad group
	  ...

	# kerberos
	rhel:~ # cat /etc/krb5.conf
	...
	[libdefaults]
	  default_realm = CONTOSO.COM # ad domain/realm, 須用大寫
	...

	[realms]
	  CONTOSO.COM = {
	    kdc = ad.contoso.com
	  }
	...

	[domain_realm]
	  contoso.com = CONTOSO.COM
	  .contoso.com = CONTOSO.COM
	...

	# dns
	rhel:~ # cat /etc/resolv.conf
	nameserver 192.168.0.1
	search contoso.com

	# pam
	rhel:~ # cat /etc/pam.d/system-auth
	auth        required      pam_env.so
	auth        sufficient    pam_unix.so nullok try_first_pass
	auth        requisite     pam_succeed_if.so uid >= 500 quiet
	auth sufficient pam_winbind.so use_first_pass
	auth        required      pam_deny.so

	account     required      pam_unix.so broken_shadow
	account     sufficient    pam_localuser.so
	account     sufficient    pam_succeed_if.so uid < 500 quiet
	account [default=bad success=ok user_unknown=ignore] pam_winbind.so
	account     required      pam_permit.so

	password    requisite     pam_cracklib.so try_first_pass retry=3 type=
	password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok
	password sufficient pam_winbind.so use_authtok
	password    required      pam_deny.so

	session     optional      pam_keyinit.so revoke
	session     required      pam_limits.so
	session     [success=1 default=ignore] pam_succeed_if.so service in crond quiet use_uid
	session     required      pam_unix.so
	session     optional      pam_krb5.so
	session optional pam_winbind.so use_first_pass
	session required pam_mkhomedir.so skel=/etc/skel/ umask=0022

	rhel:~ # cat /etc/security/pam_winbind.conf

	# nss
	rhel:~ # cat /etc/nsswitch.conf
	passwd:     files winbind
	shadow:     files winbind
	group:      files winbind

	hosts:      files dns wins


### GUI ###

	rhel:~ # authconfig-gtk


### test ###

	# 使用 krb5-workstation 測試 domain/realm
	rhel:~ # klist # 顯示 tgt
	rhel:~ # kinit Administrator # 取得 tgt
	rhel:~ # kdestroy # 刪除 tgt

	# 使用 samba-common 測試 domain/realm
	rhel:~ # net ads info
	rhel:~ # net ads join -U Administrator 
	rhel:~ # net ads leave -U Administrator
	rhel:~ # net ads join -k # create /etc/krb5.keytab
	rhel:~ # net ads leave -k 

	# 測試 ad server
	rhel:~ # wbinfo -u # 顯示 ad user
	rhel:~ # wbinfo -g # 顯示 ad group
	rhel:~ # wbinfo -a user # 測試 ad user 帳密

	# 測試帳號
	rhel:~ # id administrator
	rhel:~ # getent passwd # 確認使用這是否在 linux 主機
	rhel:~ # su - administrator


# Linux IdM domain integer with Widnows AD domain #

Domain and Realm Names
The IdM DNS domain name and Kerberos realm name must be different than the Active Directory DNS domain name and Kerberos realm name.

NetBIOS Names
The NetBIOS name is the far-left component of the domain name. For example, if the domain is linux.example.com, the NetBIOS name is linux

Integrated DNS
Both the Active Directory server and the IdM server must be configured to run their own respective DNS services.

Integrated Certificate Authorities
Both Active Directory and Identity Management must be configured with integrated certificate services.

## Firewalls and Ports ##


| Service 		 | Ports 	 | Type 		 |
| -------------- | --------- | ------------- |
| NetBIOS-DGM 	 | 138 		 | TCP and UDP 	 |
| NetBIOS-SSN 	 | 139 		 | TCP and UDP 	 |
| LDAP 			 | 389 		 | UDP 			 |
| Microsoft-DS 	 | 445 		 | TCP and UDP 	 |

	rhel:~ # systemctl start firewalld.service
	rhel:~ # systemctl enable firewalld.service
	rhel:~ # firewall-cmd --permanent --add-port={80/tcp,443/tcp,389/tcp,636/tcp,88/tcp,464/tcp,53/tcp,88/udp,464/udp,53/udp,123/udp} # for IdM
	rhel:~ # firewall-cmd --permanent --add-port={138/tcp,139/tcp,445/tcp,138/udp,139/udp,389/udp,445/udp} # for trust relationship
	rhel:~ # firewall-cmd --reload


## IdM Group ##


	rhel:~ # ipa group-add --desc='AD users external map' ad_users_external --external # external IdM group for AD
	rhel:~ # ipa group-add-member ad_users_external --external "AD\Domain Users" # add ad group/member to external IdM group
	rhel:~ # ipa group-add --desc='AD users' ad_users # IdM group for POSIX
	rhel:~ # ipa group-add-member ad_users --groups ad_users_external # # add external IdM group to IdM POSIX group


`Changing the NetBIOS Name`

	ipa-adtrust-install --netbios-name=NEWBIOSNAME -a secret


`Changing the Default Group for Windows Users`

	kinit admin
	ipa trustconfig-mod --fallback-primary-group="Example Windows Group"

https://ipaserver.example.com


`Discovering, Enabling, and Disabling Trust Domains`

	kinit admin

	ipa trust-fetch-domains adexample.com
	ipa trustdomain-disable test.adexample.com
	ipa trustdomain-del prod.adexample.com


`Viewing and Managing DNS Realms`

	kinit admin
	ipa realmdomains-show
	ipa realmdomains-mod --add-domain=adexample.com
	ipa realmdomains-mod --domain={ipa.example.org,adexample.com}


`Adding Ranges for UID/GID Numbers in a Transitive Trust`

	kinit admin
	ipa idrange-add --base-id=1200000 --range-size=200000 --rid-base=0 --dom-sid=S-1-5-21-123-456-789 trusted_dom_range