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