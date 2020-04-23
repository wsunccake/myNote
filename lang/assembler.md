# assembler


## hello

```
.text

    .global _start

_start:

        # write our string to stdout.

        movl    $len,%edx       # third argument: message length.
        movl    $msg,%ecx       # second argument: pointer to message to write.
        movl    $1,%ebx         # first argument: file handle (stdout).
        movl    $4,%eax         # system call number (sys_write).
        int     $0x80           # call kernel.

        # and exit.

        movl    $0,%ebx         # first argument: exit code.
        movl    $1,%eax         # system call number (sys_exit).
        int     $0x80           # call kernel.

.data

msg:
        .ascii  "Hello, world!\n"      # the string to print.
        len = . - msg                  # length of the string.
```

```bash
linux:~ # as -o hello.o hello.S
linux:~ # ld -s -o hello hello.o
linux:~ # ./hello
```
