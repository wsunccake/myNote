# pip

## install

```bash
# for rhel / centos
linux:~ # yum install python3-pip

# for debian / ubuntu
linux:~ # apt-get install python3-pip

# for sles / opensuse
linux:~ # zypper install python-pip

# for source code
linux:~ # wget https://bootstrap.pypa.io/get-pip.py
linux:~ # python3 get-pip.py
```

---

## usage

```bash
# help
linux:~ # pip help
linux:~ # pip help install

# install module
linux:~ # pip install <pkg>.zip # 安裝下載的 module
linux:~ # pip install [--install-option="--prefix=/path"] <pkg>[==ver]* [--user] # 線上安裝 module, 可指定版本

linux:~ # cat requirement.txt # 將欲安裝 module 寫在檔案裡
Django==1.6
selenium==2.39
linux:~ # pip install -r requirement.txt # 安裝檔案內的 module

# uninstall module
linux:~ # pip uninstall <pkg> # 移除 module

#upgrade module
linux:~ # pip install -U <pkg> # 升級 module

# list & show
linux:~ # pip list # 列出現在已安裝的 module
linux:~ # pip freeze # 列出現在已安裝的 module

linux:~ # pip show module # 顯示 module 資訊
linux:~ # pip show -f module # 顯示 module 安裝檔案
```

```bash
linux:~ # pip -V
linux:~ # pip list
linux:~ # pip help

# 安裝 virtualenv, pybuilder 為例子

# package
linux:~ # pip search virtualenv             # search package

linux:~ # pip install virtualenv            # install package
linux:~ # cat requirements.txt
pybuilder
linux:~ # pip install -r requirements.txt   # install package from requirements file
linux:~ # python -m pip install requests    # install package by module

linux:~ # pip install --upgrade pip         # upgrade package
linux:~ # pip uninstall requests            # remove package

# show package avaible version
linux:~ # pip index versions pylibmc                                  # pip >= 21.2
linux:~ # pip install pylibmc==                                       # pip >= 21.1
linux:~ # pip install --use-deprecated=legacy-resolver pylibmc==      # pip >= 20.3
linux:~ # pip install pylibmc==                                       # pip >= 9.0
linux:~ # pip install pylibmc==blork                                  # pip < 9.0
```

---

## private pypi

```bash
# command
linux:~ # pip install --trusted-host <pypi server> --index-url http://<pypi server>:<pypi port>/simple/ --upgrade <pkg>

# config
linux:~ # cat /etc/pip.conf
[global]
extra-index-url = http://<pypi server>:<pypi port>/simple/

[install]
trusted-host = <pypi server>

linux:~ # pip install --upgrade <pkg>
```

/etc/pip.conf, $HOME/.pip/pip.conf, $HOME/.config/pip/pip.conf

---

## yolk

使 pip 搜尋軟體時, 沒辦法知道有哪些版本可以安裝, 此時就需要另外安裝 yolk

```bash
linux:~ # pip install yolk
linux:~ # yolk -V pip # 顯示可安裝的版本
```
