# power shell

## profile

```powershell
$HOME\Documents\PowerShell\profile.ps1

$PROFILE.AllUsersAllHosts
```

---

## like linux

| Bash                        | PowerShell                                        |
| --------------------------- | ------------------------------------------------- |
| cat <file>                  | Get-Content <file>                                |
| cat <file1> <file2> > <out> | Get-Content <file1>, <file2> \| Set-Content <out> |
| head -n 10 <file>           | Get-Content <file> -TotalCount 10                 |
| tail -n 10 <file>           | Get-Content <file> -Tail 10                       |
| tail -f <file>              | Get-Content <file> -Wait                          |

---

## a

```powershell
Get-Help Where-Object -Full
```

```powershell
Get-ChildItem | Where-Object {$_.Extension -eq ".txt"}
Get-Process | Where-Object {$_.Name -eq "chrome"}
Get-Service | Where-Object {$_.Status -eq "Running"}
Get-Service | Where-Object {($_.DisplayName -like "*Win*") -and ($_.Status -eq "Running")}
query user | Where-Object {$_.ID -gt 1}

Get-Process | Where Name -eq "chrome"
```

| 運算符    | 含義                     |
| --------- | ------------------------ |
| -eq       | 等於                     |
| -ne       | 不等於                   |
| -gt       | 大於                     |
| -lt       | 小於                     |
| -ge       | 大於等於                 |
| -le       | 小於等於                 |
| -like     | 字符串匹配（支持通配符） |
| -notlike  | 不匹配通配符             |
| -contains | 集合中包含值             |

---

## ref

- [PowerShell 文件](https://learn.microsoft.com/zh-tw/powershell/)
