# debian 11

## develop

### openjdk

```bash
debian:~ # apt update
debian:~ # apt install openjdk-11-jdk
```


### git

```bash
debian:~ # apt update
debian:~ # apt install git
```


---

## cli

### zsh

```bash
debian:~ # apt install zsh
```


### oh-my-zsh

```bash
debian:~ $ chsh -s /bin/zsh
debian:~ $ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### fzf

```bash
debian:~ $ git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
debian:~ $ ~/.fzf/install
```


### screen / tmux

```bash
debian:~ # apt install screen tmux
```


---

## gui

### vscode

```bash
debian:~ # apt install software-properties-common apt-transport-https curl
debian:~ # curl -sSL https://packages.microsoft.com/keys/microsoft.asc -o microsoft.asc
debian:~ # gpg --no-default-keyring --keyring ./ms_signing_key_temp.gpg --import ./microsoft.asc
debian:~ # gpg --no-default-keyring --keyring ./ms_signing_key_temp.gpg --export > ./ms_signing_key.gpg
debian:~ # mv ms_signing_key.gpg /etc/apt/trusted.gpg.d/
debian:~ # echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" | tee /etc/apt/sources.list.d/vscode.list

debian:~ # apt update
debian:~ # apt install code
```


### chrome

```bash
debian:~ # cat << EOF > /etc/apt/sources.list.d/google-chrome.list
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
EOF

debian:~ # wget -O- https://dl.google.com/linux/linux_signing_key.pub |gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg

debian:~ # apt update
debian:~ # apt install google-chrome-stable
```


### i3wm

```bash
debian:~ # apt update
debian:~ # apt install i3
```

