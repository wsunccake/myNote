# Environment #

RHEL (ad client)  ----  Widows Server (ad server)
192.168.0.10 			192.168.0.1/ad.contoso.com

client is necessary to resolve domain name (contoso.com in example, recommend setup dns)

	# network
	rhel:~ # cat /etc/resovl.conf
	search contoso.com # ad domain/realm
	nameserver 198.168.0.1


# SSSD #

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
	domains = ad.contoso.com
	services = nss, pam, pac

	[domain/ad.contoso.com]
	id_provider = ad
	auth_provider = ad
	chpass_provider = ad
	access_provider = ad

	rhel:~ # chmod 400 /etc/sssd/sssd.conf

	rhel:~ # systemctl start sssd


# realmd #

	rhel:~ # yum install realmd oddjob oddjob-mkhomedir sssd adcli

	rhel:~ # realm discover -v contoso.com
	rhel:~ # realm join contoso.com # 加入 domain/realm
	rhel:~ # realm join contoso.com -U contoso.com\jsmith # join ad with jsmith user
	rhel:~ # realm list
	rhel:~ # realm list --all --name-only
	rhel:~ # realm leave
	rhel:~ # realm leave ad.contoso.com # 離開 domain/realm
	rhel:~ # realm leave ad.contoso.com -U contoso.com\jsmith

	rhel:~ # realm permit --all
	rhel:~ # realm permit -a -R contoso.com
	rhel:~ # realm permit -x AD.EXAMPLE.COM\jsmith -R contoso.com 

	rhel:~ # getnet passwd

	rhel:~ # /etc/realmd.conf
	[users]
	default-home = /home/%u
	default-shell = /bin/bash
