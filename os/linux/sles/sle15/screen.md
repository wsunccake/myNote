# screen

## basic

```bash
linux:~ $ screen [-S session_name]     # 啟動 screen 並命名
linux:~ $ screen -ls                   # 列出所有 screen
linux:~ $ screen -dr [pid.tty.host]    # 分離並重新連接 screen
linux:~ $ screen -x [pid.tty.host]     # 多點連接到 screen

C-a '    # 切換 window
C-a "    # 切換 window
C-a :    # 進入命令列模式
```

### window

| 快捷鍵          | 指令名稱      | 說明                                            |
| --------------- | ------------- | ----------------------------------------------- |
| C-a c           | screen        | 建立一個新視窗並切換過去                        |
| C-a n / C-a C-n | next          | 切換到下一個視窗（編號遞增）                    |
| C-a p / C-a C-p | prev          | 切換到前一個視窗（編號遞減）                    |
| C-a 0~9         | select 0-9    | 直接切換到指定編號的視窗                        |
| C-a "           | windowlist -b | 顯示所有視窗供選擇（可用上下鍵移動）            |
| C-a '           | select        | 手動輸入視窗名稱或編號以切換                    |
| C-a A           | title         | 設定當前視窗名稱（自訂標題）                    |
| C-a k / C-a C-k | kill          | 關閉目前視窗（會提示確認）                      |
| C-a N           | number        | 顯示目前視窗的編號與名稱                        |
| C-a w / C-a C-w | windows       | 顯示簡易視窗清單列（畫面底部列出視窗）          |
| C-a C-a         | other         | 切換到前一個正在顯示的視窗                      |
| C-a :           | colon         | 進入命令列模式，可用 `select 1`、`title xxx` 等 |
| C-a \           | quit          | 結束所有視窗並退出 screen                       |

### split

```bash
C-a S   # 建立新區域 (水平分割)
C-a |   # 建立新區域 (垂直分割)
C-a tab # 切換焦點
C-a c   # 開啟第二個 shell
```

```bash
# ~/.scrrenrc

bind h focus left   # 將焦點移動到左方區域
bind j focus down   # 將焦點移動到下方區域
bind k focus up     # 將焦點移動到上方區域
bind l focus right  # 將焦點移動到右方區域
bind t focus top    # 將焦點移動到最上方的區域
bind b focus bottom # 將焦點移動到最下方的區域
```

---

## key bindings

透過特定的按鍵組合來控制視窗、分割畫面、脫離會話等，而無需離開命令列。

基本概念

1. 前綴鍵 (Prefix Key):

   - 預設情況下，Screen 的前綴鍵是 Ctrl+A。
   - 當您想要執行一個 Screen 命令時，您需要先按下前綴鍵，然後放開，再按下第二個鍵。
   - 例如，要建立一個新視窗，您會依序按下 Ctrl+A，然後放開，再按下 c。

2. 命令 (Command):

   - 前綴鍵後面跟隨的第二個鍵，就是您要執行的 Screen 命令。
   - 這些命令可以是內建功能（如建立視窗），也可以是您在 .screenrc 設定檔中定義的自訂操作。

### default key binding

以下是一些最常用且值得您熟記的預設鍵盤綁定：

