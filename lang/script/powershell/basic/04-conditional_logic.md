# 條件判斷 (Conditional Logic)

## 1. `if`, `elseif`, `else`

這是最基本的條件判斷。 使用小括號 `()` 包裹條件，大括號 `{}` 包裹執行內容。

```pwsh
$score = 85

if ($score -ge 90) {
    "Excellent"
} elseif ($score -ge 60) {
    "Passed"
} else {
    "Failed"
}
```

---

## 2. `switch`

大量條件需要比對時（例如檢查多個狀態碼），`switch` 比一堆 `elseif` 更簡潔且易讀。

語法特色：

- 預設比對：會逐一檢查所有分支，除非使用 `break`。
- 萬用字元：支援 `-wildcard` 或 `-regex` 模式。
- `Default`：當所有條件都不匹配時執行。

```pwsh
$score = 85

switch ($score) {
    { $_ -ge 90 } { "Excellent"; break }
    { $_ -ge 60 } { "Passed"; break }
    Default       { "Failed" }
}
```

```pwsh
$status = "Warning"

switch ($status) {
    "OK"      { "System Normal"; break }
    "Warning" { "System Warning, please check"; break }
    "Error"   { "System Error, immediate action required"; break }
    Default   { "Unknown Status" }
}
```

---

## 3. 三元運算子 (Ternary Operator)

判斷非常簡單時，用一行程式碼搞定。

```pwsh
$score = 85
$result = ($score -ge 60) ? "Passed" : "Failed"
$result
```

---

## 4. 條件判斷必備的邏輯工具

在寫條件判斷時，會頻繁用到之前提到的比較[運算子](./02-operator.md)。

| Type     | Keyword              | Example                         | Explain                |
| -------- | -------------------- | ------------------------------- | ---------------------- |
| 存在性   | `$null` `-ne` `$var` | if ($null -ne $file)            | 檢查變數是否有值       |
| 檔案檢查 | `Test-Path`          | if (Test-Path "C:\temp")        | 檢查路徑/檔案是否存在  |
| 多重邏輯 | `-and`, `-or`        | if ($a -gt 0 -and $a -lt 10)    | 同時滿足多個條件       |
| 反轉邏輯 | `-not`, `!`          | if (-not (Test-Path "log.txt")) | 若檔案「不存在」才執行 |

---

## 5. Switch 的進階用法 (正規表示法)

如需要判斷字串模式，`switch` 搭配 `-regex` 非常強大：

```pwsh
$inputString = "Error-404"

switch -regex ($inputString) {
    "^Error" { "Error message" }
    "\d{3}"  { "Three digital number" }
}
```

| Keyword  | 適用場景             | Feature                    |
| -------- | -------------------- | -------------------------- |
| `if`     | 1~3 個簡單條件       | 最直覺、彈性最高           |
| `elseif` | 延伸 if 的多重判斷   | 適合循序漸進的邏輯         |
| `switch` | 多個固定值或模式比對 | 程式碼乾淨、支援正則表達式 |
| `? :`    | 極簡的一行判斷       | 節省空間 (需 PS 7+)        |
