# tmux

## install

```bash
linux:~ # yum install -y tmux

linux:~ # tmux info
# ctrl ^ b + ?
```

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
setw -g mode-keys vi
set -g mouse on
```

---

## other

```bash
# ctrl ^ b, s   ->  choose session
# ctrl ^ b, w   ->  choose window
# ctrl ^ b, q   ->  show pane number
# ctrl ^ b, :   ->  command

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
# 1. 在背景 (-d) 建立一個名為 "my_job" (-s) 的新 Session。
#    並在裡面執行 'top; exec sh'。
#    核心技巧：當 'top' 被關閉時，'exec sh' 會立刻接手啟動一個 Shell，防止 tmux Session 因為程式結束而直接自動銷毀。
tmux new-session -d -s my_job 'top; exec sh'

# 2. 讓整個腳本暫停（睡眠）3 秒鐘。
#    這是為了給 'top' 指令一點時間初始化並刷出第一波系統效能畫面，避免後續的截圖抓到空白畫面。
sleep 3

# 3. 擷取 (capture) 名為 "my_job" 的 tmux 面板目前的畫面，並直接印在目前的螢幕上 (-p = print, -t = target)。
#    不必連進去，就能在當前終端機看到 top 的即時監控畫面。
tmux capture-pane -pt my_job

# 4. 列出目前系統中所有正在運行的 tmux Sessions。
#    用來二次確認 "my_job" 是否真的有在背景穩定執行中。
tmux list-session

# 5. 遠端遙控：對 "my_job" 發送按鍵 "1" 然後按下 Enter。
#    在 'top' 指令運作時，按下 "1" 代表「展開/切換所有 CPU 核心的獨立使用率」（由原本的總和變成看 CPU0, CPU1...）。
tmux send-keys -t my_job "1" Enter

# 6. 再度暫停 3 秒鐘，等待 top 接收到指令、重新計算並刷新 CPU 核心列表的畫面。
sleep 3

# 7. 再次對 "my_job" 的畫面進行截圖並印出。
#    這時候從輸出畫面上，應該就能看到原本總體的 CPU 使用率變成了各個核心（CPU0, CPU1...）分開顯示的狀態。
tmux capture-pane -pt my_job

# 8. 遠端遙控：對 "my_job" 發送 Ctrl + C 組合鍵（C-c）。
#    這會中斷並跳出正在執行的 'top' 行程。因為前面寫了 '; exec sh'，所以此時 top 結束後會停在 sh 提示字元（$）。
tmux send-keys -t my_job C-c

# 9. 第三次進行畫面截圖並印出。
#    此時畫面應該不會再有 top 的效能表格，而是會看到 top 結束後留下的最後畫面，以及等待輸入指令的 sh 命令列提示字元。
tmux capture-pane -pt my_job

# 10. 強行關閉並銷毀名為 "my_job" 的 tmux Session。
#     這會連同裡面剛剛殘留的 sh 一併結束，乾淨俐落地釋放系統資源，完成整個自動化測試任務。
tmux kill-session -t my_job
```
