# lnav

## install

```bash
sle:~ # zypper addrepo https://download.opensuse.org/repositories/server:monitoring/SLE_15_SP2/server:monitoring.repo
sle:~ # zypper refresh
sle:~ # zypper install lnav
```


---

## usage

```bash
sle:~ # lnav [<file>|<dir>]
sle:~ # lnav -r [<compress file>]
```

```
?           help
q/Q         quit
j/k/h/l     up/down/left/right
g/G         top/end of file
f/F         next/previous file
e/E         next/previous error
w/W         next/previous warning
n/N         next/previous search
```
