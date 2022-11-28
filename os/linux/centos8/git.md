# git 2.x

## version

```bash
[linux:~ ] # git --version
git version 2.18.4
```


---

## remote branch

```bash
# create
[linux:~ ] # git branch <branch>
[linux:~ ] # git push origin <branch>

# delete
[linux:~ ] # git branch -d <branch>
[linux:~ ] # git push origin -d <branch>
```


---

## multi repo

```bash
# create repo
[linux:~/repo ] $ git init
[linux:~/repo ] $ git add <file>
[linux:~/repo ] $ git status
[linux:~/repo ] $ git commit -m "init repo"
[linux:~/repo ] $ git remote add origin <git uri>       # can't overwrite
[linux:~/repo ] $ git remote set-url origin <git uri>   # overwrite origin
[linux:~/repo ] $ git push -u origin master
[linux:~/repo ] $ git remote -v

# add second repo
[linux:~/repo ] $ git remote set-url --add --push origin <git uri>
[linux:~/repo ] $ git remote -v
[linux:~/repo ] $ git push

[linux:~/repo ] $ vi .git/config
[remote "origin"]
        url = <git uri 1>
        fetch = +refs/heads/*:refs/remotes/origin/*
        pushurl = <git uri 1>
        pushurl = <git uri 2>
# git uri:
# ssh://git@<git server>/<repo>.git     # for ssh
# git@<git server>/<repo>.git           # for ssh
# https://<git server>/<repo>.git       # for https

# example
[linux:~/repo ] $ git remote set-url origin <git uri>
[linux:~/repo ] $ git remote set-url --add --push origin <git mirror uri>
[linux:~/repo ] $ git branch -M master
[linux:~/repo ] $ git push -u origin --all
[linux:~/repo ] $ git push origin --tags
```


---

## credential

```bash
[linux:~/repo ] $ git config credential.https://example.com.username myusername
[linux:~/repo ] $ vi .git/config
[credential "https://example.com"]
        username = myusername

[linux:~/repo ] $ git config --list
[linux:~/repo ] $ git config credential.helper cache
[linux:~/repo ] $ git config credential.helper 'cache --timeout=3600'
[linux:~/repo ] $ git config credential.helper store
[linux:~/repo ] $ git config credential.helper 'store --file ~/.git-credentials'
[linux:~/repo ] $ cat .git-credentials

[linux:~/repo ] $ git config --unset credential.https://example.com.username
```
