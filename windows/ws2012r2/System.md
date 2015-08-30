# 系統簡介 #


## 架構 ##

- workgroup

	peer-to-peer

- domain

	client / server


## 啟動 / boot ##

開機時, 按 F8 將進入 "進階開機選單" (或是使用 bcdedit.exe)


## 關機 / shutdown ##

	PS C:\Users\Administrator> logon.exe # 登出
	PS C:\Users\Administrator> shutdown.exe /s # 關機

	PS C:\Users\Administrator> Restart-Computer # 重開機
	PS C:\Users\Administrator> Stop-Computer # 關機


## 電腦名稱 / hostname ##

	PS C:\Users\Administrator> HOSTNAME.EXE # 顯示當前主機名稱

	PS C:\Users\Administrator> netdom.exe help
	PS C:\Users\Administrator> netdom.exe renamecomputer old_hostname /newname:new_hostname # 改變主機名稱


## 使用者 / user ##

	PS C:\Users\Administrator> whoami.exe # 顯示當前使用者
	PS C:\Users\Administrator> whoami.exe /all # 顯示當前使用者所有資訊
	PS C:\Users\Administrator> runas.exe /user:Administrator powershell # 以 Administrator 權限執行


## 改密碼 / password ##

	PS C:\Users\Administrator> net.exe user user * # 改密碼


## 序號 / serial number ##

	PS C:\Users\Administrator> Dism.exe /Online /Get-CurrentEdition # 顯示當前版本
	PS C:\Users\Administrator> Dism.exe /Online /Get-TargetEditions # 可設定之版本
	PS C:\Users\Administrator> Dism.exe /online /Set-Edition:ServerStandard /ProductKey:M98WF-NY2PP-73243-PC8R6-V6B4Y /AcceptEula # 改序號


# 網路設定 / network #


## 網卡設定 / nic ##

APIPA(Automatic Private IP Addressing) 169.254.0.0/16

	PS C:\Users\Administrator> ipconfig.exe # 顯示 NIC
	PS C:\Users\Administrator> ipconfig.exe /?
	PS C:\Users\Administrator> ipconfig.exe /all

	PS C:\Users\Administrator> netsh.exe /?
	PS C:\Users\Administrator> netsh.exe interface ipv4 set address ethernet0 static 192.168.0.1 255.255.255.0 192.168.0.1 # 設定 static ip
	PS C:\Users\Administrator> netsh.exe interface ipv4 set dns ethernet0 static 192.168.0.1 # 設定 dns

	PS C:\Users\Administrator> netsh.exe interface ipv4 set address ethernet0 dhcp # 設定 dynamic ip

	PS C:\Users\Administrator> PING.EXE 8.8.8.8 # 測試網路
	PS C:\Users\Administrator> Test-Connection 8.8.8.8

	PS C:\Users\Administrator> ARP -a # 顯示 arp table

	PS C:\Users\Administrator> ROUTE.EXE PRINT # routing table

	New-NetIPAddress
	Get-NetIPAddress
	Set-NetIPAddress
	New-NetIPInterface
	Get-NetIPInterface
	Set-NetIPInterface


## 防火牆 / firewall ##

	PS C:\Users\Administrator> netsh.exe firewall show # 顯示防火牆設定
	PS C:\Users\Administrator> netsh.exe advfirewall show currentprofile


## 網路位置 / network location ##

	PS C:\Users\Administrator> Get-NetConnectionProfile # 顯示當前網路位置
	PS C:\Users\Administrator> Set-NetConnectionProfile -NetworkCategory Public|Private


## 網域 / domain ##

	PS C:\Users\Administrator> netdom.exe join machine /Domain: contoso.com /UserD:contoso\administrator /PasswordD:* # 加入網域
	PS C:\Users\Administrator> netdom.exe join machine /Domain: contoso.com /UserD:contoso\administrator /PasswordD:* /REBoot # 加入網域後自動重開機


## 網路芳鄰 ##

