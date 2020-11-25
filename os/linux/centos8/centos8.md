# centos 8


## gui

### gnome3

after mini install, source from iso/image

```bash
centos:~ # mount -oloop CentOS-8.2.2004-x86_64-dvd1.iso /mnt
centos:~ # cp /mnt/media.repo /etc/yum.repos.d
centos:~ # vi /etc/yum.repos.d/media.repo
[AppStream]
name=AppStream
mediaid=None
metadata_expire=-1
gpgcheck=0
cost=500
baseurl=file:///mnt/AppStream

[BaseOS]
name=BaseOS
mediaid=None
metadata_expire=-1
gpgcheck=0
cost=500
baseurl=file:///mnt/BaseOS

centos:~ # yum makecache
centos:~ # yum repolist
centos:~ # dnf install @'Server with GUI'

centos:~ # systemctl set-default graphical
centos:~ # systemctl isolate graphical
```


### gnome3 tweak 

```bash
centos:~ # dnf install gnome-tweaks
```

[Tweaking GNOME Desktop Environment on CentOS 8](https://linuxhint.com/tweaking_gnome_desktop_centos8/)

[How to Show Desktop in GNOME](https://itsfoss.com/show-desktop-gnome-3/)


---

## repository

### epel

```bash
centos:~ # dnf install epel-release
```


---

## develop


### openjdk

```bash
centos:~ # dnf install java-11-openjdk-devel
```


### git

```bash
centos:~ # dnf install git
```


---

## editor/ide

### sublime

```bash
centos:~ # rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg
centos:~ # wget -P /etc/yum.repos.d/ https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
centos:~ # dnf install sublime-text
```


### vscode

```bash
centos:~ # rpm --import https://packages.microsoft.com/keys/microsoft.asc
centos:~ # echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo
centos:~ # dnf check-update
centos:~ # dnf install code
```


### intellij idea

```bash
# intellij idea
centos:~ # vi ~/.local/share/applications/idea.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=IntelliJ IDEA
Icon=/opt/idea-IU-143.1821.5/bin/idea.sh/idea.png
Exec="/opt/idea-IU-143.1821.5/bin/idea.sh" %f
Comment=Develop with pleasure!
Categories=Development;IDE;
Terminal=false
StartupWMClass=jetbrains-idea

# /usr/share/applications/
# /usr/local/share/applications/
# ~/.local/share/applications
```


---

## browser

### chrome

```bash
# chrome
centos:~ # wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
centos:~ # dnf install google-chrome-stable_current_x86_64.rpm
```


---

## terminal

### zsh

```bash
centos:~ # dnf install zsh
```


### oh-my-zsh

```bash
centos:~ # sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```


### fzf

```bash
centos:~ # git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
centos:~ # ~/.fzf/install

# fzf for bash
centos:~ # vi ~/.bashrc
...
[ -f ~/.fzf.bash ] && source ~/.fzf.bash

centos:~ # vi ~/.fzf.bash
# Setup fzf
# ---------
if [[ ! "$PATH" == *$HOME/.fzf/bin* ]]; then
  export PATH="${PATH:+${PATH}:}$HOME/.fzf/bin"
fi

# Auto-completion
# ---------------
[[ $- == *i* ]] && source "$HOME/.fzf/shell/completion.bash" 2> /dev/null

# Key bindings
# ------------
source "$HOME/.fzf/shell/key-bindings.bash"

# fzf for zsh
centos:~ # vi ~/.zshrc
...
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
cat ~/.fzf.zsh
# Setup fzf
# ---------
if [[ ! "$PATH" == *$HOME/.fzf/bin* ]]; then
  export PATH="${PATH:+${PATH}:}$HOME/.fzf/bin"
fi

# Auto-completion
# ---------------
[[ $- == *i* ]] && source "$HOME/.fzf/shell/completion.zsh" 2> /dev/null

# Key bindings
# ------------
source "$HOME/.fzf/shell/key-bindings.zsh"
```

