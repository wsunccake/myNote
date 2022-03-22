# gdb

## install

```bash
ubuntu:~ # apt install gdb
```


---

## usage

```c
// minimal.c
int main()
{
   int i = 1337;
   return 0;
}
```

```bash
linux:~ $ gcc -g -o minimal.exe minimal.c

# -g: enable extra debugging
# -o <file>: output file

linux:~ $ gdb minimal.exe

(gdb) list
(gdb) quit
```


```bash
(gdb) help
(gdb) help all

(gdb) print 1 + 2
(gdb) print (int) 9223372036854775807

# 載入 file
(gdb) file <file>
(gdb) list

# breakpoint
(gdb) break main            # add breakpoint by function
(gdb) break 4               # add breakpoint by line
(gdb) delete breakpoints 1  # delete breakpoint

(gdb) info breakpoints      # list breakpoint

(gdb) enable                # enable breakpoint
(gdb) disable               # disable breakpoint

(gdb) run

# 顯示 variable
(gdb) print i
(gdb) print &i

# 顯示 cache size of type
(gdb) print sizeof(i)
(gdb) print sizeof(int)
(gdb) print sizeof(double)

# 檢查 type
(gdb) ptype i
(gdb) ptype &i

# quit
(gdb) quit
```
