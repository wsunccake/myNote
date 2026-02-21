# file system operation

在 PowerShell 中，檔案系統操作是透過 FileSystem Provider 實現的。最核心的觀念是：PowerShell 把硬碟資料夾視為一種「磁碟機 (Drive)」，因此你可以像切換 C: 一樣，用同樣的邏輯去操作註冊表 (Registry) 或變數。

## 1. 核心路徑與導覽 (Navigation)

在操作檔案前，須先學會如何在資料夾間移動。

- `Get-Location` (**pwd**)：取得目前所在路徑。
- `Set-Location` (**cd**)：切換目錄。
- `Push-Location` / `Pop-Location`：將目前路徑推入堆疊，稍後再跳回（適合腳本內暫時切換路徑）。

```pwsh
Push-Location "C:\Windows\System32"
# 執行一些操作...
Pop-Location # 直接回到原本的位置
```

---

## 2. 項目操作 (Item Operations)

處理「檔案或資料夾本身」。

- `New-Item` (**touch** or **mkdir**)：建立項目，透過 -ItemType 參數決定是建立檔案還是資料夾。
- `Get-ChildItem` (**ls** or **dir**)：讀取項目，用來列出檔案還或資料夾。
- `Copy-Item` (**cp**)：複製項目，用來複製檔案還或資料夾。
- `Move-Item` (**mv**)：移動項目，用來移動檔案還或資料夾。
- `Remove-Item` (**rm** or **rmdir**)：刪除項目，用來刪除檔案或資料夾。

```pwsh
# 建立資料夾
New-Item -Path "C:\Backup" -ItemType Directory

# 建立空白檔案
New-Item -Path "C:\Backup\log.txt" -ItemType File -Value "Initial Content"

# 列出 C 槽下所有 .log 檔，包含子資料夾 (-Recurse)
Get-ChildItem -Path "C:\" -Filter "*.log" -Recurse -ErrorAction SilentlyContinue

# 複製資料夾及其內容 (-Recurse)
Copy-Item -Path "C:\Source" -Destination "D:\Backup" -Recurse

# 刪除所有暫存檔而不跳出確認提醒 (-Force)
Remove-Item -Path "C:\Temp\*" -Include *.tmp -Force
```

---

## 3. 內容操作 (Content Operations)

處理「檔案內部的資料」。

- `Get-Content` (**cat**)：讀取檔案內容。
- `Set-Content`：覆寫檔案內容。
- `Add-Content`：在檔案末尾追加內容。

範例：逐行讀取並過濾關鍵字

```pwsh
Get-Content -Path "./server.log" | Where-Object { $_ -match "Error" }
```

---

## 4. 進階技巧：測試與管理權限

- `Test-Path`：檢查路徑是否存在，回傳 True/False（寫腳本必備）。
- `Get-Acl` / `Set-Acl`：讀取或設定檔案的存取控制清單（權限）。

範例：如果資料夾不存在就建立它

```pwsh
$path = "C:\Scripts\Output"
if (!(Test-Path $path)) {
    New-Item -Path $path -ItemType Directory
}
```

| Function  | Cmdlet              | Alias        | Example                    |
| --------- | ------------------- | ------------ | -------------------------- |
| 路徑切換  | Set-Location        | cd, chdir    | sl C:\Users                |
| 列出清單  | Get-ChildItem       | ls, dir, gci | gci -File                  |
| 建立項目  | New-Item            | ni           | ni test.txt -ItemType File |
| 刪除項目  | Remove-Item         | del, rm, ri  | ri ./old_folder -Recurse   |
| 複製/移動 | Copy-Item Move-Item | cp, mv       | mi file.txt D:\Archive\|   |
| 讀取內容  | Get-Content         | cat type     | gc config.json             |
| 寫入內容  | Set-Content         | sc           | sc log.txt "Start"         |
| 追加內容  | Add-Content         | ac           | ac log.txt "Finish"        |
| 路徑檢查  | Test-Path           | (無)         | Test-Path C:\config.ini    |
| 重新命名  | Rename-Item         | ren          | ren old.txt new.txt        |


記住，`Get-ChildItem` 傳回的是檔案物件。可利用它的屬性進行強大操作：

```pwsh
# 找出大於 100MB 的檔案並按大小排序
Get-ChildItem -Path "C:\Data" -Recurse | Where-Object { $_.Length -gt 100MB } | Sort-Object Length -Descending
```