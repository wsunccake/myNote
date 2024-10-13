# powerline


## require

```
linux:~ # yum install python36
linux:~ # curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
linux:~ # python3 get-pip.py
```


---

## install


```
# for system
linux:~ # pip install powerline-status

# for user
linux:~ # pip install --user git+git://github.com/powerline/powerline
linux:~ # ls $HOME/.local/bin
```


---

## font

```
linux:~ # xset q

# method 1
linux:~ # git clone https://github.com/powerline/fonts.git --depth=1
linux:~ # cd fonts
linux:~ # ./install.sh

# method 2
linux:~ # wget https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf
linux:~ # wget https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf

linux:~ # mkdir -p ~/.local/share/fonts/
linux:~ # mv PowerlineSymbols.otf ~/.local/share/fonts/
linux:~ # fc-cache -vf ~/.local/share/fonts/
linux:~ # mkdir -p ~/.config/fontconfig/conf.d/
linux:~ # mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/
```


---

## usage

`bash`

```
linux:~ # vi .bashrc
powerline-daemon -q
POWERLINE_BASH_CONTINUATION=1
POWERLINE_BASH_SELECT=1
source ~/.local/lib/python3.6/site-packages/powerline/bindings/bash/powerline.sh
```

`vim`

```
# install pathogen
linux:~ # mkdir -p ~/.vim/autoload ~/.vim/bundle
linux:~ # curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

linux:~ # vi .vimrc 
set laststatus=2
python3 from powerline.vim import setup as powerline_setup
python3 powerline_setup()
python3 del powerline_setup
set rtp+=~/.local/lib/python3.6/site-packages/powerline/bindings/vim

execute pathogen#infect()
```

`tmux`

```
linux:~ # vi .tmux.conf
source ~/.local/lib/python3.6/site-packages/powerline/bindings/tmux/powerline.conf
```
