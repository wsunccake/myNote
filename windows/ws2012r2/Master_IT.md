# 首次安裝 #


## 換序號 ##

	PS C:\Users\Administrator> dism /online /Get-TargetEditions
	PS C:\Users\Administrator> dism /online /Set-Edition:ServerStandard /ProductKey:M98WF-NY2PP-73243-PC8R6-V6B4Y /AcceptEula


## 設定 IP ##

	PS C:\Users\Administrator> ipconfig
	PS C:\Users\Administrator> ipconfig /?
	PS C:\Users\Administrator> ipconfig /all

	PS C:\Users\Administrator> netsh /?
	PS C:\Users\Administrator> netsh interface ipv4 set address ethernet0 static 192.168.0.1 255.255.255.0 192.168.0.1 # 設定 static ip
	PS C:\Users\Administrator> netsh interface ipv4 set dns ethernet0 static 192.168.0.1 # 設定 dns

	PS C:\Users\Administrator> netsh interface ipv4 set address ethernet0 dhcp # 設定 dynamic ip


## 主機名稱 ##

	PS C:\Users\Administrator> hostname # 顯示當前主機名稱
	PS C:\Users\Administrator> netdom /renamecomputer old_hostname /newname:new_hostname # 改變主機名稱


## 加入網域 ##

	PS C:\Users\Administrator> netdom join bigfirmappsvr1 /Domain: contoso.com /UserD:contoso\administrator /PasswordD:* # 加入網域
	PS C:\Users\Administrator> netdom join bigfirmappsvr1 /Domain: contoso.com /UserD:contoso\administrator /PasswordD:* /REBoot # 加入網域後自動重開機


## Server Manager ##

	PS C:\Users\Administrator> import-module Servermanager
	PS C:\Users\Administrator> Get-WindowsFeature | more # 顯示已安裝 service
	PS C:\Users\Administrator> Install-WindowsFeature –Name Web-Ftp-Server -Restart # 安裝 service
	PS C:\Users\Administrator> Get-WindowsFeature | findstr \I ftp
	PS C:\Users\Administrator> Remove-WindowsFeature Web-Ftp-Server -Restart # 移除 service


# Server Core #


## Accessing Task Manager ##

Ctrl+Alt+Del

Ctrl+Shift+Esc

## Help ##

	PS C:\Users\Administrator> Get-Help Get-Host # 指令說明
	PS C:\Users\Administrator> Get-Host # PowerShell 版本


## 關機 ##

	PS C:\Users\Administrator> Restart-Computer # 重開機
	PS C:\Users\Administrator> Stop-Computer # 關機


## 改變管理員密碼 ##

	PS C:\Users\Administrator> net user administrator * # 換密碼


## Telnet server ##

	PS C:\Users\Administrator> Install-WindowsFeature Telnet-Server
	PS C:\Users\Administrator> net start Telnet


## FTP server ##

	PS C:\Users\Administrator> Install-WindowsFeature Ftp-Server
	PS C:\Users\Administrator> New-WebFTPSite -Name FTPTest -Port 21 -PhysicalPath D:\FTPTest
	PS C:\Users\Administrator> Get-ChildItem IIS:\Sites 


## 安裝 Windows Server GUI ##
	C:\Users\Administrator> powershell
	PS C:\Users\Administrator> Get-WindowsImage -ImagePath d:\source\install.wim
	PS C:\Users\Administrator> Install-WindowsFeature Server-Gui-Mgmt-Inftra,Server-Gui-Shell -Restart -Source wim:d:\source\install.wim:3


## 啟動 Hyper-V ##

	PS C:\Users\Administrator> bcbedit
	PS C:\Users\Administrator> bcbedit /set (current) hypervisorlaunchtype auto


## 其他 ##

	PS C:\Users\Administrator> sconfig


### FTP ###
1. 安裝 Web Server (IIS) 底下選 FTP
2. 開啟 Internet Information Services (IIS) Manager
click Sites 圖示, Add FTP Site...

### 共享檔案 ###
Control Panel -> Network and Internet -> Network and Sharing Center
Ethernet NIC \ Proerties\ click File and Printer Sharing for Microsoft Networks

Control Panel -> Network and Internet -> Network and Sharing Center
Change advanced sharing settings

在要分享的資料夾上 click right, 選 Properties, 然後 Sharing 設定


Mac 連接 Windows SMB
smbutil view [connection options] //[domain;][user[:password]@]server