# YUM #


## Package ##

YUM 在系統安裝時就已安裝, yum-utils 可協助設定 package 和 repository

	rhel:~ # yum install yum-utils
	rhel:~ # yum install createrepo


## Configuration ##

	# setup iso to repo
	rhel:~ # mount -oloop,ro rhel-server-7.2-x86_64-dvd.iso /mnt/rhel-server-7.2
	rhel:~ # yum-config-manager --add-repo file:///mnt/rhel-server-7.2
	rhel:~ # yum clean


## Command ##


### Repository ###

repositoory 以下簡稱 repo

	# list repo
	rhel:~ # yum repolist                        # 顯示可用的 repo, 僅 enable
	rhel:~ # yum repolist all                    # 顯示所有 repo, 包括 disable
	rhel:~ # yum-config-manager --disable <repo> # 停用 repo
	rhel:~ # yum-config-manager --enable <repo>  # 啟用 repo

	# add repo
	rhel:~ # yum-config-manager --add-repo file:///mnt/rhel-server-7.2
	rhel:~ # yum-config-manager --add-repo https://www.softwarecollections.org/repos/rhscl/python33/epel-7-x86_64

新增的 repo config 會在 /etc/yum.repo.d 目錄下


### Package ###

	# search package
	rhel:~ # yum serach <pkg>       # 搜尋 pkg, 包括 package name 及 summary
	rhel:~ # yum list *<pkg>*       # 搜尋 pkg, 只搜 package name, 可使用 regex
	rhel:~ # yum provides /path/cmd # 搜尋 pkg, 內有 command, 可配合 regex

	# info
	rhel:~ # yum info <pkg>
	rhel:~ # yumdb info <pkg>

	# install
	rhel:~ # yum install <pkg>
	rhel:~ # yum install -y <pkg>
	rhel:~ # yum localinstall <rpm_pkg>

	# uninstall
	rhel:~ # yum remove <pkg>
	rhel:~ # yum autoremove <pkg>

	# upgrade
	rhel~: # yum update -y --nogpgcheck
	rhel~: # yum upgrade -y --nogpgcheck

	# download package
	rhel:~ # yumdownloader pkackage_name

下載的 package 放在 /var/cache/yum/$basearch/$releasever/packages 目錄下


### Package Group ###

	# list 
	rhel:~ # yum groups list
	rhel:~ # yum groups info <pkg_grp>    # 顯示安裝 package

	# install
	rhel:~ # yum groups install <pkg_grp>
	rhel:~ # yum install @<pkg_grp>

	# uninstall
	rhel:~ # yum groups remove <pkg_grp>
	rhel:~ # yum remove @<pkg_grp>


### History ###

	# list
	rhel:~ # yum history [list]     # 顯示安裝紀錄, list 可省略
	rhel:~ # yum history list all
	rhel:~ # yum history list 1..3

	# info
	rhel:~ # yum info [his_id]      # 顯示該次安裝, 移除, 升級 package

	# undo/redo
	rhel:~ # yum history undo <his_id>
	rhel:~ # yum history redo <his_id>

	# new
	rhel:~ # yum history new        # 將之前安裝紀錄刪除, 小心使用

YUM 使用 SQLite 存放在 /var/lib/yum/history/ 目錄下


## Repository ##

	# create
	rhel:~ # createrepo --database /mnt/local_repo