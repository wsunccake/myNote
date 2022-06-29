# Git


## Environment

```bash
linux:~ $ git config --global user.name 'owner'            # 設定使用者名稱
linux:~ $ git config --global user.email 'owner@localhost' # 設定email
linux:~ $ git config --global core.editor vim              # 設定文字編輯器
linux:~ $ git config --global merge.tool vimdiff           # 設定比較工具
linux:~ $ git config --global color.ui true                # 設定顯示顏色
linux:~ $ git config --global apply.whitespace nowarn      # 忽略空白的變化, 空白對有些語言是有影響的 (像是 Ruby)
linux:~ $ git config --global alias.log-pretty 'log --graph --oneline --decorate --date-order' # 設定別名
linux:~ $ git config --list                                # 顯示當前設定

linux:~ $ cat ~/.gitconfig
[user]
    name = owner
    email = owner@localhost
[core]
    editor = vim
    pager =
[merge]
    tool = vimdiff
[color]
    ui = true
[alias]
    commit-show = commit -v -uno
    branch-all = branch -avv

    log-pretty = log --graph --oneline --decorate --date-order
#    log-pretty = log --graph --oneline --boundary --decorate --all --date-order
    log-full= log -C --stat --decorate
```


---

## Normal

```bash
# download project
linux:~ $ git clone git@github.com:user/sandbox.git            # download project
linux:~ $ git clone git@github.com:user/sandbox.git newproejct # download project to rename newproject
linux:~ $ ssh-agent bash -c 'ssh-add <private key>; git clone <ssh-repo>'   # use other private to download project

# file status
linux:~/project $ git add file                    # 檔案納入控制系統
linux:~/project $ git rm [--cache|-f] file        # 檔案移出制系統
linux:~/project $ git mv src_file des_file        # 檔案移出制系統

linux:~/project $ git commit -m '<my_comment>'    # 提交到控制系統
linux:~/project $ git commit -m                   # 提交到控制系統
linux:~/project $ git commit --amend              # 修改/編輯 commit

# rollback, 狀態改成前一次 commit
linux:~/project $ git reset HEAD^           # no record, only revert commit and keep change file
linux:~/project $ git reset HEAD^ --hard    # no record, revert commit and file

linux:~/project $ git status # version記錄

linux:~/project $ git log                     # commit記錄
linux:~/project $ git log -1                  # show HEAD
linux:~/project $ git log --graph --oneline --all --decorate
linux:~/project $ git log --graph --oneline --all --decorate --boundary --date-order
linux:~/project $ git log --graph --oneline --decorate=full --date-order --all
linux:~/project $ git log --graph --decorate=full --date-order --stat

# branch, checkout, fetch
linux:~/project $ git branch                # 顯示 branch
linux:~/project $ git branch --all          # 顯示所有 branch (包括 remote)
linux:~/project $ git branch <branch>       # 新增 branch
linux:~/project $ git branch -d <branch>    # 刪除 branch

linux:~/project $ git checkout -b <branch>  # 新增 branch
linux:~/project $ git checkout <branch>     # 切換 branch

# same checkout -b for previous version
linux:~/project $ git branch <branch> origin/<branch>
linux:~/project $ git checkout <branch>

linux:~/project $ git fetch
linux:~/project $ git fetch --all

# push, pull
linux:~/project $ git push
linux:~/project $ git pull

# remote
linux:~/project # git remote -v
linux:~/project # git remote add origin <url>
linux:~/project # git remote set-url origin <url>
linux:~/project # git push -u origin master
```


## Merge

```bash
   b1              b1
   /     =>      /    \
m1 - m2       m1 - m2 - m3
```

```bash
linux:~/project $ git checkout m2
linux:~/project $ git merge b1
```


### fast-forward

```bash
   b1
   /     =>
m1              m1  - b1
```

```bash
linux:~/project $ git checkout m1
linux:~/project $ git merge [--ff] b1
```


```bash
   b1              b1
   /     =>      /    \
m1 - m2       m1  ---  m2
```

```bash
linux:~/project $ git checkout m2
linux:~/project $ git merge --no-ff b1
```



## Rebase

```bash
   b1
   /     =>
v1 - v2       v1 - v2 - v3
```

```bash
linux:~/project $ git checkout v2
linux:~/project $ git rebase b1
```

```bash
c1 -> c2 -> c3  =>  c1 -> c3
```

```bash
linux:~/project $ git checkout c3

linux:~/project $ git log --graph --oneline
* f47dc45 c3
* 1f93216 c2
* c28beea c1

linux:~/project $ git rebase -i  c1
pick 1f93216 c2
pick f47dc45 c3
->
pick 1f93216 c2
squash f47dc45 c3

linux:~/project $ git log --graph --oneline
* 445b1ba c3
* c28beea c1
```


