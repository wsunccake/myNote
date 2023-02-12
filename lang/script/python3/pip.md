# pip #

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


---

# private pypi

## install

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

# yolk

使 pip 搜尋軟體時, 沒辦法知道有哪些版本可以安裝, 此時就需要另外安裝 yolk

```bash
linux:~ # pip install yolk
linux:~ # yolk -V pip # 顯示可安裝的版本
```
