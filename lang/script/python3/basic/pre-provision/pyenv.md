# pyenv

## install

```bash
linux:~ $ curl -fsSL https://pyenv.run | bash     # $HOME/.pyenv

# for bash
linux:~ $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
linux:~ $ echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
linux:~ $ echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

# for zsh
linux:~ $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
linux:~ $ echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
linux:~ $ echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc

# require for build python
linux:~ # dnf install openssl-devel sqlite-devel
linux:~ # dnf install bzip2-devel xz-devel
linux:~ # dnf install libffi-devel
linux:~ # dnf install ncurses-devel readline-devel
```

## uninstall

```bash
linux:~ $ rm -rf ~/.pyenv

linux:~ # vi ~/.bashrc
# clear below config
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

linux:~ # vi ~/.zshrc
# clear below config
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"
```

---

## usage

```bash
# show all version
linux:~ $ pyenv versions

# install / uninstall
linux:~ $ pyenv install -l          # list all avaible version
linux:~ $ pyenv install [-v] <ver>  # install
linux:~ $ pyevn uninstall           # uninstall

# change python version
linux:~ $ pyenv global <ver>
linux:~ $ pyenv local <ver>
linux:~ $ pyenv shell <ver>
```