## Stash

```bash
linux:~/project $ git stash                  # 先將以改修改過的 code 存入 stash
linux:~/project $ git list                   # 顯示所有 stash
linux:~/project $ git show [stash@{0}]
linux:~/project $ git apply [stash@{0}]
linux:~/project $ git drop  [stash@{0}]
linux:~/project $ git stash pop [stash@{0}]  # 再將以改修改過的 code 從 stash 寫回
linux:~/project $ git pull

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


## Reset

| option 	 | HEAD 	 | index | workdir 	 |
| ---------- | --------- | ----- | --------- |
| --soft 	 | Y		 | 		 | 			 |
| --mixed 	 | Y 		 | Y 	 | 			 |
| --hard 	 | Y 		 | Y 	 | Y 		 |

```bash
linux:~/project $ git reset HEAD
linux:~/project $ git reset --mixed HEAD # 同上
linux:~/project $ git reset --soft HEAD
linux:~/project $ git reset --hard HEAD
```


---

## Multi User

### push commit to remote server

`condition`

```bash
# user1
centos:~/project $ git add file1
centos:~/project $ git commit -m "Add file1"
centos:~/project $ git push

# user2
centos:~/project $ git add file2
centos:~/project $ git commit "Add file2"
centos:~/project $ git push
 ! [rejected]        master -> master (fetch first)
```

`action1`

```bash
*    (HEAD, master) Merge branch 'master'
|\
* |  Add file2
| *  (origin/master, origin/HEAD) Add file1
|/
*

# user2
centos:~/project $ git pull
centos:~/project $ git push

*  (HEAD, origin/master, origin/HEAD, master) Add 1
*  Add file1
*  first commit

centos:~/project $ git reset <hash add file1>
centos:~/project $ git pull
centos:~/project $ git add file2
centos:~/project $ git commit "Add file2"
centos:~/project $ git push
```

`action2`

```bash
# user2
centos:~/project $ git reset <hash Add file1>
centos:~/project $ git pull
centos:~/project $ git add file2
centos:~/project $ git commit "Add file2"
centos:~/project $ git push
```

`action3`

```bash
# user2
centos:~/project $ git stash
centos:~/project $ git stash list
centos:~/project $ git pull

centos:~/project $ git reset --hard <hash master>
centos:~/project $ git stash pop [<hash stash>]

# if Merge conflict in filex
centos:~/project $ vi filex
centos:~/project $ git stash drop [<hash stash>]
centos:~/project $ git add file2 filex
centos:~/project $ git commit "Add file2"
centos:~/project $ git push
```


---

## Tag

```bash
# add tag
linux:~/project # git tag <tag_name>

# del tag
linux:~/project # git tag -d <tag_name>

# push tag to remote
linux:~/project # git push origin <tag_name>    # one tag
linux:~/project # git push origin --tags        # all tag

# remove tag to remote
linux:~/project # git push -d origin <tag_name>
```


---

## Submodule

```bash
# add sub repo to repo
linux:~/repo $ git submodule add <sub-repo> <sub-path>
linux:~/repo $ cat .gitmodules
[submodule "<sub>"]
        path = <sub-path>
        url = <sub-repo>
linux:~/repo $ cat .git/config
linux:~/repo $ git commit -m "add sub repo"
linux:~/repo $ git push

# clone repo
linux:~ $ git clone <repo>
linux:~ $ cd repo

# clone sub repo
linux:~/repo $ git submodule status
linux:~/repo $ git submodule init <sub-path>
linux:~/repo $ git submodule update [--remote] <sub-path>
linux:~/repo $ ls <sub-path>

# pull latest sub repo
linux:~/repo $ cd <sub-path>
linux:~/repo/<sub-path> $ git pull <remote> <branch>
linux:~/repo/<sub-path> $ git pull origin master

# remove sub repo
linux:~/repo $ git rm [--cached] <sub-path>
linux:~/repo $ vi .gitmodules
linux:~/repo $ vi .git/config
linux:~/repo $ git submodule sync
linux:~/repo $ git commit -m "remove sub repo"

# example
## add submodule
linux:~/repo $  git submodule add https://github.com/wsunccake/sub_repo.git sub
linux:~/repo $  git commit -m "add sub_repo to be submodule"
linux:~/repo $  git push

## clone repo and submodule
linux:~ $ git clone https://github.com/wsunccake/repo
linux:~ $ cd repo
linux:~/repo $ ls sub
linux:~/repo $ git submodule status
linux:~/repo $ git submodule update --init --remote sub

## pull sub_repo / submodule update
linux:~/repo $ git submodule update --remote sub
linux:~/repo $ git submodule status
linux:~/repo $ git add sub
linux:~/repo $ git commit "update sub_repo"
linux:~/repo $ git push
```

