# Environment #

RHEL (ad client)  ----  Widows Server (ad server)
192.168.0.10 			192.168.0.1/ad.contoso.com

client is necessary to resolve domain name (contoso.com in example, recommend setup dns)

	# network
	rhel:~ # cat /etc/resovl.conf
	search contoso.com # ad domain/realm
	nameserver 198.168.0.1


# sssd #

SSSD (System Security Services Daemon) provides access to different identity and authentication providers. This service ties a local system to a larger back-end system. That can be a simple LDAP directory, domains for AD (Active Directory) or IdM (Identity Management) in Red Hat Enterprise Linux, or Kerberos realms. Authorization information is gathered by SSSD by using HBAC (Host-Based Access Control) in IdM and GPO (Group Policy Object) in AD.


SSSD replaces older identity management services (NIS and Winbind, etc)

Linux/Unix systems:  user ID (UID) and group ID number (GID)
Microsoft Windows Active Directory: Security Identifier (SID)


S-1-5-21-3623811015-3361044348-30300820-1013
reserve word: S
os version: 1

domain/machine id: 3623811015-3361044348-30300820
relative identifier (RID): 1013, 500 (Administrator), 501 (Guest)

	# kerberos service
	rhel:~ # krb5-libs
	rhel:~ # cat /etc/krb5.conf
	[logging]
	 default = FILE:/var/log/krb5libs.log
	
	[libdefaults]
	 default_realm = CONTOSO.COM # ad domain/realm, 須用大寫
	 dns_lookup_realm = true
	 dns_lookup_kdc = true
	 ticket_lifetime = 24h
	 renew_lifetime = 7d
	 rdns = false
	 forwardable = yes

	# samba service
	rhel:~ # yum install samba
	rhel:~ # cat /etc/samba/smb.conf
	[global]
	   workgroup = CONTOSO # NetBIOS 名稱
	   client signing = yes
	   client use spnego = yes
	   kerberos method = secrets and keytab
	   log file = /var/log/samba/%m.log
	   password server = ad.contoso.com # ad server
	   realm = contoso.com # ad domain/realm
	   security = ads

	# init tgt
	rhel:~ # yum install krb5-workstation
	rhel:~ # kinit Administrator # 新增 TGT
	rhel:~ # klist # 顯示 TGT
	rhel:~ # kdestroy # 刪除 TGT

	rhel:~ # net ads join -k # /etc/krb5.keytab
	rhel:~ # net ads leave -k 

	#
	rhel:~ # yum install oddjob-mkhomedir
	rhel:~ # authconfig --update --enablesssd --enablesssdauth --enablemkhomedir

	#
	rhel:~ # yum install sssd
	rhel:~ # cat /etc/sssd/sssd.conf
	[sssd]
	config_file_version = 2
	domains = contoso.com
	services = nss, pam, pac

	[domain/ad.contoso.com]
	id_provider = ad
	auth_provider = ad
	chpass_provider = ad
	access_provider = ad

	rhel:~ # chmod 400 /etc/sssd/sssd.conf

	rhel:~ # systemctl start sssd


# realmd #


## package ##

	rhel:~ # yum install realmd
	rhel:~ # yum install oddjob oddjob-mkhomedir
	rhel:~ # yum install sssd
	rhel:~ # yum install adcli
	rhel:~ # yum install samba-common


## CLI ##

	# realm command
	rhel:~ # realm discover -v contoso.com
	rhel:~ # realm join contoso.com # 加入 domain/realm, 會自動修改 /etc/sssd/sssd.conf
	rhel:~ # realm join contoso.com -U contoso.com\jsmith # join ad with jsmith user
	rhel:~ # realm list
	rhel:~ # realm list --all --name-only
	rhel:~ # realm leave
	rhel:~ # realm leave ad.contoso.com # 離開 domain/realm
	rhel:~ # realm leave ad.contoso.com -U contoso.com\jsmith

	# login command
	rhel:~ # realm permit --all
	rhel:~ # realm permit -a -R contoso.com
	rhel:~ # realm permit user@contoso.com
	rhel:~ # realm permit -x AD.EXAMPLE.COM\jsmith -R contoso.com 
	rhel:~ # realm demy --all

	rhel:~ # /etc/realmd.conf
	[users]
	default-home = /home/%u
	default-shell = /bin/bash


# winbind #


## package ##

	rhel:~ # yum install samba-winbind samba-winbind-clients samba-winbind-krb5-locator
	rhel:~ # yum isntall pam_krb5 krb5-workstation


## configuration ##

	# samba
	rhel:~ # cat /etc/samba/smb.conf
	[global]
	  workgroup = CONTOSO
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
	  default_realm = CONTOSO.COM
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

	# nns
	rhel:~ # cat /etc/nsswitch.conf
	passwd:     files winbind
	shadow:     files winbind
	group:      files winbind

	hosts:      files dns wins


## CLI ##

	rhel:~ # authconfig 
	\ --enablewinbind --enablewins # nns
	\ --enablewinbindauth  --enablemkhomedir # pam
	\ --smbsecurity ads --smbworkgroup=CONTOSO --smbrealm CONTOSO.COM # samba
	\ --smbservers=ad.contoso.com --krb5realm=CONTOSO.COM # kerberbos
	\ --enablewinbindoffline --enablewinbindkrb5 --winbindtemplateshell=/bin/sh # winbind
	\ --winbindjoin=Administrator --update --enablelocauthorize # general

	rhel:~ # net join -w CONTOSO -S ad.contoso.com -U Administrator # 執行 authconfig, 會自動執行此指令

	rhel:~ # systecmctl enable winbind
	rhel:~ # systecmctl start winbind

	# 使用 krb5-workstation 測試 domain/realm
	rhel:~ # klist
	rhel:~ # kinit Administrator # 取得 tgt
	rhel:~ # kdestroy

	# 使用 samba-common 測試 domain/realm
	rhel:~ # net ads info
	rhel:~ # net ads join -U Administrator 
	rhel:~ # net ads leave -U Administrator

	# 測試 ad server
	rhel:~ # wbinfo -u # 顯示 ad user
	rhel:~ # wbinfo -g # 顯示 ad group
	rhel:~ # wbinfo -a user # 測試 ad user 帳密
	rhel:~ # getent passwd # 確認使用這是否在 linux 主機

在執行 authoconfig 可加 --savebackup=/backups, 先將所有會用到的設定檔備份


## GUI ##

	rhel:~ # authconfig-gtk