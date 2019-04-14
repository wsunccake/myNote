# tmux

## install

```
linux:~ # yum install -y tmux
```


---

## command

```
linux:~ # tmux list-commands
linux:~ # tmux lscm
```


---

## session

```
# new session
linux:~ # tmux
linux:~ # tmux new-session <session_name>
linux:~ # tmux new -s <session_name>

# list session
linux:~ # tmux list-sessions
linux:~ # tmux ls

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


---

## pane

```
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
# ctrl ^ b + up, down, right, left
# ctrl ^ b + ctrl ^ up, down, right, left

```

