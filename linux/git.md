# Git #


## Environment ##

```
linux:~ $ git config --global user.name 'owner' # 設定使用者名稱 
linux:~ $ git config --global user.email 'owner@localhost' # 設定email 
linux:~ $ git config --global core.editor vim # 設定文字編輯器 
linux:~ $ git config --global merge.tool vimdiff # 設定比較工具 
linux:~ $ git config --global color.ui true # 設定顯示顏色 
linux:~ $ git config --global apply.whitespace nowarn # 忽略空白的變化, 空白對有些語言是有影響的 (像是 Ruby) 
linux:~ $ git config --global alias st status # 設定別名, 打 git st 就等同於打 git status 
linux:~ $ git config --list # 顯示當前設定

linux:~ $ cat ~/.gitconfig 
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
```


## Normal ##

```
# download project
linux:~ $ git clone git@github.com:user/sandbox.git # 下載 project 
linux:~ $ git clone git@github.com:user/sandbox.git newproejct # 下載 project 並改名為 newproject 

# file status
linux:~/project $ git add file # 檔案納入控制系統 
linux:~/project $ git rm file # 檔案移出制系統 

linux:~/project $ git commit -m 'initial project version' # 提交到控制系統 
linux:~/project $ git commit --amend # 編輯 commit

linux:~/project $ git status # version記錄 

linux:~/project $ git log # commit記錄 
linux:~/project $ git log -1 # show HEAD
linux:~/project $ git log --graph --oneline --all --decorate 
linux:~/project $ git log --graph --oneline --all --decorate --boundary --date-order 

# branch, checkout, fetch
linux:~/project $ git branch # 顯示分支
linux:~/project $ git branch --all
linux:~/project $ git branch b1 # 新增分支
linux:~/project $ git branch -d b1 # 刪除分支

linux:~/project $ git checkout -b b1 # 新增分支
linux:~/project $ git checkout b1 # 切換分支

linux:~/project $ git fetch
linux:~/project $ git fetch --all

# push, pull
linux:~/project $ git push
linux:~/project $ git pull
```


## Merge

```
   b1              b1 
   /     =>      /    \ 
v1 - v2       v1 - v2 - v3
```

```
linux:~/project $ git checkout v2 
linux:~/project $ git merge b1
```


## Rebase

```
   b1 
   /     => 
v1 - v2       v1 - v2 - v3
```

```
linux:~/project $ git checkout v2 
linux:~/project $ git rebase b1
```


## Reset

| option 	 | HEAD 	 | index | workdir 	 |
| ---------- | --------- | ----- | --------- |
| --soft 	 | Y		 | 		 | 			 |
| --mixed 	 | Y 		 | Y 	 | 			 |
| --hard 	 | Y 		 | Y 	 | Y 		 |

```
linux:~/project $ git reset HEAD
linux:~/project $ git reset --mixed HEAD # 同上
linux:~/project $ git reset --soft HEAD
linux:~/project $ git reset --hard HEAD
```


## Stash

```
linux:~/project $ git stash      # 先將以改修改過的 code 存入 stash
linux:~/project $ git pull
linux:~/project $ git stash pop  # 再將以改修改過的 code 從 stash 寫回

# pull code step:
linux:~/project $ git stash
linux:~/project $ git show stash
linux:~/project $ git pull --rebase
linux:~/project $ git stash pop

# push code step:
linux:~/project $ git show --pretty="" --name-only 53bd8b2
linux:~/project $ git stash
linux:~/project $ git pull --rebase
linux:~/project $ git push
linux:~/project $ git log
linux:~/project $ git stash pop
```