`workgroup info`

	PS C:\Users\Administrator> net.exe config workstation
	PS C:\Users\Administrator> net.exe config server


`workgroup setup`

	PS C:\Users\Administrator> WMIC.exe ComputerSystem Set Workgroup= "NewWorkGroup" # 更改 workgroup


`NetBIOS info`

	PS C:\Users\Administrator> nbtstat.exe -n # 本機 NetBIOS 設定
	PS C:\Users\Administrator> nbtstat.exe -a machine
	PS C:\Users\Administrator> nbtstat.exe -A machine


`SMB info`

	PS C:\Users\Administrator> net.exe view /all # 顯示 workgroup 中的主機
	PS C:\Users\Administrator> net.exe view machine # 顯示主機名稱 machine


`mount/umount CIFS`

	PS C:\Users\Administrator> net.exe use Z: \\machine\shered_folder # mount
	PS C:\Users\Administrator> net.exe use Z: /delete # umount


`share folder`

	PS C:\Users\Administrator> net.exe share myshare=C:\Users\shared_folder


# 使用者 / 群組 / user / group #


## Guest 帳號 / guest account ##

	PS C:\Users\Administrator> net.exe user guest # 顯示帳號狀態
	PS C:\Users\Administrator> net.exe user guest /ACTIVIE:YES # 啟用 Guest 帳號
	PS C:\Users\Administrator> net.exe user guest /ACTIVIE:NO # 關閉 Guest 帳號
	PS C:\Users\Administrator> net.exe user guest * # 設定密碼
	PS C:\Users\Administrator> net.exe user guest "" # 移除密碼


## 帳號管理 / user account management ##

windows 的帳號主要是以 SID 作為區別

	PS C:\Users\Administrator> net.exe user new_user * /add # 新增使用者
	PS C:\Users\Administrator> net.exe user new_user /delete # 刪除使用者
	PS C:\Users\Administrator> net.exe user # 顯示所有使用者帳號
	PS C:\Users\Administrator> WMIC.exe useraccount list brief
	PS C:\Users\Administrator> WMIC.exe useraccount where "Name='new_user'" get SID


## 群組 / group ##

localgroup 和 group 不一樣, localgroup 指的是本機上的 (localhost) group, group 指的是網域上的 (domain/realm) group

	PS C:\Users\Administrator> net.exe localgroup # 顯示所有群組
	PS C:\Users\Administrator> net.exe localgroup new_group /add # 新增群組
	PS C:\Users\Administrator> net.exe localgroup new_group /delete # 刪除群組
	PS C:\Users\Administrator> net.exe localgroup new_group new_user /add # 將使用者加入群組
	PS C:\Users\Administrator> net.exe localgroup new_group new_user /delete # 將使用者從群組中移除


## 群組原則 / GPO (Group Policy Objects) ##

	gpresutl.exe /V
	gpresutl.exe /R
	gpresutl.exe /Z	


	gpupdate.exe


	PS C:\Users\Administrator> gpedit.msc


# 檔案管理 #

	PS C:\Users\Administrator> cacls.exe
	PS C:\Users\Administrator> icacls.exe


# 安裝 #

## Feature ##

	PS C:\Users\Administrator> import-module Servermanager
	PS C:\Users\Administrator> Get-WindowsFeature | more # 顯示已安裝 service
	PS C:\Users\Administrator> Install-WindowsFeature –Name Web-Ftp-Server -Restart # 安裝 service
	PS C:\Users\Administrator> Get-WindowsFeature | findstr \I ftp
	PS C:\Users\Administrator> Remove-WindowsFeature Web-Ftp-Server -Restart # 移除 service


# 磁碟 / Disk #

	PS C:\Users\Administrator> diskpart.exe
	DISKPART> list disk
	DISKPART> select disk 0
	DISKPART> list partition
	DISKPART> quit


## 公用資料夾 ##


	net share Users=C:\Users /GRANT:Everyone,FULL
	netsh advfirewall firewall set rule group=”File and Printer Sharing” new enable=Yes



