# bash text

## sort

```csv
11,v11
1,v1
2,v2
10,v10
8,v8
```

```bash
linux:~ $ sort <csv_file>                   # 依第一欄, ascii 順序排列
linux:~ $ sort <csv_file>                   # 依第一欄, 數值 順序排列
linux:~ $ sort -k2 -V <csv_file>            # 依第二欄, 版本 順序排列
linux:~ $ sort -k2,2V -k1,1 <csv_file>      # 依第二欄, 版本 順序排列, 再依第一欄, ascii 順序排列
```

## wc
