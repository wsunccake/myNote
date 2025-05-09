# fedora 42

## cli

### bash-it

```bash
# install
fedora:~ $ git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it
fedora:~ $ ~/.bash_it/install.sh        # install
fedora:~ $ ~/.bash_it/uninstall.sh      # uninstall

# setting
fedora:~ $ export BASH_IT="~/.bash_it"
fedora:~ $ source $BASH_IT/bash_it.sh

# usage
fedora:~ $ bash-it help
fedora:~ $ bash-it version

fedora:~ $ bash-it show aliases
fedora:~ $ bash-it show completions
fedora:~ $ bash-it show plugins

fedora:~ $ bash-it enable plugin git
fedora:~ $ bash-it reload
fedora:~ $ bash-it help alias git

fedora:~ $ ls ~/.bash-it/themes
```

### fzf

```bash
fedora:~ $ git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
fedora:~ $ ~/.fzf/install

fedora:~ $ eval "$(fzf --bash)"

fedora:~ $ fzf -m
# ctrl-t ****：所選的物件會貼至命令列。
# ctrl-r ：開啟歷史指令列表，所選的指令會貼至命令列。
# alt-c  ：移動至所選的目錄。

```

### neovim

```bash
fedora:~ $ dnf install neovim
```

---

## service

### gnome-remote-desktop

fedora 42 開始用 Wayland, VNC 不支援 Wayland (支援 Xorg), 要使用 RDP (gnome-remote-desktop)

```bash
# GUI
fedora:~ $ gnome-control-center [system]
System -> Remote Desktop
Enable
Desktop Share
Remote Control

# CLI
fedora:~ $ gsettings list-recursively org.gnome.desktop.remote-desktop.rdp
fedora:~ $ gsettings get org.gnome.desktop.remote-desktop.rdp enable
fedora:~ $ gsettings set org.gnome.desktop.remote-desktop.rdp view-only false

fedora:~ $ systemctl status gnome-remote-desktop --user
fedora:~ $ systemctl enable gnome-remote-desktop --user --now

fedora:~ $ grdctl status
fedora:~ $ grdctl rdp enable
```
