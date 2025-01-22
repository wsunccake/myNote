# power shell

## content

- [basic](#basic)
  - [run](#run)
  - [command](#help)
  - [member](#member)
  - [run](#run)
  - [profile](#profile)
- [object-oriented scripting](#object-oriented-scripting)
  - [pipeline](#pipeline)
  - [format](#format)
  - [alias](#alias)
  - [provider](#provider)
  - [comparison](#comparison)
- [common](#common)
  - [variable](#variable)

---

## basic

### version

```powershell
PS C:\Users\user> $PSVersionTable
# 5.x -> powershell
# 7.x -> pwsh
```

### help

```powershell
PS C:\Users\user> Get-Help <cmd> [-Full|-Online]
PS C:\Users\user> Get-Help Where-Object -Full
PS C:\Users\user> Get-Help *process*
PS C:\Users\user> Get-Help process
```

### command

```powershell
PS C:\Users\user> Get-Command
PS C:\Users\user> Get-Command *process*
PS C:\Users\user> Get-Command process

PS C:\Users\user> Start-Process <cmd> -Verb runas
```

### member

```powershell
PS C:\Users\user> Get-Service -Name w32time
PS C:\Users\user> Get-Service -Name w32time | Get-Member [-MemberType Method]
PS C:\Users\user> Get-Service -Name w32time | Select-Object -Property *
PS C:\Users\user> Get-Service -Name w32time | Select-Object -Property Status, Name, DisplayName, ServiceType

PS C:\Users\user> Start-Service -Name w32time
PS C:\Users\user> Stop-Service -Name w32time
PS C:\Users\user> (Get-Service -Name w32time).Stop()
```

### run

```powershell
# run as inactive mode
PS C:\Users\user> echo "Hello PowerShell"
PS C:\Users\user> Get-Service -Name W32Time

# get/set current policy
PS C:\Users\user> Get-ExecutionPolicy [-List]
PS C:\Users\user> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned [-Scope CurrentUser]
# ExecutionPolicy: Restricted, AllSigned, RemoteSigned, Unrestricted, Bypass, Undefined
# Scope: MachinePolicy, UserPolicy, Process,CurrentUser, LocalMachine

# run as script
PS C:\Users\user> ./hello.ps1
```

```powershell
# hello.ps1
echo "Hello PowerShell"
```

### profile

```powershell
PS C:\Users\user> $HOME\Documents\PowerShell\profile.ps1

PS C:\Users\user> $PROFILE.AllUsersAllHosts
```

---

## object-oriented scripting

### pipeline

```powershell
PS C:\Users\user> Get-Service |
    Where-Object CanPauseAndContinue -eq $true |
    Select-Object -Property *
```

| situation | natural line symbol |
| ------------- | -PS C:\Users\user> ------------------ |
| common | , [ { ( |
| other | ; = |
| controversial | ` |

filter Left

```powershell
PS C:\Users\user> Get-Service -Name w32time
PS C:\Users\user> Get-Service | Where-Object Name -eq w32time

PS C:\Users\user> Stop-Service w32time
PS C:\Users\user> Get-Service -Name w32time
PS C:\Users\user> 'w32time' | Stop-Service
PS C:\Users\user> Get-MrPipelineInput -Name Stop-Service | Format-List

PS C:\Users\user> Get-Service |
    Select-Object -Property DisplayName, Running, Status |
    Where-Object CanPauseAndContinue
PS C:\Users\user> Get-Service |
    Where-Object CanPauseAndContinue |
    Select-Object -Property DisplayName, Status
```

### format

format right

| situation | cmdlet                    |
| --------- | ------------------------- |
| common    | Format-Table Format-List  |
| other     | Format-Wide Format-Custom |

```powershell
PS C:\Users\user> Get-Service -Name w32time
PS C:\Users\user> Get-Service -Name w32time | Format-List
PS C:\Users\user> Get-Service -Name w32time | Format-Table
PS C:\Users\user> Get-Service -Name w32time | Format-Wide
PS C:\Users\user> Get-Service -Name w32time | Format-Custom

PS C:\Users\user> Get-Service -Name w32time |
    Select-Object -Property Status, DisplayName, Can*
```

### alias

```powershell
PS C:\Users\user> Get-Alias
PS C:\Users\user> Get-Alias -Name gcm, gm
PS C:\Users\user> Get-Alias -Definition Get-Command, Get-Member

PS C:\Users\user> Set-Alias -Name ls -Value Get-ChildItem
PS C:\Users\user> Set-Alias -Name runmyscript -Value "C:\Scripts\MyScript.ps1"

PS C:\Users\user> Remove-Item Alias:ls
```

### provider

```powershell
PS C:\Users\user> Get-PSProvider
```

### comparison

以下列出的所有運算子都不區分大小寫。若要區分大小寫，請將 c 放在運算符前面。例如，-ceq 是等號 （-eq） 比較運算符的區分大小寫版本。

| perator                | definition                 |
| ---------------------- | -------------------------- |
| -eq                    | 等於                       |
| -ne                    | 不等於                     |
| -gt                    | 大於                       |
| -ge                    | 大於或等於                 |
| -lt                    | 小於                       |
| -le                    | 小於或等於                 |
| -Like 使用 \*          | 通配符字元進行比對         |
| -NotLike 不符合使用 \* | 通配符字符                 |
| -Match                 | 符合指定的正則表達式       |
| -NotMatch              | 不符合指定的正則表達式     |
| -Contains              | 判斷集合是否包含指定的值   |
| -NotContains           | 判斷集合是否不包含特定值   |
| -In                    | 判斷指定的值是否在集合中   |
| -NotIn                 | 判斷指定的值是否不在集合中 |
| -Replace               | 取代指定的值               |

```powershell
'PowerShell' -eq 'powershell'
'PowerShell' -ceq 'powershell'
'PowerShell' -like '*shell'
'PowerShell' -match '^.*shell$'

$Numbers = 1..10
$Numbers -contains 15
15 -in $Numbers

'PowerShell' -replace 'Shell'
'SQL Saturday - Baton Rouge' -Replace 'saturday','Sat'
'SQL Saturday - Baton Rouge'.Replace('saturday','Sat')
```

---

## common

### comment

```powershell
# single line comment

<#
multi line comment
#>
```

### variable

```powershell
Get-ChildItem Env:            # list all variable
$env:USERPROFILE              # get variable
$env:VAR=<value>              # set variable

Get-Service W32Time
$SRV = Get-Service W32Time
Stop-Service $SRV
Start-Service $SRV
$SRV | Select-Object -Property Name
${SRV}
```

### array

```powershell
$array = @("Apple", "Banana", "Cherry")
# $array = "Apple", "Banana", "Cherry"

$array[0]   # first
$array[-1]  # last

for ($i = 0; $i -lt $array.Count; $i++) {
    Write-Output "Index $($i): $($array[$i])"
}

foreach ($fruit in $array) {
    Write-Output "Fruit: $($fruit)"
}
```

### hash

```powershell
$hash = @{
    Key1 = "Value1"
    Key2 = "Value2"
    Key3 = "Value3"
}
$hash["Key4"] = "Value4"

$hash.Remove("Key3")
foreach ($key in $hash.Keys) {
    Write-Output "${key}: $($hash[$key])"
}

if ($hash.ContainsKey("Key2")) {
    Write-Output "Key2 exist"
}
else {
    Write-Output "no Key2"
}
```

### sub expression

```powershell
# $()
$result = 5 + $(2 * 3)
$result

$cwd = $(Get-Location).Path
$cwd
```

### list

```powershell
$list = [System.Collections.Generic.List[String]]::new()
$list.Add("Apple")
$list.Add("Banana")
$list.Add("Cherry")

for ($i = 0; $i -lt $list.Count; $i++) {
    Write-Output "Index $($i): $($list[$i])"
}

foreach ($fruit in $list) {
    Write-Output "Fruit: $($fruit)"
}
```

---

## loop

### for

```powershell
For ($i = 0; $i -lt 5; $i++) {
    Write-Output "i: $($i + 1)"
}
```

### foreach

```powershell
$numbers = 1..5
ForEach ($num in $numbers) {
    Write-Output "i: $num"
}
```

### while

```powershell
$i = 0
While ($i -lt 5) {
    Write-Output "i: $i"
    $i++
}
```

### do while

```powershell
$i = 0
Do {
    Write-Output "i: $($i + 1)"
    $i++
} While ($i -lt 5)
```

---

## cmdlet

### file / folder

```powershell
# $HOME\$(Get-Random)
New-Item -Path <path> -ItemType File|Directory                  # create file or folder
Copy-Item <src> <dst>                                           # copy file or folder
Copy-Item [-Recurse] -Path <src> -Destination <dst>
Remove-Item [-Recurse] <src> <dst>                              # remove file or folder
Move-Item <src> <dst>                                           # move file or folder
Rename-Item <raw> <new>                                         # rename file or folder
```

| Bash  | PowerShell  |
| ----- | ----------- |
| touch | New-Item    |
| mkdir | New-Item    |
| cp    | Copy-Item   |
| mv    | Move-Item   |
| rm    | Remove-Item |

---

### date & time

```powershell
Get-Date
Get-Date -DisplayHint DateTime|Date|Time
"$((Get-Date).Month) / $((Get-Date).Day) "
(Get-Date).AddDays(2)

Set-Date
```

| Bash | PowerShell         |
| ---- | ------------------ |
| date | Get-Date, Set-Date |

---

### text file

```powershell
Get-Content <path>
(Get-Content <path>).Length

Set-Content <path> <text>
Add-Content <path> <text>
Clear-Content <path>

Get-Content <path> | Sort-Object
Get-Content <path> | Sort-Object | Get-Unique
Get-Content <path> | Measure-Object -character -line -word
```

---

### like linux

| Bash              | PowerShell                        | Cmd      |
| ----------------- | --------------------------------- | -------- |
| ls                | Get-Item                          | dir      |
| cd                |                                   | cd       |
| pwd               | Get-Location                      |          |
| clear             | Clear-Host                        | cls      |
| cp                | Copy-Item                         | copy     |
| mv                | Move-Item                         | move     |
| rm                | Remove-Item                       | del      |
| echo              | Write-Output                      | echo     |
| touch             | New-Item                          |          |
| hostname          |                                   | hostname |
| grep              | Select-String                     | findstr  |
| cat <file>        | Get-Content <file>                | type     |
| head -n 10 <file> | Get-Content <file> -TotalCount 10 |          |
| tail -n 10 <file> | Get-Content <file> -Tail 10       |          |
| tail -f <file>    | Get-Content <file> -Wait          |          |
| ps                | Get-Process                       | tasklist |

```powershell
Get-ChildItem | Where-Object {$_.Extension -eq ".txt"}
Get-Process | Where-Object {$_.Name -eq "chrome"}
Get-Service | Where-Object {$_.Status -eq "Running"}
Get-Service | Where-Object {($_.DisplayName -like "*Win*") -and ($_.Status -eq "Running")}
query user | Where-Object {$_.ID -gt 1}

Get-Process | Where Name -eq "chrome"

Get-Disk
Get-Partition
```

---

## model

```powershell
### WMI / Windows Management Instrumentation
# 5.x
PS C:\Users\user> Get-WmiObject -Class Win32_OperatingSystem
PS C:\Users\user> Invoke-WmiMethod -Class Win32_OperatingSystem -Name Reboot -ComputerName "RemoteComputer"
PS C:\Users\user> Invoke-WmiMethod -Class Win32_OperatingSystem -Name Reboot

### CIM / Common Information Model
# 7.x
PS C:\Users\user> Get-CimInstance -ClassName Win32_OperatingSystem
PS C:\Users\user> Invoke-CimMethod -ClassName Win32_OperatingSystem -MethodName Reboot -ComputerName "RemoteComputer"
PS C:\Users\user> Invoke-CimMethod -ClassName Win32_OperatingSystem -MethodName Reboot
```

---

## ref

- [PowerShell 101](https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/00-introduction)/
  [PowerShell 101](https://learn.microsoft.com/zh-tw/powershell/scripting/learn/ps101/00-introduction)
- [PowerShell 文件](https://learn.microsoft.com/zh-tw/powershell/)
