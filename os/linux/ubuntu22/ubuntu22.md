# ubuntu 22.04

```bash
ubuntu:~ # apt update

ubuntu:~ # apt install
curl
git
vim
```

---

## cli

```bash
# bash
ubuntu:~ # apt install bash-completion

# zsh
ubuntu:~ # apt install zsh

# oh-my-zsh
ubuntu:~ $ chsh -s /bin/zsh
ubuntu:~ $ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
ubuntu:~ $ omz update

# oh-my-zsh config
ubuntu:~ $ vi ~/.zshrc
ZSH_THEME="robbyrussell"    -> ZSH_THEME="agnoster"
plugins=()                  -> plugins=(git tmux)
```

---

## gui

---

## service

```bash
# sshd
ubuntu:~ # apt install openssh-server

ubuntu:~ # systemctl enable sshd
ubuntu:~ # systemctl start sshd
ubuntu:~ # systemctl status sshd
```
