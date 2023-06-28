# toolchain

## concept

```text
build   host    target
x       x       x       native
x       x       y       cross
x       y       z       canadian
```

---

## prepare

```bash
# list all architecture
debian:~ # dpkg-architecture -L

# add architecture
debian:~ # dpkg --add-architecture armhf                                    # for armhf
debian:~ # dpkg --add-architecture armel                                    # for armel
debian:~ # dpkg --add-architecture arm64                                    # for arm64
debian:~ # dpkg --add-architecture amd64                                    # for amd64

debian:~ # dpkg --remove-architecture armhf
debian:~ # dpkg --print-architecture
debian:~ # dpkg --print-foreign-architectures

# add qemu-user
debian:~ # apt update
debian:~ # apt install qemu-system:armel qemu-user:armel qemu-user-static   # for armel
debian:~ # apt install qemu-system:armhf qemu-user:armhf qemu-user-static   # for armhf
debian:~ # apt install qemu-system:arm64 qemu-user:arm64 qemu-user-static   # for arm64
```

---

## package

```bash
# test
debian:~ # apt install crossbuild-essential-arm64   # for arm64
debian:~ # apt install crossbuild-essential-armel   # for armel
debian:~ # apt install crossbuild-essential-armhf   # for armhf
```

---

## c

```c
// hello.c
#include <stdio.h>

int main() {
  printf("hello\n");

  for (int i =0; i< 10; i++) {
	  x += 1 ;
	  printf("x: %d\n", x);
  }

  return 0;
}
```

```bash
# for armhf
debian:~ # arm-linux-gnueabihf-gcc -v
debian:~ # arm-linux-gnueabihf-gcc -o hello.armhf hello.c
debian:~ # file hello.armhf
debian:~ # hello.armhf

# for arm64
debian:~ # aarch64-linux-gnu-gcc -v
debian:~ # aarch64-linux-gnu-gcc -o hello.aarch64 hello.c
debian:~ # file hello.aarch64
debian:~ # hello.aarch64
```

---

## asm - armhf

```s
.global _start

_start:
    mov  r7, #4          @ Setup service call 4 (write)
    mov  r0, #1          @ param 1 - File descriptor 1 = stdout
    ldr  r1, =hello      @ param 2 - address of string to print
    mov  r2, #13         @ param 3 - length of hello world string
    svc  0               @ ask linux to write to stdout

    mov  r7, #1          @ Setup service call 1 (exit)
    mov  r0, #0          @ param 1 - 0 = normal exit
    svc  0               @ ask linux to terminate us

.data
hello:    .ascii    "Hello World!\n"
```

```bash
# two step
debian:~ # arm-linux-gnueabihf-as -o hello.o hello.s                      # as
debian:~ # arm-linux-gnueabihf-ld -o hello.armhf hello.o                  # ld

# one step
debian:~ # arm-linux-gnueabihf-gcc -nostartfiles -o hello.armhf hello.s   # gcc
```

---

## asm - aarch64

```s
.globl _start
_start:
    /* syscall write(int fd, const void *buf, size_t count) */
    mov     x0, #1      /* fd := STDOUT_FILENO */
    ldr     x1, =msg    /* buf := msg */
    ldr     x2, =len    /* count := len */
    mov     w8, #64     /* write is syscall #64 */
    svc     #0          /* invoke syscall */

    /* syscall exit(int status) */
    mov     x0, #0      /* status := 0 */
    mov     w8, #93     /* exit is syscall #93 */
    svc     #0          /* invoke syscall */

.data
msg:
    .ascii        "Hello, ARM64!\n"
len = . - msg
```

```bash
# two step
debian:~ # aarch64-linux-gnu-as -o hello.o hello.s                        # as
debian:~ # aarch64-linux-gnu-ld -o hello.aarch64 hello.o                  # ld

# one step
debian:~ # aarch64-linux-gnu-gcc -nostartfiles -o hello.aarch64 hello.s   # gcc
```

---

## gdb

```text
host                ---         target
x86_64                          arm / arm64
debian                          debian
192.168.10.1                    192.168.10.10
```

```bash
# prepare
host:~ # apt install gdb-multiarch
target:~ # apt install gdbserver

# application
## target side
target:~/test $ ls hello.c
target:~/test $ gcc -g -o hello hello.c
target:~/test $ file hello | grep debug_info
target:~/test $ gdbserver :1234 ./hello

## host side
host:~ $ scp -r 192.168.10.1:~/test .
host:~ $ cd test
host:~/test $ gdb-multiarch
(gdb) file hello

(gdb) layout split

(gdb) show architecture
(gdb) show sysroot
(gdb) show solib-search-path

(gdb) set architecture aarch64
(gdb) set sysroot ~/test
(gdb) set solib-search-path /usr/lib/aarch64-linux-gnu/

(gdb) target remote 192.168.10.10:1234

(gdb) hbreak
(gdb) info break
(gdb) break *0xfffff7fcd150

(gdb) contiune
(gdb) info all-registers
(gdb) info registers x1
(gdb) p/x $x1
(gdb) x/i $x1
(gdb) set $x1 =

(gdb) quit

## multi
target:~/test $ gdbserver --multi :1234

host:~/test $ gdb-multiarch
(gdb) target extended-remote 192.168.10.10:1234
(gdb) set remote exec-file ./a.out
(gdb) run
(gdb) monitor exit
```
