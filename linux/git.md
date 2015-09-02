# Git #


## Environment ##

	Linux:~ $ git config --global user.name 'owner' # 設定使用者名稱 
	Linux:~ $ git config --global user.email 'owner@localhost' # 設定email 
	Linux:~ $ git config --global core.editor vim # 設定文字編輯器 
	Linux:~ $ git config --global merge.tool vimdiff # 設定比較工具 
	Linux:~ $ git config --global color.ui true # 設定顯示顏色 
	Linux:~ $ git config --global apply.whitespace nowarn # 忽略空白的變化, 空白對有些語言是有影響的 (像是 Ruby) 
	Linux:~ $ git config --global alias st status # 設定別名, 打 git st 就等同於打 git status 
	Linux:~ $ git config --list # 顯示當前設定

	Linux:~ $ cat ~/.gitconfig 
	[user] 
	    name = owner 
	    email = owner@localhost 
	[core] 
	    editor = vim 
	[merge] 
	    tool = vimdiff 
	[color] 
	    ui = true 
	[alias] 
	    s = status -s -b -uno 
	    b = branch 
	    ba = branch -avv 
	
	    co = checkout 
	    ci = commit -v -uno 
	
	    l = log -C --stat --decorate 
	    t = log --graph --oneline --boundary --decorate --all --date-order


## Normal ##

	# download project
	Linux:~ $ git clone git@github.com:user/sandbox.git # 下載 project 
	Linux:~ $ git clone git@github.com:user/sandbox.git newproejct # 下載 project 並改名為 newproject 

	# file status
	Linux:~/project $ git add file # 檔案納入控制系統 
	Linux:~/project $ git rm file # 檔案移出制系統 

	Linux:~/project $ git commit -m 'initial project version' # 提交到控制系統 
	Linux:~/project $ git commit --amend # 編輯 commit

	Linux:~/project $ git status # version記錄 

	Linux:~/project $ git log # commit記錄 
	Linux:~/project $ git log -1 # show HEAD
	Linux:~/project $ git log --graph --oneline --all --decorate 
	Linux:~/project $ git log --graph --oneline --all --decorate --boundary --date-order 

	# branch, checkout, fetch
	Linux:~/project $ git branch # 顯示分支
	Linux:~/project $ git branch --all
	Linux:~/project $ git branch b1 # 新增分支
	Linux:~/project $ git branch -d b1 # 刪除分支

	Linux:~/project $ git checkout -b b1 # 新增分支
	Linux:~/project $ git checkout b1 # 切換分支

	Linux:~/project $ git fetch
	Linux:~/project $ git fetch --all

	# push, pull
	Linux:~/project $ git push
	Linux:~/project $ git pull

   b1              b1 
   /     =>      /    \ 
v1 - v2       v1 - v2 - v3

	# merge
	Linux:~/project $ git checkout v2 
	Linux:~/project $ git merge b1

   b1 
   /     => 
v1 - v2       v1 - v2 - v3

	# rebase
	Linux:~/project $ git checkout v2 
	Linux:~/project $ git rebase b1

reset 部分

| option 	 | HEAD 	 | index | workdir 	 |
| ---------- | --------- | ----- | --------- |
| --soft 	 | Y		 | 		 | 			 |
| --mixed 	 | Y 		 | Y 	 | 			 |
| --hard 	 | Y 		 | Y 	 | Y 		 |

	# reset
	Linux:~/project $ git reset HEAD
	Linux:~/project $ git reset --mixed HEAD # 同上
	Linux:~/project $ git reset --soft HEAD
	Linux:~/project $ git reset --hard HEAD 
