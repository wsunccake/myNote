# npm

## install

會跟著 nodejs 一起安裝

---

## common

### help

```bash
linux:~ # npm -l          # all command/term
linux:~ # npm -h          # help
linux:~ # npm <term> -h   # command/term help

# example
linux:~ # npm version
linux:~ # npm version -h
linux:~ # npm help version
```

### file

```bash
# rc file
linux:~ # ls $HOME/.npmrc

# log file
linux:~ # ls $HOME/.npm/_logs
```

```bash
liunx:~/demo $ npm run
liunx:~/demo $ npm view
```

### local operation

```bash
liunx:~/demo $ npm list                     # alias: ls
liunx:~/demo $ npm install <pkg>[@<ver>]    # alias: in
liunx:~/demo $ npm uninstall <pkg>          # alias: rm
liunx:~/demo $ npm exec <cmd>               # alias: x

# example
liunx:~/demo $ npm in typescript
liunx:~/demo $ ls node_modules/typescript
liunx:~/demo $ npm x tsc
liunx:~/demo $ npm rm typescript
```

### global operation

```bash
liunx:~ $ npm -g ls
liunx:~ $ npm -g in ts-node
liunx:~ $ npm -g x ts-node
liunx:~ $ npm -g un ts-node
```

### other

```bash
linux:~ $ npm find <pkg>        # alias: se
```

---

## package

```bash
linux:~/demo $ npm init
linux:~/demo $ ls package.json

linux:~/demo $ npm config list
```
