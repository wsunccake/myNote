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
[linux:~ ] # git init
[linux:~ ] # git add <file>
[linux:~ ] # git status
[linux:~ ] # git commit -m "init repo"
[linux:~ ] # git remote add origin <git uri>
[linux:~ ] # git push -u origin master
[linux:~ ] # git remote -v

# add second repo
[linux:~ ] # git remote set-url --add --push origin <git uri>
[linux:~ ] # git remote -v
[linux:~ ] # git push

[linux:~ ] # vi .git/config
[remote "origin"]
        url = <git uri 1>
        fetch = +refs/heads/*:refs/remotes/origin/*
        pushurl = <git uri 1>
        pushurl = <git uri 2>
# git uri:
# ssh://git@<git server>/<repo>.git  # for ssh
# git@<git server>/<repo>.git  # for ssh
# https://<git server>/<repo>.git    # for https
```


---

## credential

```bash
[linux:~ ] # git config credential.https://example.com.username myusername
[linux:~ ] # vi .git/config
[credential "https://example.com"]
        username = myusername

[linux:~ ] # git config --list
[linux:~ ] # git config credential.helper cache
[linux:~ ] # git config credential.helper 'cache --timeout=3600'
[linux:~ ] # git config credential.helper store
[linux:~ ] # git config credential.helper 'store --file ~/.git-credentials'
[linux:~ ] # cat .git-credentials

[linux:~ ] # git config --unset credential.https://example.com.username
```
