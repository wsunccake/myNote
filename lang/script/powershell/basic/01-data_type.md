# 資料類型 (Data Type)

## 1. 數值類型 (Numeric Types)

用於數學運算與計數。

| type      | explain                                | example                   |
| --------- | -------------------------------------- | ------------------------- |
| [int]     | 32 位元整數（最常用）。                | $a = 10                   |
| [long]    | 64 位元長整數，處理極大數字。          | [long]9223372036854775807 |
| [double]  | 雙精度浮點數（含小數），預設除法結果。 | $b = 3.14                 |
| [decimal] | 高精度小數，適合財務計算。             | $c = 1.99d                |

```pwsh
$price = [int]50
$pi = 3.1415926     # 自動識別為 Double
```

---

## 2. 文字與字元類型 (Textual Types)

處理字串與單一字元。

- [string]：一串文字。
- [char]：單一個字元，使用單引號並加型別標記。

```pwsh
$text = "Hello PowerShell"
$letter = [char]'A'
```

---

## 3. 布林與邏輯類型 (Boolean Type)

只有兩種狀態。

- [bool]：$true 或 $false。

```pwsh
$isReady = $true
if ($isReady) { "go！" }
```

---

## 4. 集合與容器類型 (Collection Types)

用於儲存多個資料。

| type             | explain                                      | example                                  |
| ---------------- | -------------------------------------------- | ---------------------------------------- |
| [array]          | 陣列。固定順序的集合，索引從 0 開始。        | $arr = 1, 2, 3 或 @("A", "B")      |
| [hashtable]      | 雜湊表。鍵值對 (Key-Value)，搜尋速度快。     | $map = @{ID=1; Name="Joe"}"           |
| [pscustomobject] | 自定義物件。像資料庫的一筆紀錄，有自訂屬性。 | [pscustomobject]@{Color="Red"; ID=1} |

```pwsh
$list = @("Apple", "Banana", "Cherry")
$score = @{ Math = 100; English = 90 }
```

---

## 5. 日期與時間類型 (Date and Time)

專門處理時間運算的強大物件。

- [datetime]：儲存日期與精確時間。

```pwsh
$now = Get-Date
$yesterday = $now.AddDays(-1)
$specificDate = [datetime]"2026/01/01"
```

---

## 6. 特殊類型 (Special Types)

PowerShell 特有的操作類型。

- [switch]：用於 Function 參數，代表「有沒有輸入」這個開關。
- [void]：代表「空」或「不輸出結果」，常用於強行隱藏指令輸出。
- [nullable]：允許數值類型為空（$null）。

```pwsh
[void](dir C:\)     # 執行但不顯示結果
```

---

## 7. 類型檢查與轉換技巧

在 PowerShell 中，可隨時檢查或強迫轉換型別：

**檢查型別 (Checking Type)**

使用 -is 運算子或 .GetType() 方法。

```pwsh
$val = 123
$val -is [int]      # True
$val.GetType().Name # Int32
```

**強制轉型 (Type Casting)**

將型別寫在變數前面的中括號內。

```pwsh
$str = "100"
$num = [int]$str                # 將字串轉換為整數
$date = [datetime]"2026-02-19"  # 將字串轉為日期物件
```

```pwsh
4 / 3                       # 1.33333333333333
4 % 3                       # 取餘數
(4 / 3).GetType().Name      # Double
4d / 3d                     # 1.3333333333333333333333333333

[int](4 / 3)                # 四捨五入
[Math]::Floor(4 / 3)        # 無條件捨去
[Math]::Truncate(4 / 3)
[Math]::Ceiling(4 / 3)      # 無條件進位
```

---

## 8. `PSCustomObject`

**1. 建立 PSCustomObject**

最簡單且最推薦的方法是使用 `[PSCustomObject]` 加 `Hashtable (@{})`

```pwsh
$user = [PSCustomObject]@{
    Name = "Alice"
    Age  = 28
    City = "Taipei"
}

$user.Name
$user.City
```

**2. 進階應用：建立物件陣列**

在自動化腳本中，常建立一組物件清單，這非常適合用來導出 CSV 或顯示表格。

```pwsh
$users = @() # 建立空陣列

$users += [PSCustomObject]@{ Name = "Alice"; Role = "Admin";  ID = 101 }
$users += [PSCustomObject]@{ Name = "Bob";   Role = "User";   ID = 102 }
$users += [PSCustomObject]@{ Name = "Chris"; Role = "Guest";  ID = 103 }

# 1. 漂亮地顯示成表格
$users | Format-Table

# 2. 進行篩選
$users | Where-Object { $_.Role -eq "Admin" }

# 3. 直接匯出成 CSV
$users | Export-Csv -Path "C:\temp\Users.csv" -NoTypeInformation
```

**3. 動態增加屬性：`Add-Member`**

有時候物件建立後，根據後續邏輯動態增加欄位。

```pwsh
$server = [PSCustomObject]@{
    ServerName = "Prod-DB-01"
    Status     = "Online"
}

# 增加一個新的屬性
$server | Add-Member -NotePropertyName "IPAddress" -NotePropertyValue "192.168.1.10"

$server.IPAddress
```

**4. PSCustomObject 優點**

- 管線友好 (Pipeline Friendly)：它是 PowerShell 的原生公民，可以無縫對接到 `Select-Object`、`Where-Object`、`Export-Csv` 等指令。
- 屬性名稱固定：比起 Hashtable，PSCustomObject 更有利於顯示。`Hashtable` 在輸出時只有 `Name` 和 `Value` 兩欄，而 `PSCustomObject` 的 `Key` 會直接變成標題。
- 排序穩定：在 PowerShell 3.0 之後，`[PSCustomObject]@{...}` 會保持你定義屬性的順序。

**5. PSCustomObject vs. Hashtable**

這兩者長得很像，但用途不同：

| Feature   | `Hashtable (@{})`          | `PSCustomObject ([pscustomobject]@{})` |
| --------- | -------------------------- | -------------------------------------- |
| 主要用途  | 快速查找、儲存鍵值對       | 結構化資料、報表輸出、管線傳輸         |
| 顯示方式  | 預設顯示 Name / Value 兩欄 | 顯示為表格標題 (Column Headers)        |
| 方法/屬性 | 提供 .Keys / .Values       | 只能存取你定義的屬性                   |
| 管線      | 傳輸整個表（一個物件）     | 傳輸多筆記錄（多個物件）               |

| 目標       | Syntax                                                   |
| ---------- | ------------------------------------------------------ |
| 建立新物件 | $obj = [PSCustomObject]@{ Key = Value }                |
| 存取屬性   | $obj.Key                                               |
| 修改值     | $obj.Key = NewValue                                    |
| 增加欄位   | $obj                                                  |
| 轉換型別   | $hashtable = @{A=1}; $obj = [PSCustomObject]$hashtable |
