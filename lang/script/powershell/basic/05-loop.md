# 迴圈 (Loop)

1. `foreach`

這是處理「集合」（如陣列、檔案列表、物件群）最直覺的方式。它會遍歷集合中的每一個項目。

```pwsh
$servers = "Server01", "Server02", "Server03"

foreach ($s in $servers) {
    Write-Host "checking：$s"
}
```

```pwsh
$studentGrades = @{
    "Alice" = 95
    "Bob"   = 82
    "Chris" = 88
}

foreach ($student in $studentGrades.GetEnumerator()) {
    Write-Host "$($student.Key) score: $($student.Value)"
}

$studentGrades.GetEnumerator() | ForEach-Object {
    Write-Host "$($_.Key) score: $($_.Value)"
}
```

---

2. `ForEach-Object`

當從管線（Pipeline）接收資料時，會使用這方法。通常用 $\_ 代表「當前處理的那個物件」。

```pwsh
1..5 | ForEach-Object {
    $_ * 10
}
```

---

## 4. while 與 do...while (條件驅動版)

這類迴圈會一直執行，直到括號內的條件不再成立。

- `while`：先檢查條件，成立才執行。
- `do...while`：先執行一次，再檢查條件。

```pwsh
$count = 1

while ($count -le 3) {
    Write-Host "Count：$count"
    $count++
}
```

---

## 5. `break` 與 `continue`

在任何迴圈中，這兩個關鍵字可精確控制執行流程。

- `break`：直接「跳出」並結束整個迴圈。
- `continue`：跳過「這一次」剩下的程式碼，直接進入「下一輪」循環。

```pwsh
foreach ($num in 1..5) {
    if ($num -eq 3) { continue }
    if ($num -eq 5) { break }
    Write-Host "Number：$num"
}
```

| Keyword          | 適用場景                | Feature                        |
| ---------------- | ----------------------- | ------------------------------ |
| `foreach`        | 處理陣列或物件集合      | 語法最乾淨，效能好             |
| `ForEach-Object` | 配合管線命令 (Pipeline) | 適合處理大流量資料，節省記憶體 |
| `for`            | 指定次數、使用索引      | 邏輯控制最精密                 |
| `while`          | 當條件成立時持續執行    | 適合用於等待某個事件發生       |
| `do...until`     | 執行直到條件成立        | 至少會執行一次程式碼           |
