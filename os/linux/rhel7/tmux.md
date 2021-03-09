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

tmux new-session -d -s ${SESSION}
tmux rename-window -t ${SESSION}:0 'WORKSPACE'
tmux send-keys -t ${SESSION}:0 'bash' C-m 'clear' C-m
tmux new-window -t ${SESSION}:1 -n 'GIT'
tmux send-key -t ${SESSION}:1 'zsh' C-m 
tmux new-window -t ${SESSION}:2 -n 'IDE'
tmux split-window -t ${SEESION}:2.0
tmux split-window -h -t ${SEESION}:2.0
tmux resize-pane -t ${SEESION}:2.1 -x 100 -y 100
```
