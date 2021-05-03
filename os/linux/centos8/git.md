# git 2.x

## version

```bash
[linux:~ ] # git --version
git version 2.18.4
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
```