| 快捷鍵                        | 指令名稱      | 說明                            |
| ----------------------------- | ------------- | ------------------------------- |
| C-a '                         | select        | 提示輸入視窗名稱或編號以切換    |
| C-a "                         | windowlist -b | 顯示所有視窗供選擇              |
| C-a 0~9                       | select 0-9    | 切換到第 0-9 號視窗             |
| C-a -                         | select -      | 切換到 0-9 號視窗或空白視窗     |
| C-a tab                       | focus         | 切換輸入焦點至下一區域          |
| C-a C-a                       | other         | 切回前一個顯示的視窗            |
| C-a a                         | meta          | 將 C-a 字元送至視窗             |
| C-a A                         | title         | 為目前視窗命名                  |
| C-a b / C-a C-b               | break         | 傳送 break 訊號至視窗           |
| C-a B                         | pow_break     | 重新開啟終端線並傳送 break      |
| C-a c / C-a C-c               | screen        | 建立新視窗並切換至該視窗        |
| C-a C                         | clear         | 清除螢幕內容                    |
| C-a d / C-a C-d               | detach        | 分離 screen                     |
| C-a D D                       | pow_detach    | 分離並登出                      |
| C-a f / C-a C-f               | flow          | 切換 flow 控制狀態              |
| C-a F                         | fit           | 視窗調整為目前區域大小          |
| C-a C-g                       | vbell         | 切換視覺鈴聲模式                |
| C-a h                         | hardcopy      | 將目前畫面寫入 `hardcopy.n`     |
| C-a H                         | log           | 開始/停止記錄至 `screenlog.n`   |
| C-a i / C-a C-i               | info          | 顯示目前視窗資訊                |
| C-a k / C-a C-k               | kill          | 關閉目前視窗                    |
| C-a l / C-a C-l               | redisplay     | 完整刷新目前視窗                |
| C-a L                         | login         | 切換視窗登入狀態（需支援 utmp） |
| C-a m / C-a C-m               | lastmsg       | 顯示上一則訊息                  |
| C-a M                         | monitor       | 切換監控目前視窗狀態            |
| C-a space / n / C-n           | next          | 切換到下一個視窗                |
| C-a N                         | number        | 顯示目前視窗號碼與標題          |
| C-a backspace / p / C-p / C-h | prev          | 切換到前一個視窗                |
| C-a q / C-a C-q               | xon           | 傳送 Ctrl-Q                     |
| C-a Q                         | only          | 刪除其他區域，只保留目前區域    |
| C-a r / C-a C-r               | wrap          | 切換自動換行狀態                |
| C-a s / C-a C-s               | xoff          | 傳送 Ctrl-S                     |
| C-a S                         | split         | 水平分割區域                    |
| C-a t / C-a C-t               | time          | 顯示系統資訊                    |
| C-a v                         | version       | 顯示版本與編譯日期              |
| C-a C-v                       | digraph       | 輸入組合字元                    |
| C-a w / C-a C-w               | windows       | 顯示視窗清單                    |
| C-a W                         | width         | 切換 80/132 欄                  |
| C-a x / C-a C-x               | lockscreen    | 鎖定螢幕                        |
| C-a X                         | remove        | 關閉目前區域                    |
| C-a z / C-a C-z               | suspend       | 暫停 screen                     |
| C-a Z                         | reset         | 重設虛擬終端為開機狀態          |
| C-a .                         | dumptermcap   | 輸出 `.termcap` 檔              |
| C-a ?                         | help          | 顯示快捷鍵說明                  |
| C-a \                         | quit          | 關閉所有視窗並結束 screen       |
| C-a :                         | colon         | 進入指令列模式                  |
| C-a [ / C-[ / esc             | copy          | 進入複製/滾動模式               |
| C-a C-] / C-a ]               | paste .       | 貼上剪貼簿內容到目前視窗        |
| C-a { / C-a }                 | history       | 複製並貼上先前命令列            |
| C-a >                         | writebuf      | 將剪貼簿寫入檔案                |
| C-a <                         | readbuf       | 讀取交換檔至剪貼簿              |
| C-a =                         | removebuf     | 刪除交換用的檔案                |
| C-a ,                         | license       | 顯示版權與授權資訊              |
| C-a \_                        | silence       | 開始/停止監控視窗閒置狀態       |
| C-a \|                        | split -v      | 垂直分割區域                    |
| C-a \*                        | displays      | 顯示目前所有已連接的螢幕        |

---

## hardstatus

設定用於在 GNU Screen 終端機底部（或頂部）顯示一個狀態列。這個狀態列可以顯示各種有用的資訊，例如主機名稱、目前視窗、其他視窗列表、系統負載等。

幾種常見的寫法:

1. hardstatus alwayslastline

這條命令本身只表示狀態列始終顯示在終端機的最後一行。

要定義顯示的內容，通常會搭配 hardstatus string 使用。

2. hardstatus string "格式字串"

這是定義狀態列內容最主要的方式。"格式字串" 包含了您想要顯示的文字、格式化碼和顏色設定。

