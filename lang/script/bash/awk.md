# awk


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
