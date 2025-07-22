# MS-DOS 6.x

## download

- [MS-DOS 6.22](https://archive.org/details/ms-dos-6.22_dvd)
- [MS-DOS 6.20](https://winworldpc.com/product/ms-dos/620)
- [Borland Turbo C 2.x](https://winworldpc.com/product/borland-turbo-c/2x)
- [Borland Turbo C++ 3.x (DOS)](https://winworldpc.com/product/turbo-c/3x)
- [Borland Turbo Assembler 5.x](https://winworldpc.com/product/turbo-assembler/5x)
- [Microsoft C/C++ 6.x](https://winworldpc.com/product/microsoft-c-c/6x)
- [Microsoft FORTRAN 5.x](https://winworldpc.com/product/microsoft-fortran/5x)
- [Microsoft Macro Assembler 6.x](https://winworldpc.com/product/macro-assembler/6x)
- [Microsoft Visual Basic 1.0 for DOS](https://winworldpc.com/product/microsoft-visual-bas/10-for-dos)

---

## command

📁 檔案與目錄操作

| 指令             | 說明                         | 範例                 |
| ---------------- | ---------------------------- | -------------------- |
| `dir`            | 顯示目前目錄的檔案與資料夾   | `dir`                |
| `cd`             | 切換目錄（Change Directory） | `cd games`、`cd ..`  |
| `md` / `mkdir`   | 建立新目錄                   | `md newfolder`       |
| `rd` / `rmdir`   | 刪除空的目錄                 | `rmdir oldfolder`    |
| `del`            | 刪除檔案                     | `del test.txt`       |
| `copy`           | 複製檔案                     | `copy a.txt b.txt`   |
| `move`           | 移動檔案或重新命名           | `move a.txt folder\` |
| `ren` / `rename` | 重新命名檔案                 | `ren a.txt b.txt`    |
| `type`           | 顯示文字檔內容               | `type readme.txt`    |

💾 磁碟與系統指令

| 指令       | 說明                 | 範例             |
| ---------- | -------------------- | ---------------- |
| `format`   | 格式化磁碟           | `format a:`      |
| `chkdsk`   | 檢查磁碟狀況         | `chkdsk c:`      |
| `vol`      | 顯示磁碟卷標         | `vol`            |
| `label`    | 修改磁碟卷標         | `label`          |
| `diskcopy` | 複製整張磁碟         | `diskcopy a: a:` |
| `sys`      | 將系統檔複製到磁碟中 | `sys a:`         |

⚙️ 系統管理與批次

| 指令    | 說明                     | 範例                   |
| ------- | ------------------------ | ---------------------- |
| `cls`   | 清除畫面                 | `cls`                  |
| `ver`   | 顯示 DOS 版本            | `ver`                  |
| `path`  | 設定可執行檔路徑         | `path c:\dos;c:\tools` |
| `set`   | 設定環境變數             | `set temp=c:\temp`     |
| `echo`  | 顯示訊息（常用於批次檔） | `echo Hello`           |
| `pause` | 停止執行等待按鍵         | `pause`                |
| `exit`  | 離開命令列或批次檔       | `exit`                 |

🧪 範例批次檔 (.bat)

```bat
@echo off
echo Welcome MS-DOS
cd games
dir
pause
```

---

## environment variable

```bat
SET TEMP=C:\TEMP
SET PATH=C:\DOS;C:\TOOLS

echo %PATH%
```

## AUTOEXEC.BAT

## DEBUG

MS-DOS DEBUG 是一個強大的工具，用於低階系統操作、記憶體檢視、以及基本的匯編程式開發。以下是 DEBUG 的常用命令及其操作範例。

- R（Register）

  顯示或修改 CPU 暫存器內容。

```bat
:: 顯示 CPU 內部寄存器
-r
AX=0000  BX=0000  CX=0000  DX=0000  SP=FFFE  BP=0000  SI=0000  DI=0000
DS=16D5  ES=16D5  SS=16D5  CS=16D5  IP=0100   NV UP EI PL NZ NA PO NC

:: 修改 AX
-r ax
AX 0000
:1234   ; 輸入 1234 並按 Enter
```

- D （Dump）

  以十六進位與 ASCII 顯示記憶體內容。

```bat
-D 100
0F71:0100  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
0F71:0110  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................

-D CS:100 L 10    ; 顯示從CS:100開始的16個位元組
0F71:0100  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................

-D 100 10F        ; 顯示從100H到10FH的記憶體內容
0F71:0100  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
```

- E（Enter）

  修改記憶體中的資料。

```bat
-E 100 41 42 43 44 45    ; 在100H處寫入ASCII碼 'A', 'B', 'C', 'D', 'E'
-D 100
0F71:0100  41 42 43 44 45 00 00 00-00 00 00 00 00 00 00 00  ABCDE...........

-E 105 "Hello World!"    ; 在105H處寫入字串 "Hello World!"
-D 100
0F71:0100  41 42 43 44 45 48 65 6C-6C 6F 20 57 6F 72 6C 64  ABCDEHello World
0F71:0110  21 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  !...............

-E 100                   ; 進入互動模式，逐位元組修改
0F71:0100  41.F1         ; 顯示當前值41，輸入F1並按Enter
0F71:0101  42.           ; 顯示當前值42，按空格跳過
0F71:0102  43.F2         ; 顯示當前值43，輸入F2並按Enter
0F71:0103  44.           ; 按Enter退出互動模式
```

- U（Unassemble）

  反組譯記憶體中的機器碼。

```bat
-U 100 L 8    ; 反匯編從100H開始的8個位元組
0F71:0100 B83412          MOV     AX,1234
0F71:0103 BB7856          MOV     BX,5678
0F71:0106 CD20            INT     20
^    ^    ^               ^
|    |    |               |
|    |    Machine Code    Assembly Code
|    Offset Address
Segment Address
```

- A（Assemble）

  輸入組合語言指令，轉換為機器碼寫入記憶體。

```bat
-A 100
0F71:0100 MOV AX,1234
0F71:0103 MOV BX,5678
0F71:0106 INT 20        ; DOS exit program
0F71:0108               ; 按Enter結束輸入
```

- T (Trace)

  單步執行指令（會進入中斷）。

```bat
:: 假設CS:IP指向0F71:0100 MOV AX,1234
-T
AX=1234  BX=0000  CX=0000  DX=0000  SP=FFFE  BP=0000  SI=0000  DI=0000
DS=0F71  ES=0F71  SS=0F71  CS=0F71  IP=0103   NV UP EI PL NZ NA PO NC
0F71:0103 BB7856          MOV     BX,5678
```

- N（Name）, L（Load）, W（Write）

  N：指定檔案名稱，用於讀寫檔案。
  L：從檔案或磁碟載入資料到記憶體。
  W：從記憶體寫入資料到檔案或磁碟。

```bat
-N HELLO.COM     ; 指定要寫入的檔名
-RCX             ; 設定要寫入的位元組數 (COM檔大小)
CX 0000
:16              ; 假設程式大小為16H (22個位元組)
-W 100           ; 將從記憶體位址100H開始的內容寫入HELLO.COM
Writing 0016 bytes
```

- Q (Quit)

  離開 DEBUG 工具。

```bat
-Q
```

| 指令 | 名稱       | 功能簡介                      | 範例           |
| ---- | ---------- | ----------------------------- | -------------- |
| `R`  | Register   | 顯示/修改 CPU 暫存器          | `-r` / `-r ax` |
| `D`  | Dump       | 顯示記憶體內容（Hex + ASCII） | `-d 100`       |
| `E`  | Enter      | 修改記憶體內容                | `-e 100`       |
| `U`  | Unassemble | 反組譯顯示記憶體中機器碼      | `-u 100`       |
| `A`  | Assemble   | 輸入組合語言指令              | `-a 100`       |
| `T`  | Trace      | 單步執行（進入中斷）          | `-t`           |
| `P`  | Proceed    | 單步執行（不進入中斷）        | `-p`           |
| `G`  | Go         | 執行程式直到結束或中斷        | `-g`           |
| `N`  | Name       | 指定檔案名稱                  | `-n test.com`  |
| `L`  | Load       | 載入檔案至記憶體              | `-l`           |
| `W`  | Write      | 寫入記憶體內容至檔案          | `-w`           |
| `Q`  | Quit       | 離開 DEBUG 工具               | `-q`           |

---

## Reference

- [MS-DOS](https://github.com/microsoft/MS-DOS)
