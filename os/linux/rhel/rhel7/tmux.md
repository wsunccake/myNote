# tmux

## install

```bash
linux:~ # yum install -y tmux

linux:~ # tmux info
# ctrl ^ b + ?
```

`prefix`: 預設是 `ctrl` ^ `b`

---

## command

```bash
linux:~ # tmux list-commands
linux:~ # tmux lscm
```

---

## session

```bash
# new session
linux:~ # tmux
linux:~ # tmux new-session -s <session_name>
linux:~ # tmux new -s <session_name>

# list session
linux:~ # tmux list-sessions
linux:~ # tmux ls

# choose session
linux:~ # tmux choose-session

# attach session
linux:~ # tmux attach-session
linux:~ # tmux attach
linux:~ # tmux att  [-dr] [-t <session_name>]

# deattch sessuin
linux:~ # tmux detach-client
linux:~ # tmux detach
linux:~ # tmux det
# ctrl ^ b + d
```

---

## window

```bash
# creat window
linux:~ # tmux new-window
# ctrl ^ b + c

# list window
linux:~ # tmux list-windows

# choose window
linux:~ # tmux choose-window

linux:~ # tmux next-window
# ctrl ^ b + n

linux:~ # tmux previous-window
# ctrl ^ b + p
```

---

## pane

```bash
# split horizon pane
linux:~ # tmux split-window
linux:~ # tmux splitw
linux:~ # tmux spl
# ctrl ^ b + "

# split vertical pane
linux:~ # tmux spl -h
# ctrl ^ b + %

# list pane
linux:~ # tmux list-panes
linux:~ # tmux lsp
linux:~ # tmux displayp

# move
linux:~ # tmux move-pane
linux:~ # tmux movep [-p <percentage>|-l <size>] -t <pane_id>
# ctrl ^ b + {, }
# ctrl ^ b + up, down, right, left
# ctrl ^ b + ctrl ^ up, down, right, left
```

---

## conf

```bash
linux:~ # vi ~/.tmux.conf
setw -g mode-keys emacs
set -g mouse on

# new-window -n bash /bin/bash
# new-window -n tcsh /bin/tcsh
# new-window -n zsh /bin/zsh
```

---

## other

```bash
# ctrl ^ b, s   ->  choose session
# ctrl ^ b, w   ->  choose window
# ctrl ^ b, q   ->  show pane number
# ctrl ^ b, :   ->  command mode

# ctrl ^ b, f
# ctrl ^ b, [   ->  copy mode
```

---

## script

```bash
#!/bin/sh

SESSION=mySession

WINDOW=0
tmux new-session -d -s ${SESSION}
tmux rename-window -t ${SESSION}:${WINDOW} 'WORKSPACE'
tmux send-keys -t ${SESSION}:${WINDOW} 'bash' C-m 'clear' C-m

WINDOW=1
tmux new-window -t ${SESSION}:${WINDOW} -n 'GIT'
tmux send-key -t ${SESSION}:${WINDOW} 'zsh' C-m

WINDOW=2
PANE=0
tmux new-window -t ${SESSION}:${WINDOW} -n 'IDE'
tmux split-window -t ${SEESION}:${WINDOW}.${SUB_WINDOW}
tmux split-window -h -t ${SEESION}:${WINDOW}.${PANE}
tmux resize-pane -t ${SEESION}:${WINDOW}.${PANE} -x 100 -y 100
```

```bash
# 1. 建立背景 Session 並預備防退機制
# new-session -d：在背景（Detached）建立一個新的 tmux session，不會立刻被切進去。
# -s my_job：將 session 命名為 my_job。
# 'top; exec sh'：要執行的指令。
tmux new-session -d -s my_job 'top; exec sh'

# 2. 開啟全程持續錄製
# pipe-pane -t my_job：指定針對 my_job 這個 session 的當前視窗。
tmux pipe-pane -t my_job "cat >> $HOME/sim_top.log"

# 3. 等待與畫面檢查
# capture-pane -pt my_job：抓取 my_job 當下的終端機畫面，並直接印在畫面上（-p 代表 print）。
# list-session：列出目前系統中所有的 tmux sessions，用來確認 my_job 是否還活著。
sleep 3
tmux capture-pane -pt my_job
tmux list-session

# 4. 模擬鍵盤輸入
tmux send-keys -t my_job "1" Enter
sleep 3

# 5. 畫面檢查與結束程式
# send-keys -t my_job C-c：隔空發送 Ctrl + C（C-c 在 tmux 中代表 Ctrl+C）。這會強制中斷並結束正在執行的 top 程式。
tmux capture-pane -pt my_job
tmux send-keys -t my_job C-c
tmux capture-pane -pt my_job

# 6. 停止錄製並清理環境
# pipe-pane -t my_job：後面留空不接指令，代表關閉、停止該 session 的錄製功能。
# kill-session -t my_job：徹底關閉並刪除 my_job 這個 session，釋放系統資源，完成整個自動化任務。
tmux pipe-pane -t my_job
tmux kill-session -t my_job
```

```bash
tmux new-session -d -s shell -n "bash" "/bin/bash"
tmux new-window -t shell -n tcsh "/bin/tcsh"
tmux new-window -t shell -n tcsh "/bin/zsh"

tmux capture-pane -S - -pt pcap:0
tmux capture-pane -S - -pt pcap:1
tmux capture-pane -S - -pt pcap:2
```

---

## copy mode

```bash
tmux show-options -gw mode-keys
tmux setw -g mode-keys emacs
tmux setw -g mode-keys vi
```

### emacs

- Copy
  1. 按 prefix + [ 進入複製模式。
  2. 用方向鍵移動到你想複製的起點。
  3. 按 Ctrl + Space (空白鍵) 開始選取。
  4. 移動方向鍵到終點（文字會反白）。
  5. 按 Alt + W 複製文字（這時會自動退出複製模式）。

- Paste
  - 在任何想貼上的地方，按下 prefix + ] 即可。

- Page Up / Page Down
  - Page Up：按 Alt + V（或直接按鍵盤上的 PageUp）
  - Page Down：按 Ctrl + V（或直接按鍵盤上的 PageDown）
  - 向上滾動半頁：Ctrl + Up
  - 向下滾動半頁：Ctrl + Down

- Search
  - 向後搜尋（由新到舊，往上找）：
    1. 按 Ctrl + S，最下方會出現 Search Down:（這裡的 Down 指的是在 buffer 記憶體裡往舊資料找，也就是畫面上往上翻）。
    2. 輸入要找的字，按 Enter。
    3. 重複按 Ctrl + S 可以跳到下一個相符的關鍵字。
  - 向前搜尋（由舊到新，往下找）：
    1. 按 Ctrl + R，最下方會出現 Search Up:（往新資料/畫面下方找）。
    2. 重複按 Ctrl + R 跳到下一個。
