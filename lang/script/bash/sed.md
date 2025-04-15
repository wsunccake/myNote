# sed

## basic

```csv
Andy Jiang, ACA-4566, 10
Joe Hwang, M16-1226, 20
Tim Cheng, YKC-7725, 10
John Cheng, YKC-7722, 10
Kevin Lin, NI2-039, 100
David Lee, 2C-323, 200
Herry McGray Jr., 3C-123, 500
LeeLongDa, 3C-123, 500
```

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

## append / insert

```bash
# by line
linux:~ $ sed '1aAnn Su, XYZ-1122, 10' data.csv           # insert at 1 line
linux:~ $ sed '1aAnn Su, XYZ-1122, 10' data.csv           # append at 1 line
linux:~ $ sed '1,3aAnn Su, XYZ-1122, 10' data.csv         # append between 1 ~ 3 line
linux:~ $ sed '$aAnn Su, XYZ-1122, 10' data.csv           # append at last line
linux:~ $ sed '1a\Ann Su, XYZ-1122, 10' data.csv
linux:~ $ sed '1a\Ann Su, XYZ-1122, 10' data.csv

# by pattern
linux:~ $ sed '/Tim/a\Ann Su, XYZ-1122, 10' data.csv      # append at Tim line
linux:~ $ sed '/Tim/i\Ann Su, XYZ-1122, 10' data.csv      # insert at Tim line
```

---

## remove / delete

```bash
# by line
linux:~ $ sed '1d' data.csv                 # remove at 1 line
linux:~ $ sed '1,3d' data.csv               # remove between 1 ~ 3 line
linux:~ $ sed '$d' data.csv                 # remove at last line

# by pattern
linux:~ $ sed '/Tim/d' data.csv             # remove at Tim line
linux:~ $ sed '/Tim/,/Herry/d' data.csv     # remove between Tim and Herry line
```

---

## script

```bash
# script file
linux:~ $ cat << EOF > test.sed
2,4p
EOF
linux:~ $ sed -n -f test.sed data.csv

linux:~ $ sed -n [-f <sed_script1> [-f <sed_script2>]] <file>

# script
linux:~ $ sed -n -e '2,4p' data.csv

linux:~ $ sed -n [-e <sed1> [-e <sed2>]] <file>
```

```bash
2,4p
2p;4p
/Joe/,/Cheng/p
/Joe/p;/Cheng/p
/Tim/q
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

## substitute

---

## common

```bash
sed 's/\x1b\[[0-9;]*m//g' <file>    # remove color code

sed "s/\r//g" <file>                # remove ^M (windows carry return)
sed $'s/\r$//' <file>               # dos to unix
sed $'s/$/\r/' <file>               # unix to dos

sed ':a;N;$!ba;s/\n/ /g' <file>     # tr '\n' ' '
# :a          : 設置了一個標籤，類似於循環的開始點。
# N           : 將下一行追加到當前模式空間，從而處理多行文本。
# $!ba        : 如果還沒有到文件的末尾 ($! 表示“不是最後一行”)，則跳轉回標籤 :a，繼續追加。
# s/\n/ /g    : 將模式空間中的所有換行符 (\n) 替換為空格 ( )。
```

---

## buffer

pattern space: 預設每次讀入一行進來處理的內容
hold space: 額外的暫存空間（你可以放東西進去再拿出來）

| 指令    | 功能                                                                  |
| ------- | --------------------------------------------------------------------- |
| h       | 把 pattern space 複製到 hold buffer                                   |
| H       | 把 pattern space 加到 hold buffer（append）                           |
| g       | 把 hold buffer 複製回 pattern space                                   |
| G       | 把 hold buffer 加到 pattern space                                     |
| x       | 交換 pattern space 和 hold buffer                                     |
| n       | 讀下一行進入 pattern space（會自動印出原來的 pattern space，除非 -n） |
| N, P, D | 進階多行處理                                                          |

```txt
apple
banana
cherry
```

```bash
/banana/{
  h             # 複製原始行到 hold buffer
  s/.*/\u&!!/   # 修改成 Banana!!
  p             # 額外印出修改後的行
  g             # 從 hold buffer 取回原始行
}
```
