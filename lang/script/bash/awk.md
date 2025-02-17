# awk

## run

```bash
linux:~ $ seq 5 | awk ' { sum = sum + $1 } END { print sum }'

# awk access shell variable
linux:~ $ awk -v today="`date`" 'BEGIN {print today}'

# awk access environment variable
linux:~ $ awk 'BEGIN {print ENVIRON["HOME"]}'

# awk argument
linux:~ $ awk 'BEGIN {print ARGV[0], ARGV[1]}' "`date`"

# awk script
linux:~ $ cat avg.awk
#!/usr/bin/awk -f

BEGIN {
  sum = 0
}

{
  sum = sum + $1
}

END {
  print("count:", NR)
  print "sum: ", sum
  printf "average: %f\n", sum / NR
}
```

---

## pattern

```bash
# regrex
linux:~ $ awk '/<pattern>/{print $_}' <file>
linux:~ $ awk '{if ($1 ~ /<pattern>/) print $_}' <file>
linux:~ $ awk '{if ($1 == "<pattern>") print $_}' <file>
linux:~ $ awk '$1 ~ /<pattern>/{print $_}' <file>
linux:~ $ awk '$1 == "<pattern>"{print $_}' <file>

# double quote
linux:~ $ awk "\$1 == \"<pattern>\" {printf \"$HOME %s\", \$_}" <file>

# NF: number fields (column), NR: number record (row), $_
linux:~ $ awk '{if (NF < 3) {printf line %s, %s\n", NR, $_}}' <file>
linux:~ $ ps aux | awk '{for (i = 11; i <= NF; i++) printf $i" "; print ""}'
```

---

## hash

```awk
BEGIN {
  sum = 0
  count = -
}

{
  if ($2 ~ /^[[:digit:]]+$/) {
    sum += sum
    count += 1

    if ($1 in attr_data) {
      attr_data[$1] += $2
      attr_count[$1] += 1
    } else {
      attr_data[$1] = $2
      attr_count[$1] = 1
    }
}

END {
  for (k in attr_data) {
    printf("%s -> %d, %d, %f\n", k, attr_data[k], attr_count[k], attr_data[k] / attr_count[k]
  }
  printf("total sum: %d, count: %d, averag: %f\n", sum, count, sum / count)
}
```

---

## variable

```bash
# NR / number of record
linux:~ $ echo -e 'root\nadmin' | awk '{ print NR, $0 }'
1 root
2 admin

# FNR / file number of record
linux:~ $ awk '{ print NR, $0 }' <file1> <file2>
1 line1 from <file1>
2 line2 from <file1>
1 line1 from <file2>
2 line2 from <file2>

# NF / number of field
linux:~ $ echo -e 'root admin\nsys' | awk '{ print NF, $_ }'
2 root admin
1 sys

# FS / field separator
linux:~ $ echo 'apple,banana,cherry' | awk 'BEGIN { FS="," } { print $1, $2 }'
apple banana

# OFS / output field separator
linux:~ $ echo 'script awk' | awk 'BEGIN { OFS=" - " } { print $1, $2 }'
script - awk

# RS / record separator
linux:~ $ echo 'apple,banana,cherry' | awk 'BEGIN { RS="," } { print $_ }'
apple
banana
cherry

# ORS / output record separator
linux:~ $ echo -e 'apple\nbanana\ncherry' | awk 'BEGIN { ORS="," } { print $_ }'
apple,banana,cherry,

# $0 / entire line
linux:~ $ echo 'apple banana cherry' | awk '{ print $0 }'
apple banana cherry

# $n / field reference
linux:~ $ echo 'apple banana cherry' | awk '{ print $1 }'
apple

# FILENAME
linux:~ $ awk '{ print FILENAME, NR, $0 }' <file>
<file> 1 line1
...

# ARGC / argument count
linux:~ $ awk 'BEGIN { print "Number of arguments:", ARGC }' <file1> <file2>
Number of arguments: 3

# ARGV / argument vector
linux:~ $ awk 'BEGIN { for (i = 0; i < ARGC; i++) print ARGV[i] }' <file1> <file2>
awk
<file1>
<file2>

# ENVIRON
linux:~ $ awk 'BEGIN { print ENVIRON["HOME"] }'

# IGNORECASE
linux:~ $ echo -e 'Apple\napple\nAPPLE' | awk 'BEGIN { IGNORECASE=1 } /apple/ { print $0 }'
Apple
apple
APPLE

# CONVFMT / conversion format
linux:~ $ awk 'BEGIN { CONVFMT="%.2f"; num=3.14159; print num }'
3.14

# OFMT / output format
linux:~ $ awk 'BEGIN { OFMT="%.2f"; print 123.456789 }'
123.46
```

---

## common

```bash
awk -v inp="$HOME/my.inp" '{print $1 > (f_inp "_" $2)}' <file>
# 變數與其他文字組合，應該將它們放在括號中 ( ... )，以確保正確解析。
# => (f_inp "_" $2) 會生成期望的文件名。

awk -v inp="$HOME/my.inp" 'BEGIN {ORS=" "} {print $1 > (f_inp "_" $2)}  END {print ""}' <file>
# ORS=" "           :將輸出的行分隔符（Output Record Separator）設置為空格。
# {print $0}        :輸出每一行。
# END {print ""}    :在最後加上換行符。


awk '{$1=""; print $0}' <file>
# 第一列清空（設為空字串），但行的其他部分仍然存在
awk '{$1=""; sub(/^ /, ""); print}' <file>
# 第一列清空包括後留空格（設為空字串），但行的其他部分仍然存在
```
