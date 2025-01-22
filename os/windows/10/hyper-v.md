# hyper-v

## install

gui

```batch
:: 開啟 "windows 功能" 後點選 "Hyper-V"
C:\Users\user> optionalfeatures

C:\Users\user> virtmgmt.msc
```

cli

```powershell
# install hyper-v
PS C:\Users\user> Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

PS C:\Users\user> Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -like "*Hyper-V*"}
```

## VM

```powershell
PS C:\Users\user> Get-VM

PS C:\Users\user> New-VM -Name <vm> -MemoryStartupBytes 2GB -Generation 2 -NewVHDPath <vm>.vhdx -NewVHDSizeBytes 50GB

PS C:\Users\user> Start-VM -Name <vm>
PS C:\Users\user> Stop-VM -Name <vm>
PS C:\Users\user> Remove-VM -Name <vm> -Force
PS C:\Users\user> Get-VM -Name <vm>
PS C:\Users\user> Rename-VM -Name <old_vm> -NewName <new_vm>
```

---

## network

```powershell
# create NAT on vSwitch
PS C:\Users\user> Get-NetAdapter
PS C:\Users\user> New-NetIPAddress -IPAddress <ip> -PrefixLength <preifx> [-InterfaceAlias <name>| -InterfaceIndex <ifIndex>]
PS C:\Users\user> New-NetNat -Name NatNetwork -InternalIPInterfaceAddressPrefix 192.168.100.0/24
```
