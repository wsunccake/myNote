# fire format

## shell

- `shfmt`

`shfmt` 是一個非常受歡迎的開源工具，專門用於 格式化 Shell 指令碼（如 Bash、Sh、Mksh 等）。它就像是 Shell 界的 Prettier 或 Go fmt，能讓原本凌亂的程式碼變得整齊、易讀且符合規範。

```bash
linux:~ $ shfmt -h
linux:~ $ shfmt -l .
linux:~ $ shfmt -d .
linux:~ $ shfmt -ci -i 4 -s -bn -sr -w <sh_file>
```

| Option        | 說明                                                                   |
| ------------- | ---------------------------------------------------------------------- |
| -i <num>      | 縮排大小。例如 -i 2 代表 2 個空格；-i 0 則使用 Tab。                   |
| -w            | 直接寫入 (Write)。將格式化後的內容覆蓋原檔案，不加此項則只輸出到螢幕。 |
| -d            | 比較 (Diff)。顯示格式化前後的差異，但不修改檔案。                      |
| -l            | 列出 (List)。僅列出格式不符合標準的檔案名稱。                          |
| -s            | 簡化 (Simplify)。嘗試縮減程式碼（例如將 if 縮成一行）。                |
| -p            | Function 換行。將 function 的左大括號 { 換到下一行。                   |
| -ln <variant> | 指定語言。可選 bash, posix, mksh, bats。                               |
| -ci           | case 分支縮排。                                                        |
| -bn           | 若語句太長，將二進位運算子（如 &&, \|\|）置於行首。                    |
| -sr           | 在重導向符號（>）後方加入空格。                                        |

---

## robotframework

- `robotframework-robocop`

`robotframework-robocop`（簡稱 Robocop）是專為 Robot Framework 開發的靜態程式碼分析工具（Linter）。6.0 之後的一個重大架構變更。開發團隊為了簡化工具鏈，決定將原本獨立的 Robotidy (Formatter) 功能正式整合進 Robocop (Linter) 之中。

1. 基礎工作模式 (Work Modes)
   最常用的部分，決定工具如何處理檔案。
   --overwrite (預設)：直接修改原始檔案。
   --diff：不會修改檔案，但會在螢幕上顯示「如果格式化，程式碼會長怎樣」（類似 git diff）。
   --check：CI/CD 必備。檢查檔案是否符合格式，不符合會回傳錯誤狀態碼，但不會動到程式碼內容。

2. 格式設定 (Formatting Settings)
   想微調排版細節，這組參數最重要：
   --space-count：設定 Cell 之間的空格（預設 4）。
   --indent：設定縮排空格。
   --line-length：設定單行長度上限（預設 120），超過可能會觸發換行。
   --separator：可以選擇使用 space 或 tab。

3. 選取格式化規則 (Selecting formatters)
   Robocop 的格式化是由多個「Formatter（原 Robotidy 的 Transformers）」組成的：
   --select：只跑你指定的格式化規則（例如：只跑 AlignSettingsSection）。
   --target-version：根據你的 Robot Framework 版本（4/5/6/7）自動關閉不支援的規則。

4. 局部格式化 (Partial Formatting)
   --start-line / --end-line：你可以指定只格式化檔案中的某幾行，這在處理巨大且舊有的舊腳本（Legacy Code）時非常好用，避免一次改動太多。

```bash
linux:~ $ robocop --version
linux:~ $ robocop --help
linux:~ $ robocop --install-completion

linux:~ $ robocop list --help
linux:~ $ robocop list formatters
linux:~ $ robocop list rules

linux:~ $ robocop format --select OrderSettingsSection
linux:~ $ robocop format --configure "MergeAndOrderSections.enabled=False"
linux:~ $ robocop check --ignore NAME18 --ignore DOC01
```

---

## rust

```bash
linux:~ $ rustfmt <file>.rs

linux:~/project $ cargo fmt
```
