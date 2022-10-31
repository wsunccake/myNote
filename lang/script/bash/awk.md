# awk

## run

```bash
linux:~ # seq 5 | awk ' { sum = sum + $1 } END { print sum }'

# awk access shell variable
linux:~ # awk -v today="`date`" 'BEGIN {print today}'

# awk access environment variable
linux:~ # awk 'BEGIN {print ENVIRON["HOME"]}'

# awk argument
linux:~ # awk 'BEGIN {print ARGV[0], ARGV[1]}' "`date`"

# awk script
linux:~ # cat avg.awk
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
linux:~ # awk '/<pattern>/{print $_}' <file>
linux:~ # awk '{if ($1 ~ /<pattern>/) print $_}' <file>
linux:~ # awk '{if ($1 == "<pattern>") print $_}' <file>
linux:~ # awk '$1 ~ /<pattern>/{print $_}' <file>
linux:~ # awk '$1 == "<pattern>"{print $_}' <file>

# double quote
linux:~ # awk "\$1 == \"<pattern>\" {printf \"$HOME %s\", \$_}" <file>

# NF: number fields (column), NR: number record (row), $_
linux:~ # awk '{if (NF < 3) {printf line %s, %s\n", NR, $_}}' <file>
linux:~ # ps aux | awk '{for (i = 11; i <= NF; i++) printf $i" "; print ""}'
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
