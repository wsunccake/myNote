# powershell 7

## intro

```pwsh
C:\ pwsh
PS C:\> $PSVersionTable
```

```pwsh
PS C:\> Get-Help        # man
PS C:\> Get-Command     #
PS C:\> Get-Variable    # printenv

PS C:\> Write-Host      # echo
PS C:\> Clear-Host      # clean

# example
PS C:\> Get-Help New-Item

PS C:\> Write-Host "Hello PowerShell!"                          # echo "Hello PowerShell!"
PS C:\> Clear-Host                                              # clean
```

---

## run

```ps1
# hello.ps1
Write-Output "Hello PowerShell!"
```

```pwsh
# method 1.
PS C:\> pwsh hello.ps1

# method 2.
PS C:\> hello.ps1
```

## policy

```pwsh
PS C:\> Get-ExecutionPolicy -List
PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned [-Scope CurrentUser]
```

| Policy       | Explain                                                                           |
| ------------ | --------------------------------------------------------------------------------- |
| Restricted   | 最嚴格。禁止執行任何腳本（.ps1），只能執行單個指令。Windows 用戶端的預設值。      |
| AllSigned    | 所有腳本（包含自己寫的）都必須有 受信任發行者的數位簽章 才能執行。                |
| RemoteSigned | 最常用（平衡點）。本機寫的腳本直接跑；但從網路下載的必須有數位簽章。              |
| Unrestricted | 執行所有腳本。執行網路下載的未簽署腳本時會彈出警告。                              |
| Bypass       | 完全不檢查。沒有警告、不要求簽章，常用於自動化部署或單次任務。                    |
| Default      | 使用預設原則（用戶端為 Restricted，伺服器為 RemoteSigned）。                      |
| Undefined    | 移除該範圍的設定，將權限交由更高層級決定。若全部都是 Undefined，則為 Restricted。 |

| Priority | Scope         | Explain                                                    |
| -------- | ------------- | ---------------------------------------------------------- |
| 1 (high) | MachinePolicy | 由「電腦群組原則 (GPO)」設定，影響整台電腦。               |
| 2        | UserPolicy    | 由「使用者群組原則 (GPO)」設定，影響該使用者。             |
| 3        | Process       | 只對 當前 PowerShell 視窗 有效，關閉後失效。存於記憶體中。 |
| 4        | CurrentUser   | 影響目前登入的使用者。設定存於該使用者的 Registry 中。     |
| 5 (low)  | LocalMachine  | 預設作用域。影響電腦上所有使用者。需管理員權限 才能變更。  |

---

## container environment

```pwsh
PS C:\> docker pull mcr.microsoft.com/powershell:nanoserver-ltsc2022
PS C:\> docker run -itd `
          -v "${PWD}:C:\app" `
          -p 5985:5985 `
          --name nano `
          mcr.microsoft.com/powershell:nanoserver-ltsc2022 pwsh
PS C:\> docker exec -it nano pwsh
```

```pwsh
PS C:\> subst /?
PS C:\> subst
PS C:\> subst <X>: C:\Users\user\vdisk
PS C:\> subst <X>: /D

PS C:\> Get-PSDrive -PSProvider FileSystem
PS C:\> Get-Volume
```

---

## comment

```ps1
# this is comment

<#
multi line comment
#>

Write-Output "Hello PowerShell!"
```

---

## newline / line break

```ps1
# method 1.
Write-Output `
  "Hello PowerShell!"

# method 2.
Get-Process -Name pwsh |
  Select-Object Id, Name, CPU
```
