# run

## script

```zsh
#!/bin/zsh

echo "hello zsh"
print "hello zsh"
```


---

## execute by change mode

```zsh
linux:~ # chmod +x script.zsh
linux:~ # ./script.zsh
```


---

## execute by zsh command

```zsh
linux:~ # zsh script.zsh
```


---

## execute with environment variable

```zsh
linux:~ # export VAR=value
linux:~ # ./script.sh
```

---

## execute with environment variable

```zsh
linux:~ # env VAR=value ./script.sh
```


---

## execute with debug mode

```zsh
linux:~ # zsh -xv script.sh
```
