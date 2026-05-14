# cli tool

## terminal

### nerd fonts

- [nerd fonts](https://www.nerdfonts.com/)

### ghostty

- [ghostty](https://ghostty.org/)

```bash
linux:~ $ ghostty +list-fonts

linux:~ $ vi ~/.config/ghostty/config
font-family = "FiraCode Nerd Font"
font-size = 16
```

---

## shell

### oh my zsh 

- [oh my zsh ](https://ohmyz.sh/)
- [ohmyzsh git](https://github.com/ohmyzsh/ohmyzsh)

```bash
linux:~ $ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

---

## editor

### neovim

- [neovim](https://neovim.io/)
- [neovim git](https://github.com/neovim/neovim)

```bash
# for linux
linux:~ $ curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz
linux:~ $ sudo tar -C /opt -xzf nvim-linux-x86_64.tar.gz
linux:~ $ sudo ln -s /opt/nvim-linux-x86_64/bin/nvim /usr/local/bin/.

# for macos
mac:~ $ curl -LO https://github.com/neovim/neovim/releases/download/nightly/nvim-macos-arm64.tar.gz
mac:~ $ sudo tar zxf nvim-macos-arm64.tar.gz -C /opt
mac:~ $ sudo ln -s /opt/nvim-macos-arm64/bin/nvim /usr/local/bin/.
```

### lazyvim

- [lazyvim](https://www.lazyvim.org/)
- [lazyvim git](https://github.com/lazyvim/lazyvim)

```bash
# backup required
linux:~ $ mv ~/.config/nvim{,.bak}

# backup optional but recommended
linux:~ $ mv ~/.local/share/nvim{,.bak}
linux:~ $ mv ~/.local/state/nvim{,.bak}
linux:~ $ mv ~/.cache/nvim{,.bak}

linux:~ $ git clone https://github.com/LazyVim/starter ~/.config/nvim

linux:~ $ nvim
```

---

## other

### fzf

- [fzg git](https://github.com/junegunn/fzf)

```bash
linux:~ $ git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
linux:~ $ ~/.fzf/install

linux:~ $ vi ~/.bashrc:
[ -f ~/.fzf.bash ] && source ~/.fzf.bash

linux:~ $ vi ~/.zshrc:
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

---

## develop

### uv

```bash
linux:~ $ curl -LsSf https://astral.sh/uv/install.sh | sh

# for bash
linux:~ $ echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
linux:~ $ echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc

# for zsh
linux:~ $ echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
linux:~ $ echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc
```