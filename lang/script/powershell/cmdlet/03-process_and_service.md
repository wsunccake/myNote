# Process & Service

## Process

- `Get-Process` (**ps**)：取得程序資訊
- `Stop-Process` (**kill**)：停止程序
- `Start-Process`：啟動程序
- `Wait-Process`：等待程序結束

```pwsh
PS C:\> Get-Process
PS C:\> Get-Process -Name chrome
PS C:\> Get-Process chrome
PS C:\> Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5
PS C:\> Get-Process | Sort-Object -Property CPU,WS -Descending

PS C:\> Stop-Process -Name notepad
PS C:\> Stop-Process -Id 1234 -Force

PS C:\> Start-Process notepad

PS C:\> Start-Process "installer.exe" -PassThru | Wait-Process
```

---

## Service

- `Get-Service`：取得服務狀態
- `Start-Service`：啟動服務
- `Stop-Service`：停止服務
- `Restart-Service`：重啟服務
- `Suspend-Service`：暫停服務 (並非所有服務都支援暫停功能)
- `Resume-Service`：重啟服務 (並非所有服務都支援暫停功能)
- `Set-Service`： 設定服務內容

```pwsh
PS C:\> Get-Service
PS C:\> Get-Service -Name <svc>
PS C:\> Get-Service <svc>
PS C:\> Get-Service <svc> | Select-Object -Property *
PS C:\> Get-Service | Where-Object {$_.Status -eq "Running"}
PS C:\> Get-Service | Where-Object {$_.Name -like "*svc*" -and $_.Status -eq "running"}

PS C:\> Set-Service -Name <svc> -StartupType Manual
```