3. hardstatus alwayslastline "格式字串"

這種寫法是前兩者的簡化結合，直接在 alwayslastline 後面接上格式字串，效果等同於同時使用了 alwayslastline 和 hardstatus string。如果您的設定檔中有多條這樣的命令，只有最後一條會生效。

常用格式化碼:

1. 視窗相關資訊

   - %n: 目前視窗的編號 (Window number)。
   - %t: 目前視窗的標題 (Window title)。
   - %f: 目前視窗的旗標 (Window flags)，例如 \* 表示目前視窗，$ 表示活動變更的視窗，! 表示有輸出變化，\_ 表示有警示聲等。
   - %w: 顯示所有視窗的列表。這會列出所有視窗的編號和標題。
   - %W: 類似 %w，但會高亮顯示目前視窗。
   - %-w: 顯示前一個視窗的列表。如果沒有前一個視窗，則不顯示。
   - %+w: 顯示後一個視窗的列表。

2. 時間與日期

   - %c: 顯示目前時間 (HH:MM)。
   - %c:: 顯示目前時間 (HH:MM:SS)。
   - %d: 顯示日期 (DD)。
   - %M: 顯示月份 (Jan, Feb 等)。
   - %Y: 顯示年份 (YYYY)。
   - %m: 顯示月份 (MM)。
   - %D: 顯示星期幾 (Mon, Tue 等)。
   - %s: 顯示秒數 (SS)。
   - %S: 顯示自 1970 年 1 月 1 日以來的秒數。

3. 系統與用戶資訊

   - %H: 顯示主機名稱 (Hostname)。
   - %l: 顯示系統平均負載 (Load average)。
   - %u: 顯示目前登入的使用者名稱 (Username)。
   - %a: 顯示系統架構 (e.g., x86_64)。

4. 對齊與填充

   - %<: 左對齊。這個標記後面的內容會靠左顯示。
   - %<...%=: 任何放在 %= 之前的內容都會被靠左對齊，而 %= 之後的內容會靠右對齊。
   - %|: 右對齊。
   - %: 將剩餘的空間填滿空格。
   - %X：填充到 X 個字元寬。

5. 顏色設定 (Color Escapes)

顏色設定碼以 %{ 開頭，以 } 結尾。格式通常是 %{屬性 前景顏色 背景顏色}。

a. 屬性:

- =：設定背景色和前景。
- !：反轉前景和背景色。
- +：開啟屬性（如粗體）。
- -：關閉屬性（如粗體）。
- \_：底線。
- \*：閃爍。

b. 顏色:

- k: 黑色 (black)
- r: 紅色 (red)
- g: 綠色 (green)
- y: 黃色 (yellow)
- b: 藍色 (blue)
- m: 洋紅色 (magenta)
- c: 青色 (cyan)
- w: 白色 (white)
- K, R, G, Y, B, M, C, W: 對應的亮色版本（如 K 是亮黑）。

%{-}: 重置所有顏色和屬性為預設值。

```bash
# ~/.scrrenrc
caption splitonly "%{= bK} %{= bG} [%n] %t @ %H"
hardstatus alwayslastline "%{= GK} %-Lw%{= KY}%n%f %t%{-}%+Lw %{= BW} %=| %0c:%s  %Y-%m-%d"
```

---

## screenrc

```bash
# Set disable startup message
startup_message off

# Set automatically name
autoname on

# Set scrollback line
defscrollback 1024

# Set default encoding using utf8
defutf8 on

# Set visual bell
vbell on

# Set key binding
bindkey ^[l next       # next window
bindkey ^[h prev       # previous window
bindkey ^[k focus      # next region
bindkey ^[j focus prev # previous region

# Set default screen
chdir $HOME
screen -t my      0 /bin/zsh
chdir $HOME/workspace
screen -t work    1 /bin/bash

caption splitonly "%{= bK} %{= bG} [%n] %t @ %H"
hardstatus alwayslastline "%{= GK} %-Lw%{= KY}%n%f %t%{-}%+Lw %{= BW} %=| %0c:%s  %Y-%m-%d"
```
