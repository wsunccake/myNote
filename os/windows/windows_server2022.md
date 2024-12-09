# windows server 2022

## begin

### version

```powershell
# cli
PS> ver
PS> systeminfo
PS> Get-ComputerInfo

# gui
PS> winver
```

### activate

```powershell
PS> DISM /Online /Get-CurrentEdition        # Current Edition
PS> DISM /Online /Get-TargetEditions        # Target Edition
PS> Get-ComputerInfo
PS> DISM /Online /Get-CurrentEdition | Select-String 'Current Edition :'
PS> DISM /Online /Get-TargetEditions | Select-String 'Target Edition :'
PS> Get-ComputerInfo | Select-Object WindowsProductName, WindowsEditionId

# activate
PS> DISM /Online /Set-Edition:<Target Edition> /ProductKey:XXXXX-XXXXX-XXXXX-XXXXX-XXXXX /AcceptEula
```

| Operating system edition       | Generic Volume License Key (GVLK) |
| ------------------------------ | --------------------------------- |
| Windows Server 2022 Standard   | VDYBN-27WPP-V4HQT-9VMD4-VMK7H     |
| Windows Server 2022 Datacenter | WX4NM-KYWYW-QJJR4-XV3QB-6VM33     |

### KMS

```powershell
PS> slmgr.vbs /skms                                 # check KMS
PS> slmgr.vbs /skms <KMS_Server>                    # set KMS
PS> slmgr.vbs /dli                                  # verify KMS
PS> slmgr.vbs /ato                                  # activate windows using KMS
PS> slmgr.vbs /ckms                                 # clear KMS configuration
PS> slmgr.vbs /xpr                                  # show activation expiration
PS> slmgr.vbs /ipk XXXXX-XXXXX-XXXXX-XXXXX-XXXXX    # set product key
```

