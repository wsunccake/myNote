# fedora 41

## dnf

預設的 dnf 是 dnf5, 目前還有的沒整理到 dnf5 group

```bash
fedora:~ # dnf5 group list -v
fedora:~ # dnf4 group list -v
```

---

## develop

```bash
# python3
fedora:~ # dnf install python3
fedora:~ # dnf install python3-pip python3-virtualenv
fedora:~ # python3 --version
fedora:~ # pip3 --version

# nodejs
fedora:~ # dnf install nodejs
fedora:~ # node --version
fedora:~ # npm --version

# java
fedora:~ # dnf install java-17-openjdk-devel
fedora:~ # update-alternatives --config java
fedora:~ # dnf install maven
fedora:~ # mvn -version

fedora:~ $ echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk" >> ~/.bashrc
fedora:~ $ echo "export PATH=$JAVA_HOME/bin:$PATH" >> ~/.bashrc
fedora:~ $ source ~/.bashrc

# git
fedora:~ $ dnf install git

# vscode
fedora:~ # rpm --import https://packages.microsoft.com/keys/microsoft.asc
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | tee /etc/yum.repos.d/vscode.repo > /dev/null
fedora:~ # dnf check-update
fedora:~ # dnf install code

# intelliJ idea
fedora:~ # dnf install intellij-idea-community
```

---

## cli

```bash
# screen
fedora:~ # dnf in screen

# tmux
fedora:~ # dnf in tmux

# zsh
fedora:~ # dnf in zsh
fedora:~ $ chsh -s $(which zsh)

# oh-my-zsh
fedora:~ $ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# fzf
fedora:~ $ git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
fedora:~ $ ~/.fzf/install
```

---

## gui

```bash
# gnome
fedora:~ # dnf4 group install gnome-desktop

# chrome
fedora:~ # curl -OL https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
fedora:~ # dnf in google-chrome-stable_current_x86_64.rpm
```
