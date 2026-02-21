# 變數 (Variable)

## 1. 變數基礎與命名規則

**命名規則**

- 開頭符號： 必須以錢字號 $ 開頭。
- 組成字元： 可以包含字母、數字和底線（\_）。
- 不分大小寫： $MyVar 與 $myvar 是同一個變數。
- 特殊字元處理： 若名稱包含空格或特殊符號，須用大括號括起來，例如：${My Local Variable}。

```pwsh
$name = "Gemini"          # 字串
$age = 25                 # 整數
$today = Get-Date         # 儲存物件 (DateTime)
$process = Get-Process    # 儲存多個物件 (陣列)
```

---

## 2. 環境變數 (Environment Variables)

環境變數用於儲存作業系統層級的資訊。在 PowerShell 中，可透過 Env: 磁碟機來存取它們。

**基本用法**

- 讀取： 使用 $env:變數名。
- 修改： 直接賦值（僅對當前工作階段有效）。

```pwsh
# 顯示電腦名稱
$env:COMPUTERNAME

# 顯示系統路徑 (Path)
$env:Path

# 暫時新增一個路徑到環境變數
$env:Path += ";C:\MyTools"
```

---

## 3. 變數的所有使用用法

**A. 型別宣告 (Type Casting)**

雖然 PowerShell 是動態型別，但可強制指定型別以確保資料正確。

```pwsh
[int]$number = "10"      # 將字串強制轉為整數
[datetime]$birthday = "2026/01/01"
```

## B. 常數與唯讀變數

不希望變數被意外修改，可以使用 `Set-Variable`。

```pwsh
# 建立一個唯讀變數
Set-Variable -Name "PI" -Value 3.14159 -Option ReadOnly

# 建立一個常數 (無法刪除或修改，直到關閉視窗)
Set-Variable -Name "API_KEY" -Value "XYZ123" -Option Constant
```

**C. 特殊與自動變數**

PowerShell 內建了一些特殊變數來反映當前狀態：

- `$PSVersionTable`：查看 PowerShell 版本資訊。
- `$HOME`：目前使用者的家目錄路徑。
- `$null`：代表「空」或「無」。
- `$?`：執行上一個指令是否成功（True/False）。

---

## 4. 作用域 (Scopes)

變數在哪裡可用，取決於它的作用域：

- Global (全域)： 在整個 PowerShell 工作階段都可用。
- Local (區域)： 預設值，僅在目前的 Script 或 Function 中可用。
- Script： 在該 Script 檔案內可用。

```pwsh
$global:MyApp = "Running"
```

| Type     | Syntax / Example              | Explain                                          |
| -------- | ----------------------------- | ------------------------------------------------ |
| 一般變數 | $var = "value"                | 最常見用法，儲存任何物件。                       |
| 環境變數 | $env:UserName                 | 存取 Windows/系統層級的設定。                    |
| 型別變數 | [string]$name = 123           | 強制將 123 儲存為字串 "123"。"                   |
| 唯讀變數 | Set-Variable -Option ReadOnly | 防止變數內容被後續指令覆寫。                     |
| 自動變數 | $PWD, $PID, $\_               | 系統自動維護，反映目前路徑、程序 ID 或管線物件。 |
| 特殊命名 | ${My Variable!}               | 使用大括號來定義包含空格或符號的名稱。           |

如果想看目前記憶體中到底存了哪些變數，可以執行：

```pwsh
Get-Variable | Out-GridView
```
