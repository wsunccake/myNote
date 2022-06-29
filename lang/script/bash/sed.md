# sed

## basic

```bash
linux:~ $ cat << EOF > data.csv
Andy Jiang, ACA-4566, 10
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10
John Cheng, YKC-7722, 10
Kevin Lin, NI2-039, 100
David Lee, 2C-323, 200
Herry McGray Jr., 3C-123, 500
LeeLongDa, 3C-123, 500
EOF

# show m ~ n
linux:~ $ sed -n 2,4p data.csv
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10
John Cheng, YKC-7722, 10

# show m and n
linux:~ $ sed -n '2p;4p' data.csv
Joe Hwang, M16-1226, 20
John Cheng, YKC-7722, 10

# show pattern<m> ~ pattern<n> (no greedy)
linux:~ $ sed -n '/Joe/,/Cheng/p' data.csv
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10

# show pattern<m> and pattern<n>
linux:~ $ sed -n '/Joe/p;/Cheng/p' data.csv
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10
John Cheng, YKC-7722, 10

# show 1 line to pattern
linux:~ $ sed '/Tim/q' data.csv
Andy Jiang, ACA-4566, 10
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10
```


---

## script

```bash
linux:~ $ cat << EOF > s1.sed
2,4p
EOF
linux:~ $ sed -n -f s1.sed data.csv

linux:~ $ cat << EOF > s2.sed
2p;4p
EOF
linux:~ $ sed -n -f s2.sed data.csv

linux:~ $ cat << EOF > s3.sed
/Joe/,/Cheng/p
EOF
linux:~ $ sed -n -f s3.sed data.csv

linux:~ $ cat << EOF > s4.sed
/Joe/p;/Cheng/p
EOF
linux:~ $ sed -n -f s4.sed data.csv

linux:~ $ cat << EOF > s5.sed
/Tim/q
EOF
linux:~ $ sed -n -f s5.sed data.csv
```


---

## remove character

```bash
linux:~ $ echo "Hello BASH script" | sed 's/.//6g'
Hello

linux:~ $ echo "Hello BASH script" | sed 's/.\{6\}//'
BASH script

linux:~ $ echo "Hello BASH script" | sed 's/.\{6\}//;s/.//5g'
BASH
```


---

## prefix and suffix

```bash
# no greedy suffix
linux:~ $ echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/\(.*\)\..*$/\1/'
/usr/lib/python/site-package/xxx-1.0/yyy

# greedy suffix
linux:~ $ echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/\..*$//'
/usr/lib/python/site-package/xxx-1

# no greedy prefix
linux:~ $ echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/\///'
usr/lib/python/site-package/xxx-1.0/yyy.zz

# greedy prefix
linux:~ $ echo /usr/lib/python/site-package/xxx-1.0/yyy.zz | sed 's/.*\///'
yyy.zz
```


---

## remove

```bash
linux:~ $ sed /Tim/d data.csv
Andy Jiang, ACA-4566, 10
Joe Hwang, M16-1226, 20
John Cheng, YKC-7722, 10
Kevin Lin, NI2-039, 100
David Lee, 2C-323, 200
Herry McGray Jr., 3C-123, 500
LeeLongDa, 3C-123, 500

linux:~ $ sed /Tim/,/Herry/d data.csv
Andy Jiang, ACA-4566, 10
Joe Hwang, M16-1226, 20
LeeLongDa, 3C-123, 500

# remove ^M (windows carry return)
linux:~ $ sed "s/\r//g" <file>
```


---

## substitute


---

## common

```bash
sed 's/\x1b\[[0-9;]*m//g' <file>    # remove color code

sed $'s/\r$//' <file>               # dos to unix
sed $'s/$/\r/' <file>               # unix to dos
```
