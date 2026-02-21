# pipeline

管線 (Pipeline) 是 PowerShell 其最強大的核心功能。不同於傳統命令列（如 CMD 或 Bash）只傳遞「純文字」，PowerShell 的管線傳遞的是完整的 **.NET 物件**。

## 1. Pipeline 的基本運作邏輯

管線使用符號 `|`。其運作邏輯如下：

- **左側指令**產生一個或多個物件。
- **右側指令**接收這些物件，並根據物件的類型或屬性進行操作。

---

## 2. Pipeline 的進階用法與範例

**A. 篩選與過濾 (`Where-Object`)**

這是最常用的用法，從一大堆資料中找出符合條件的。

範例： 找出所有佔用記憶體超過 500MB 的程序。

```pwsh
Get-Process | Where-Object { $_.WorkingSet -gt 500MB }
```

`$_` 代表管線中當前的那個物件。

**B. 選取與轉換 (`Select-Object`)**

只保留感興趣的欄位，或限制回傳的數量。

範例： 只列出前 5 個最耗 CPU 的程序名稱與 ID。

```pwsh
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, Id
```

**C. 逐一處理 (`ForEach-Object`)**

對管線中的每一個物件執行一段特定的程式碼。

範例： 將資料夾內所有的 .log 檔改名，加上今天的日期。

```pwsh
Get-ChildItem *.log | ForEach-Object { Rename-Item $_.FullName -NewName "$($_.BaseName)_$(Get-Date -Format 'yyyyMMdd').log" }
```

**D. 排序與群組 (`Sort-Object`, `Group-Object`)**

範例： 按檔案類型（副檔名）對資料夾內的檔案進行分組統計。

```pwsh
Get-ChildItem | Group-Object Extension
```

**E. 輸出與轉換格式 (`Out-File`, `Export-Csv`, `ConvertTo-Html`)**

將物件轉換為實體檔案。

範例： 將目前的服務清單匯出成 CSV 報表。

```pwsh
Get-Service | Export-Csv -Path "./Services.csv" -NoTypeInformation
```

---

## 3. Pipeline 的繫結機制（底層原理）

把物件丟進管線時，PowerShell 會透過兩種方式來決定「誰接誰」：

- **ByValue** (按型別)： 如果 A 指令產生的物件型別剛好是 B 指令參數所要求的，直接對接。
- **ByPropertyName** (按屬性名稱)： 如果型別不合，但 A 物件的屬性名稱（例如 Name）跟 B 指令的參數名稱一樣，也會自動對接。

| 用法 | Cmdlet                         | Explain                  | 範例場景                        |
| ---- | ------------------------------ | ------------------------ | ------------------------------- |
| 篩選 | `Where-Object` (alias: `?`)    | 根據條件保留物件         | 找大於 1GB 的檔案               |
| 選取 | `Select-Object`                | 挑選特定欄位或前幾筆     | 只要顯示「名稱」和「狀態」      |
| 排序 | `Sort-Object`                  | 依據屬性大小、字母排序   | 按修改日期排序檔案              |
| 疊代 | `ForEach-Object` (alias: `%`)  | 對每個物件執行自定義動作 | 批次壓縮多個資料夾              |
| 群組 | `Group-Object`                 | 統計與分類               | 統計各狀態的服務數量            |
| 轉換 | `Export-Csv`, `ConvertTo-Json` | 變更資料呈現格式         | 將系統資訊轉成 JSON 給 API 使用 |
| 輸出 | `Out-GridView`, `Out-File`     | 顯示在視窗或存入檔案     | 彈出一個表格視窗供選取          |
