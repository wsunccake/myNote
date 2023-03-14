# pipeline

## basic

```zsh
# re-direct
echo "abc" > tmp.txt    # overwrite
echo "XYZ" >> tmp.txt   # append

cat << EOF >> tmp.txt
...
EOF
```

---

## file descritor

```zsh
cat | wc -l &
ls -l /proc/$(pidof cat)/fd
ls -l /proc/$(pidof wc)/fd

touch {0,1,2}.txt
{sleep 30 < 0.txt 1> 1.txt 2> 2.txt}&
my_pid=$!
# ls -l /proc/$(pidof sleep)/fd
ls -l /proc/$my_pid/fd
wait $my_pid
# 0: std in
# 1: std out
# 2: std err
```

---

## mkfifo

```zsh
mkfifo tmp.fifo
ls -l tmp.fifo
file tmp.fifo

wc < tmp.fifo &
cat << EOF > tmp.fifo
a
Z
0
EOF

rm tmp.fifo
```

---

## exec

```
# out
n> <file>: fd n redirect to <fille>
n>&m     : fd n redirect to fd m
n>&-     : close fd n output

# in
n< <file> : fd n
n<&m      : fd
n<&-      : close fd n input
```

```zsh
my_tty=$(tty)
exec 2> my.err
exec 1> my.out

ls -l
ls -l abcd
exec 1> $my_tty
exec 2> $my_tty

date
ls -l xyz
```
