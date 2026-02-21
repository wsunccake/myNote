# 函式（Function）

## 1. 基礎定義：無參數與有參數

最簡單的定義方式是使用 function 關鍵字，後接名稱與大括號。

```pwsh
function Say-Hello {
    "Hello, PowerShell!"
}

Say-Hello
```

```pwsh
function Greet-User ($Name) {
    "Hello, $Name!"
}

Greet-User "PowerShell"
```

---

## 2. 進階定義：型別、預設值與強制參數

建議使用 param() 區塊來定義參數，可增加可讀性並加入更多控制。

- 型別種類：在變數前加上 [type]。
- 預設值：直接在參數後加上 = value。
- 強制要求 (Mandatory)：使用屬性標籤確保使用者一定要輸入。

```pwsh
function Set-UserConfig {
    param (
        [Parameter(Mandatory=$true)] # 強制要求
        [string]$UserName,           # 字串型別

        [int]$Age = 18,              # 整數型別 + 預設值

        [datetime]$JoinDate = (Get-Date) # 預設為當前時間
    )
    "User: $UserName, Age: $Age, Date: $JoinDate"
}
```

---

## 3. 不定參數數量 (Variable Arguments)

如果不知道使用者會輸入多少個參數，有兩種做法：

**使用陣列型別**

最常見的做法，讓參數接收一個陣列。

```pwsh
function Sum-Numbers ([int[]]$Numbers) {
    $total = 0
    foreach ($n in $Numbers) { $total += $n }
    $total
}

Sum-Numbers 1, 2, 3, 4
```

**使用 `$args` 自動變數**

如不定義 param()，所有輸入的參數都會自動存入 $args 陣列中。

```pwsh
function Show-AllArgs {
    "input number: $($args.Count) "
    $args | ForEach-Object { "parameter content: $_" }
}

Show-AllArgs "A" 123 $true
```

---

## 4. 回傳值 (Return Values)

在 PowerShell 中，「所有沒有被捕捉的輸出」都會被當作回傳值。可用 `return` 關鍵字，但它主要的作用是「停止執行並回傳」。

```pwsh
function Get-Square ([int]$Number) {
    $result = $Number * $Number
    return $result
}

$val = Get-Square 5
```

---

## 5. 綜合查詢表：函式定義要素

| Function | Example                | Explain                                             |
| -------- | ---------------------- | --------------------------------------------------- |
| 型別限定 | [string]$Name          | 限制輸入必須為特定種類，不符會報錯。                |
| 預設值   | "$Mode = ""Simple"""   | 使用者未輸入時自動帶入。                            |
| 強制輸入 | [Parameter(Mandatory)] | 執行時若缺漏，PowerShell 會主動詢問。               |
| 多個型別 | [PSObject]             | 允許接收任何類型的物件。                            |
| 參數別名 | "[Alias(""CN"")]"      | 給參數一個簡短的綽號（如 ComputerName 縮寫為 CN）。 |
| 開關參數 | [switch]$Force         | 不需傳值，有輸入即為 $true（如 -Force）。           |

## 6. `[switch]`

如想要像 -Recursive 或 -Force 那樣只需開關而不需輸入 True/False，請使用 [switch]

```pwsh
function Remove-Data {
    param([switch]$Confirm)
    if ($Confirm) { "removing..." } else { "only previewing" }
}

Remove-Data -Confirm
```
