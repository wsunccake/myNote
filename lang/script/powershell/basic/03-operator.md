# 運算子 (Operator)

## 1. 算術運算子 (Arithmetic Operator)

用於對數值進行計算。有趣的是，PowerShell 的算術運算子也能用於字串或陣列的重複與串接。

- `+` (加法)：數值相加、字串串接或陣列合併。
- `-` (減法)：數值相減。
- `*` (乘法)：數值相乘或字串/陣列重複。
- `/` (除法)：數值相除。
- `%` (餘數)：取除法後的餘數。

```pwsh
$sum = 10 + 5          # 15
$str = "Hello " + "AI" # "Hello AI"
$repeat = "A" * 5      # "AAAAA"
$rem = 10 % 3          # 1
```

---

## 2. 比較運算子 (Comparison Operator)

PowerShell 的比較運算子預設不區分大小寫（若要區分，請在前面加 c，如 -ceq）。

- `-eq` (等於)：Equal。
- `-ne` (不等於)：Not Equal。
- `-gt` / `-ge` (大於 / 大於等於)：Greater Than / Greater Equal。
- `-lt` / `-le` (小於 / 小於等於)：Less Than / Less Equal。
- `-like` / `-notlike`：使用萬用字元 \* 進行比對。
- `-match` / `-notmatch`：使用正規表示法 (Regex) 比對。
- `-contains` / `-in`：檢查集合中是否包含某元素。

```pwsh
5 -gt 3                # True
"Apple" -like "A*"     # True
"User123" -match "\d+" # True (包含數字)
1,2,3 -contains 2      # True
```

---

## 3. 邏輯運算子 (Logical Operators)

用於組合多個條件判斷。

- `-and`：兩者皆為真。
- `-or`：其中一者為真。
- `-not` 或 `!`：邏輯非（反轉結果）。
- `-xor`：互斥（一真一假才為真）。

```pwsh
($a -gt 10) -and ($a -lt 20)
!($true)               # False
```

---

## 4. 指派運算子 (Assignment Operators)

用於將值賦予變數。

- `=`：基本指派。
- `+=`：加後指派（常用於累加字串或陣列）。
- `-=`：減後指派。
- `++` / `--`：遞增 / 遞減。

```pwsh
$count = 1
$count++               # $count 變為 2
$text += " World"      # 相當於 $text = $text + " World"
```

---

## 5. 字串與類型運算子 (Type & Split Operators)

處理物件類型或字串切割。

- `-is` / `-isnot`：檢查是否為特定類型。
- `-as`：嘗試轉換類型。
- `-split`：切割字串。
- `-join`：合併陣列為字串。

```pwsh
"123" -is [int]        # False (它是字串)
"a,b,c" -split ","     # 得到陣列 @("a", "b", "c")
"A", "B" -join "-"     # "A-B"
```

---

| type | operator                    | explain              | example            |
| ---- | --------------------------- | -------------------- | ------------------ |
| 算術 | `+`, `-`, `*`, `/`, `%`     | 基本數學與物件串接   | 10 % 3 (1)         |
| 比較 | `-eq`, `-ne`                | 相等、不相等         | $a -eq 10          |
| 比較 | `-gt`, `-lt`, `-ge`, `-le`  | 大於、小於系列       | $a -ge 5           |
| 比對 | `-like`, `-match`           | 萬用字元、正規表示法 | "Test" -like "T\*" |
| 集合 | `-contains`, `-in`          | 檢查元素是否在陣列中 | $arr -contains 5   |
| 邏輯 | `-and`, `-or`, `-not`, `!`  | 邏輯判斷組合         | $a -and $b         |
| 指派 | `=`, `+=`, `-=`, `++`, `--` | 賦值與運算後賦值     | $i += 1            |
| 類型 | `-is`, `-as`                | 檢查或轉換型別       | $obj -is [string]  |
| 處理 | `-split`, `-join`           | 切割與合併字串       | "A,B" -split ","   |

---

## 6. 符號運算子

**1. 範圍與成員操作 (Member & Range)**

這類運算子用於存取物件內部的屬性，或快速產生序列。

- `..` (範圍運算子)：產生一個整數陣列。
- `.` (成員存取)：存取物件的屬性或方法。
- `::` (靜態成員運算子)：存取 .NET 類別的靜態屬性或方法。
- `?.` (Null 條件運算子)：[PS 7+] 只有當物件不為 Null 時才存取成員，避免報錯。

```pwsh
1..5        # 1, 2, 3, 4, 5
$date.Year
[DateTime]::Now 或 [Guid]::NewGuid()
$user?.Name
```

**2. 管線與重新導向 (Pipeline & Redirection)**

PowerShell 的核心靈魂。

- `|` (管線)：將前一個指令的結果傳遞給下一個指令。
- `>` / `>>` (重新導向)：將輸出寫入檔案。`>` 會覆蓋，`>>` 是附加。
- `2>` / `2>&1`：處理錯誤流。`2>&1` 代表將錯誤訊息也一併轉到一般輸出流。

```pwsh
Get-Process | Sort-Object CPU
"Hello" > test.txt
```

**3. 字串與格式化 (String & Formatting)**

- `-f` (格式化運算子)：使用複合格式字串（.NET 樣式）。
- `*` (萬用字元)：在 -like 中代表任何長度的字元。
- `@(...)` (陣列次運算式)：確保結果一定是一個陣列，即使只有一個元素。
- `$(...)` (次運算式)：在字串中執行指令並嵌入結果。

```pwsh
"{0} has {1} apples" -f "Tom", 5
"Now: $(Get-Date)"
```

**4. Null 與邏輯捷徑 (Null & Logic Operators)**

這部分大多數需要 PowerShell 7.0 以上版本。

- `??` (Null 聯合運算子)：如果左邊是 Null，則回傳右邊的值。
- `??=` (Null 聯合指派)：如果左邊變數是 Null，則把右邊的值填進去。
- `&&` / `||` (管線鏈結)：`&&` 代表前一個指令成功才執行下一個；`||` 代表前一個失敗才執行。

```pwsh
$value = $input ?? "default"。
```

**5. 其他特殊操作**

- `&` (呼叫運算子)：執行字串或腳本區塊。常用於路徑中有空白的情況。
- `--` (參數終止)：告訴 PowerShell 之後的輸入全部視為參數，不要解析運算子。
- `,` (逗號運算子)：建立陣列。

```pwsh
& "C:\Program Files\App.exe"
$a = 1, 2
```

| Symbol | Name          | 主要用途             | Example                        |
| ------ | ------------- | -------------------- | ------------------------------ |
| `..`   | Range         | 快速產生連續數字     | 1..10                          |
| `.`    | Dot           | 存取物件屬性         | $obj.Property                  |
| `::`   | Static        | 呼叫 .NET 靜態方法   | [Math]::Sqrt(9)                |
| `\|`   | Pipe          | 傳遞物件給下一個指令 | Get-Process \| Sort-Object CPU |
| `-f`   | Format        | 字串填值/格式化      | '{0}' -f $val                  |
| `&`    | Call          | 執行字串代表的指令   | & $path                        |
| `??`   | Null Coalesce | 提供 Null 時的預設值 | $a ?? $b                       |
| `$( )` | Subexpression | 在字串內執行指令     | "Count: $($arr.Count)"         |
