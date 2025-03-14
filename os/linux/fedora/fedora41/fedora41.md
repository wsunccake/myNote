# fedora 41

## dnf

預設的 dnf 是 dnf5, 目前還有的沒整理到 dnf5 group

```bash
fedora:~ # dnf group list --hidden
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
fedora:~ # dnf group list --hidden
fedora:~ # dnf install @gnome-desktop

# chrome
fedora:~ # curl -OL https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
fedora:~ # dnf in google-chrome-stable_current_x86_64.rpm
```

## system

```bash
# network - dhcp
## methode 1
fedora:~ # nmcli connection add con-name enp0s1 ipv4.method auto type ethernet ifname enp0s1
## methode 2
fedora:~ # nmcli connection edit enp0s1 \
  ipv4.method auto

# network - ipv4
## methode 1
fedora:~ # nmcli connection add con-name enp0s1 \
  type ethernet ifname enp0s1 \
  ipv4.method manual \
  ipv4.addresses 192.0.2.10/24 \
  ipv4.gateway 192.0.2.254 \
  ipv4.dns 192.0.2.200
## methode 2
fedora:~ # nmcli connection edit enp0s1
nmcli> set ipv4.method manual
nmcli> set ipv4.addresses 192.0.2.10/24
nmcli> set ipv4.gateway 192.0.2.254
nmcli> set ipv4.dns 192.0.2.200
nmcli> save
nmcli> quit

# disable selinux
fedora:~ # sed s/^SELINUX=.*/SELINUX=disabled/ /etc/selinux/config
fedora:~ # grubby --update-kernel ALL --args selinux=0
fedora:~ # reboot

# extend lv
fedora:~ # lvresize -l +100%FREE /dev/fedora/root
fedora:~ # xfs_growfs /dev/fedora/root      # for xfs
fedora:~ # resize2fs /dev/vg_name/lv_name   # for ext4
```
