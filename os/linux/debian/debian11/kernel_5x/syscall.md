# syscall

```bash
debian:~ # apt install strace ltrace
```

## hello

```c
// hello.c
#include <stdio.h>
int main(void) {
    printf("hello, world!\n");
    return 0;
}
```

```bash
linux:~ $ gcc -o hello hello.c
linux:~ $./hello
linux:~ $ ltrace ./hello
linux:~ $ strace ./hello

# asm
linux:~ $ gcc -S [-masm=intel] -m64 hello.c
linux:~ $ cat hello.s

# 32-bit
# linux:~ $ as --32 -o hello.o hello.s
# linux:~ $ ld -melf_i386 -o hello hello.o

# 64-bit
linux:~ $ as --64 -o hello.o hello.s
linux:~ $ ld -melf_86_64 -o hello hello.o
```
