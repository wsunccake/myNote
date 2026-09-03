# Cmdlet

Cmdlet（發音為 "command-let"）是 PowerShell 的心臟。不同於傳統命令列（如 CMD）中的獨立執行檔（.exe），Cmdlet 是內建在 PowerShell 環境中的輕量級指令實例。

## 1. Cmdlet 的核心特色

命名規則：動詞-名詞 (Verb-Noun)
這是 Cmdlet 最直觀的特色。它永遠採用「單數名詞」搭配「標準化動詞」，讓你即使沒用過某個指令，也能猜出它的用途。

- `Get-`：獲取資訊（如 Get-Service）
- `Set-`：設定或更改（如 Set-Location）
- `New-`：新增資源（如 New-Item）
- `Remove-`：刪除資源（如 Remove-Item）

傳遞的是「物件」而非「文字」
這是 PowerShell 毀滅性領先 CMD 或 Bash 的地方。傳統指令輸出的是一串文字，需要用複雜的正規表示式去過濾資訊；而 Cmdlet 輸出的是 Object（物件）。

白話解釋： 當執行 `Get-Service`，得到的不是一堆字，而是一堆具有屬性（狀態、名稱、顯示名稱）的「實體資料」。

---

## 2. 範例與解說

看幾個實際應用的例子：

**A. 基礎查詢：列出所有正在執行的服務**

```pwsh
Get-Service | Where-Object {$_.Status -eq "Running"}
```

`Get-Service` 抓取所有服務物件，透過「管線 (Pipe, `|`)」傳給下一個指令進行篩選。

**B. 檔案操作：建立新資料夾與檔案**

```pwsh
New-Item -Path "C:\Demo" -ItemType Directory
New-Item -Path "C:\Demo\test.txt" -ItemType File -Value "Hello PowerShell!"
```

**C. 系統管理：重新啟動特定的程序**

```pwsh
Get-Process -Name "Notepad" | Stop-Process
```

找到記事本程序並直接將其關閉。

---

## 3. Cmdlet 的優缺點分析

**優點 ✅**

- 易學性高： 只要背下幾十個常用動詞，就能組合出上千種操作。
- 強大的管線機制： 由於傳遞的是物件，你可以輕鬆地將 A 指令的結果直接餵給 B 指令，不需要手動解析文字。
- 探索性強： 內建強大的輔助指令：
  `Get-Help`：顯示用法。
  `Get-Command`：找指令。
  `Get-Member`：查看物件有哪些屬性和方法。
- 跨平台： 隨著 PowerShell Core 的推出，現在在 Linux 和 macOS 上也能運行許多相同的 Cmdlet。

**缺點 ❌**

- 啟動較慢： 因為需要載入 .NET 框架，PowerShell 的啟動速度通常比 CMD 或 Bash 慢一點點。
- 語法較長： `Get-ChildItem` 寫起來比 ls 或 dir 冗長（雖然有簡寫 Alias 可用，但腳本建議寫全名以利閱讀）。
- 學習曲線： 對於習慣傳統「文字流」處理的 Linux 老手來說，切換到「物件導向」的思維需要一點時間適應。

如果隱約記得有個指令跟「進程 (Process)」有關，但忘了全名，可輸入：

```pwsh
Get-Command *Process*
```
