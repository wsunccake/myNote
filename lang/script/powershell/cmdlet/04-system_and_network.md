# System & Network

## System Informantion

- `Get-CimClass`：
- `Get-CimInstance`：獲取作業系統與硬體詳細資
- `Stop-Computer`：關閉遠端電腦
- `Restart-Computer`：重新啟動電腦

```pwsh
PS C:\> Get-CimClass
PS C:\> Get-CimClass Win32*

PS C:\> Get-CimInstance -ClassName Win32_ComputerSystem
PS C:\> Get-CimInstance -ClassName Win32_BIOS | Select-Object SerialNumber

PS C:\> Stop-Computer
PS C:\> Stop-Computer -ComputerName <hostname>
PS C:\> Restart-Computer -Force
```

### WMI (Windows Management Instrumentation)

WMI 是微軟在 90 年代基於 Web-Based Enterprise Management (WBEM) 提倡的標準所開發的架構。它是 Windows 系統管理的元老。

- 底層協定：
  - 使用 DCOM (Distributed COM) 與 RPC。
- 特性：
  - 專為 Windows 設計。
  - 通訊時會動態開啟多個連接埠，對防火牆非常不友善。
  - 在 PowerShell 中對應的指令為 `Get-WmiObject`（在 PowerShell 7+ 中已被移除）。

### CIM (Common Information Model)

CIM 是一個開放的業界標準（由 DMTF 管理），旨在定義如何描述電腦系統中的各種元件（如程序、硬體、服務）。

- 底層協定：
  - 使用 WS-Man (WS-Management)，基於 HTTP/HTTPS（預設埠 5985/5986）。
- 特性：
  - 跨平台： 不僅限於 Windows，Linux（如 OMI）也能使用。
  - 防火牆友善： 只使用單一標準連接埠。
  - 效能優化： 載入速度與物件處理效率通常優於舊版 WMI。
  - 在 PowerShell 中對應的指令為 `Get-CimInstance`。

| 特性            | WMI (舊式)              | CIM (現代)                  |
| --------------- | ----------------------- | --------------------------- |
| Cmdlet          | \*-WmiObject            | \*-CimInstance, \*-CimClass |
| 通訊協定        | DCOM / RPC              | WS-Man (HTTP/HTTPS)         |
| 防火牆穿透      | 困難 (隨機高埠)         | 容易 (固定 5985/5986 埠)    |
| 跨平台支持      | 僅限 Windows            | 支援 Windows、Linux、macOS  |
| 物件輸出        | 帶有特定方法的 WMI 物件 | 純粹的資料物件 (更輕量)     |
| PowerShell 版本 | 建議 2.0 - 5.1          | 建議 3.0 以上及 PS 7+       |
| Nano Server     | 支援度極低              | 原生支援                    |

---

## Network

- `Get-NetIPAddress`：網路配置
- `Get-NetIPConfiguration`：網路配置
- `Get-NetAdapter`：理網路卡狀態
- `Test-NetConnection`：測試連線與路由
- `Resolve-DnsName`：查詢 DNS
- `Get-NetRoute`：查詢路由

```pwsh
PS C:\> Get-NetIPConfiguration

PS C:\> Get-NetAdapter

PS C:\> Test-NetConnection -ComputerName "google.com" -Port 80

PS C:\> Resolve-DnsName -Name "www.google.com"
```