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
(gdb) set language

(gdb) set print pretty
(gdb) print 1 + 2
(gdb) print (int) 9223372036854775807

# 載入 file
(gdb) file <file>
(gdb) list [<line number>]

# breakpoint
(gdb) break main            # add breakpoint by function
(gdb) break 4               # add breakpoint by line
(gdb) delete breakpoints 1  # delete breakpoint

(gdb) info breakpoints      # list breakpoint
(gdb) info variables
(gdb) info locals
(gdb) info args

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

---

## array

```c
// arr.c
int a[3];
struct { double v[3]; double length; } b[17];
int calendar[12][31];

int main() { return 0; }
```

```bash
linux:~ # gcc -Og -g -o arr arr.c
linux:~ # gdb -s arr
```

```bash
(gdb) b main
(gdb) r
(gdb) l
(gdb) l 1

(gdb) p sizeof(calendar)   # 1488 bytes
(gdb) p 1488 / 12 / 31     # 4
(gdb) p sizreof(int)       # 4 表示 4 bytes
(gdb) p sizeof(b)

(gdb) whatis calendar   # calendar 的 data type -> type = int [12][31]
(gdb) whatis b[0]       # b[0] 的 data type     -> type = struct {...}
(gdb) whatis &b[0]      # &b[0] 的 data type    -> type = struct {...} *

(gdb) x/4 b             # 以 16進位 後面 4 個 顯示 b 記憶體位置  -> 0x555555558640 <b>:	0	0	0	0
(gdb) p &b              # 顯示 b 記憶體位置                    -> (struct {...} (*)[17]) 0x555555558640 <b>
(gdb) p &(b[0]) + 1     # 顯示 b[0] 後一個 記憶體位置           -> (struct {...} *) 0x555555558660 <b+32>
                        # 32 bits = 4 bytes 是 double
(gdb) p &b[0]           # 顯示 b[0] 記憶體位置                 -> (struct {...} *) 0x555555558640 <b>

(gdb) p (&b[0])->v                  # -> {0, 0, 0}
(gdb) p (&b[0])->v = {1, 2, 3}      # -> {1, 2, 3}
(gdb) p b[0]                        # -> {v = {1, 2, 3}, length = 0}
(gdb) whatis (&b[0])->v[0]          # -> double
(gdb) p sizeof (&b[0])->v[0]        # -> 8

(gdb) p &(&b[0])->v[0]              # -> (double *) 0x555555558640 <b>
(gdb) p (int *) &(&b[0])->v[0]      # -> (int *) 0x555555558640 <b>
(gdb) p *(int *) &(&b[0])->v[0]     # -> 0
(gdb) x/4 (int *) &(&b[0])->v[0]    # -> 0x555555558640 <b>:	0	1072693248	0	1073741824
```

---

## config

/etc/gdb/gdbinit -> ~/.gdbinit -> ./.gdbinit

```bash
linux:~ $ gdb [-n] [-x <gdbinit>] [<file>]
# -n: not execute .gdbinit
# -x: execute <gdbinit>
```

```bash
# .gdbinit
layout split
# layout src
# layout asm
set disassembly-flavor intel
set print pretty
```

---

## script

```bash
linux:~ $ gdb -n <file> << EOF
list 1
break main
info breakpoints
run
frame
info locals
quit
EOF
```

---

## tui

```makefile
CC =
ifndef CC
  CC = gcc
endif

ifndef CFLAGS
  ifeq ($(TARGET), debug)
    CFLAGS=-Wall -Wextra -g -std=c99
  else
    CFLAGS=-Wall -O2 -std=c99
  endif
endif


hello: hello.o
   ${CC} ${CFLAGS} -o hello $?

%.o: %.c
   ${CC} ${CFLAGS} -c $<

.PHONY: clean
clean:
   -@test -f hello && rm -fv hello || true
   -@rm -fv *.o 2> /dev/null || true
```

```c
#include <stdio.h>

#define MAX	5

int main() {
  printf("hello\n");

  int x = 0, sum = 0;
  for (int i = 0; i < MAX; i++) {
    x = x * sum;
    sum += i;
  }
  printf("sum %i\n", sum);

  return 0;
}
```

```bash
linux:~/demo $ tree
.
├── hello.c
└── Makefile

0 directories, 2 files

linux:~/demo $ make TARGET=debug
linux:~/demo $ gdb -tui hello
(gdb) layout split
# ctrl-x a: enter or leave the tui mode
# ctrl-x 1: use a tui layout with only one window
# ctrl-x 2: use a tui layout at least two windows
# ctrl-x o: change the active window
# ctrl-l  : refresh screen
(gdb) layout asm
(gdb) layout src
(gdb) list
(gdb) break main
(gdb) info break
(gdb) run
(gdb) frame
(gdb) info locals
(gdb) quit
```

[TUI Key Bindings](https://sourceware.org/gdb/onlinedocs/gdb/TUI-Keys.html)

---

## remote

```bash
# client
client:~ $ scp server:~/<file>

# server
server:~ # apt install gdbserver
server:~ $ gdbserver :1234 <file>

# client
client:~ $ gdb <file>
(gdb) target remote <server>:1234
...
```
