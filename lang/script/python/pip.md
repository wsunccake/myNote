# pip #

### Install ###

	osx:~ $ wget https://bootstrap.pypa.io/get-pip.py
	osx:~ $ python get-pip.py

	linux:~ $ sudo yum install python-pip
	linux:~ $ sudo apt-get install python-pip
	linux:~ $ sudo zypper install python-pip

	windows:


-----------------------------

### Usage ###

	# help
	linux:~ $ pip help
	linux:~ $ pip help install

	# install module
	linux:~ $ sudo pip install pkg.zip # 安裝下載的 module
	linux:~ $ sudo pip install [--install-option="--prefix=/path"] pkg[==ver]* # 線上安裝 module, 可指定版本

	linux:~ $ cat requirement.txt # 將欲安裝 module 寫在檔案裡
	Django==1.6
	selenium==2.39 
	linux:~ $ sudo pip install -r requirement.txt # 安裝檔案內的 module

	# uninstall module
	linux:~ $ pip uninstall pkg # 移除 module

	#upgrade module
	linux:~ $ linux:~ $ pip install -U pkg # 升級 module
	windows:~ $ pip -m pip install -U pkg

	# list & show
	linux:~ $ pip list # 列出現在已安裝的 module
	linux:~ $ pip freeze # 列出現在已安裝的 module

	linux:~ $ pip show module # 顯示 module 資訊
	linux:~ $ pip show -f module # 顯示 module 安裝檔案

	# search
	linux:~ $ pip search pkg # 搜尋線上有的 module


#### yolk ####

使 pip 搜尋軟體時, 沒辦法知道有哪些版本可以安裝, 此時就需要另外安裝 yolk

	linux:~ $ pip install yolk
	linux:~ $ yolk -V pip # 顯示可安裝的版本
-----------------------------
