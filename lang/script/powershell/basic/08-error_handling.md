# 處理錯誤（Error Handling）

## 1. 基礎結構

最簡單的錯誤捕捉。

```pwsh
try {
    # 嘗試執行的程式碼
    $result = 10 / 0
}
catch {
    # 發生錯誤時執行的程式碼
    Write-Error "error：$($_.Exception.Message)"
}
finally {
    # 無論是否發生錯誤，最後都會執行的區塊（常用於釋放資源、關閉連線）
    Write-Host "cleaning..."
}
```

---

## 2. 強制捕捉：使用 `-ErrorAction Stop`

許多 PowerShell 指令（如 Get-Item）發生錯誤時不會觸發 catch，因為它們被視為「非終止性」。這時須加上 -ErrorAction Stop。

```pwsh
try {
    # 如果檔案不存在，Get-Item 預設只會噴紅字但不會進 catch
    Get-Item "C:\不存在的檔案.txt" -ErrorAction Stop
}
catch {
    Write-Host "抓到你了！檔案找不到。" -ForegroundColor Yellow
}
```

---

## 3. 分類捕捉 (Multiple Catch Blocks)

可針對不同類型的錯誤做出不同的反應。

```pwsh
try {
    $file = Get-Content "D:\Config.txt" -ErrorAction Stop
    [int]$num = "NotANumber" # 轉型錯誤
}
catch [System.IO.FileNotFoundException] {
    Write-Host "Error: no found"
}
catch [System.Management.Automation.RuntimeException] {
    Write-Host "Error: fail to convert"
}
catch {
    Write-Host "Unkonw error：$($_.Exception.GetType().Name)"
}
```

---

## 4. 取得錯誤詳細資訊：`$_`

在 catch 區塊中，`$_` 代表當前的錯誤物件（Error Record）。

- `$_.Exception.Message`: 錯誤的簡短描述。
- `$_.InvocationInfo.ScriptLineNumber`: 錯誤發生的行號。
- `$_.FullyQualifiedErrorId`: 錯誤的完整識別碼。

---

## 5. 終止性錯誤（Terminating Error）`throw`

可直接拋出一個字串，PowerShell 會將其封裝成錯誤訊息。

```pwsh
throw "Customed error！"
```

## 6. `Write-Error`

```pwsh
Write-Error "Access denied."
```

| 比較項目 | `throw`                          | `Write-Error`                      |
| -------- | -------------------------------- | ---------------------------------- |
| 執行流   | 立即停止（除非被 catch）         | 繼續執行 下一行                    |
| 錯誤類型 | 終止性錯誤                       | 非終止性錯誤                       |
| 適用場景 | 發生「無法繼續執行」的致命錯誤時 | 發生「可預見且不影響後續」的錯誤時 |

---

有時候根本不在乎錯誤，只想讓它安靜，這時不一定要用 `try...catch`：

```pwsh
# 即使出錯也不會顯示任何紅字，直接跳過
$data = Get-Content "secret.txt" -ErrorAction SilentlyContinue
```

PowerShell 有一種非常優雅的寫法，可以在變數為空時拋出錯誤：

```pwsh
$userInput = $null
$data = $userInput ?? (throw "userInput didn't empty！")
```

| Keyword        | Explain                                                | Example                 |
| -------------- | ------------------------------------------------------ | ----------------------- |
| `try`          | 監測此區塊內的程式碼是否噴出錯誤。                     | try { ... }             |
| `catch`        | 捕捉錯誤並處理。可用 `$_` 存取錯誤資訊。               | catch { $\_.Message }   |
| `finally`      | 無論成功或失敗都會執行，適合「關檔」或「中斷連線」。   | finally { $db.Close() } |
| `throw`        | 手動拋出一個錯誤，強迫進入 `catch`。                   | throw "error message"   |
| `-ErrorAction` | 控制指令報錯行為（Stop, SilentlyContinue, Continue）。 | -ErrorAction Stop       |