- [KMS](https://kms.netnr.eu.org/)

### shutdown

```powershell
PS> shutdown /s [/t 0] [/f]
PS> shutdown /r [/t 0] [/f]

PS> Stop-Computer
PS> Restart-Computer
```

### runas

```powershell
PS> runas /user:<domain>\<user> "<cmd>"
PS> runas /user:Administrator whoami
```

### network

```powershell
PS> ipconfig /all

PS> Get-NetIPInterface
PS> Get-NetIPAddress

# dhcp / dynamic ip
PS> netsh interface ip set address name="Ethernet" source=dhcp
PS> netsh interface ip set dns name="Ethernet" source=dhcp

PS> Set-NetIPInterface [-ifAlias "Ethernet" | -InterfaceIndex 12] -Dhcp Enabled
PS> Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ResetServerAddresses
# InterfaceAlias -> ifAlias
# InterfaceIndex -> ifIndex

# static ip
PS> netsh interface ip set address name="Ethernet" static 192.168.1.100 255.255.255.0 192.168.1.1
PS> netsh interface ip set dns name="Ethernet" static 8.8.8.8
PS> netsh interface ip add dns name="Ethernet" 8.8.4.4 index=2

PS> Set-NetIPInterface [-ifAlias "Ethernet" | -ifIndex 12] -Dhcp Disabled
PS> New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.1.100 -PrefixLength 24 -DefaultGateway 192.168.1.1
PS> Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 8.8.8.8,8.8.4.4

# connection profile
PS> Get-NetConnectionProfile
PS> Set-NetConnectionProfile -Name "Network" -NetworkCategory Private

# firewall
PS> Get-NetFirewallRule

PS> netsh advfirewall firewall add rule name="Allow ICMPv4-In" protocol=icmpv4:8,any dir=in action=allow
PS> netsh advfirewall firewall add rule name="Allow ICMPv6-In" protocol=icmpv6:8,any dir=in action=allow

PS> Enable-NetFirewallRule -Name "FPS-ICMP4-ERQ-In"
PS> Enable-NetFirewallRule -Name "FPS-ICMP6-ERQ-In"
```

---

## remote

### sshd

service: sshd
port: 22

```powershell
# install ssh service
PS> Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
PS> Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# setup ssh service
PS> Set-Service -Name sshd -StartupType Automatic
PS> Start-Service sshd
PS> Get-Service sshd
PS> Get-WmiObject -Class Win32_Service -Filter "Name='sshd'" | Select-Object Name, StartMode

# setup firewall
PS> Get-NetFirewallRule | Where-Object DisplayName -like "OpenSSH*"
PS> Enable-NetFirewallRule -Name "OpenSSH-Server-In-TCP"

# if not ssh rule
PS> New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (TCP-In)" -Protocol TCP -LocalPort 22 -Action Allow -Direction Inbound
```

### remote desktop

```powershell
PS> Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\' -Name "fDenyTSConnections"
PS> Get-NetFirewallRule -DisplayGroup "Remote Desktop"

PS> Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server\' -Name "fDenyTSConnections" -Value 0
PS> Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

### Windows Admin Center / WAC

### Remote Server Administration Tools / RSAT

---

## manage

### password

```powershell
PS> net user <username> <password>

PS> Set-LocalUser -Name "<username>" -Password (ConvertTo-SecureString "<password>" -AsPlainText -Force)
```

### account, group

```powershell
# list user & group
PS> net user
PS> net localgroup
PS> net localgroup <group>
PS> Get-LocalUser
PS> Get-LocalGroup
PS> Get-LocalGroupMember -Group <group>

# add user & group
PS> net user <username> <password> /ADD     # add user
PS> net localgroup <group> /ADD             # add group
PS> net localgroup <group> <username> /ADD  # add member to group

PS> New-LocalUser -Name "<username>"        # add user
PS> New-LocalGroup -Name "<group>"          # add group
PS> Add-LocalGroupMember -Group "<group>" -Member "<username>"  # add member to group

# del user & group
PS> net user <username> /DELETE
PS> net localgroup <group> /DELETE
PS> net localgroup <group> <username> /DELETE
PS> Remove-LocalUser -Name "<username>"
PS> Remove-LocalGroup -Name "<group>"
PS> Remove-LocalGroupMember -Group "<group>" -Member "<username>"

PS> Disable-LocalUser -Name "Administrator"

# gui
PS> ServerManager.exe
PS> compmgmt.msc
```

### hostname, workgroup

```powershell
PS> hostname
PS> net config workstation
PS> Get-ComputerInfo | Select-Object CsName, Domain, Workgroup

PS> wmic computersystem where name="%computername%" call rename name="<hostname>"
PS> netdom join %computername% /workgroup:<workgroup> /reboot
PS> netdom join %computername% /domain:<domain> /userD:DomainAdmin /passwordD:Password /reboot

PS> $env:COMPUTERNAME
PS> Rename-Computer -NewName "<host>" -Restart
PS> Add-Computer -WorkgroupName "<workgroup>" -Restart
PS> Add-Computer -DomainName "<domain>" -Credential Domain\Administrator -Restart

# gui
PS> sysdm.cpl
```

### date, time

```powershell
PS> Get-Date
PS> Get-TimeZone
PS> Get-TimeZone -ListAvailable

PS> Set-Date -Date "<YYYY-MM-DD> <HH:mm:ss>"
PS> Set-TimeZone -Name "<timezone>"
```

---

## service

```powershell
PS> dism /online /get-features
PS> dism /online /enable-feature /featurename:<feature>
PS> dism /online /disable-feature /featurename:<feature>

PS> Get-WindowsFeature
PS> Install-WindowsFeature -Name <feature>
PS> Uninstall-WindowsFeature -Name <feature>
```

### DHCP

```powershell
PS> Install-WindowsFeature -Name DHCP -IncludeManagementTools
PS> Get-DhcpServerv4Scope
PS> Get-DhcpServerv4Scope -ScopeId <ScopeID>
PS> Get-DhcpServerv4Reservation -ScopeId <ScopeID>
PS> Get-DhcpServerv4Lease -ScopeId <ScopeID>
PS> Get-DhcpServerv4OptionValue

# gui
PS> ServerManager.exe
Manage \ Add Roles and Features
Tools \ DHCP

PS> dhcpmgmt.msc
```

### DNS

```powershell
PS> Install-WindowsFeature -Name DNS -IncludeManagementTools
```

### AD

```powershell
PS> Install-WindowsFeature -Name AD-Domain-Services
```
