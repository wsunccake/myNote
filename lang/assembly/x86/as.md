# gnu assembler

## hello - at&t syntax

```s
.text

.global _start

_start:
        # write our string to stdout
        movl    $len,%edx       # third argument: message length.
        movl    $msg,%ecx       # second argument: pointer to message to write.
        movl    $1,%ebx         # first argument: file handle (stdout).
        movl    $4,%eax         # system call number (sys_write).
        int     $0x80           # call kernel.

        # exit
        movl    $0,%ebx         # first argument: exit code.
        movl    $1,%eax         # system call number (sys_exit).
        int     $0x80           # call kernel.

.data
        msg: .ascii  "Hello, world!\n"  # the string to print.
        len = . - msg                   # length of the string.
```

```bash
linux:~ # as -o hello.o hello.S
linux:~ # ld -s -o hello hello.o
linux:~ # ./hello
```

---

## hello - intel syntax

```s
; test.asm
section .data
    msg: db  "Hello World!", 10 ; '10' at end is line feed
    len: equ $-msg

section .text
    global _start

    _start:
        mov edx, len            ; length of string is 13 bytes
        mov ecx, dword msg      ; set rsi to pointer to string
        mov ebx, 0x1            ; file descriptor of 1
        mov eax, 0x4            ; sys_writer = 4
        int 0x80                ; make the system call

        mov eax, 1              ; sys_exit = 1
        xor ebx, ebx
        int 0x80
```

---

## generate asm from c

```bash
linux:~ # gcc -masm=att -S -o hello.s hello.c           # at&t syntax
linux:~ # gcc -masm=intel -S -o hello.s hello.c         # intel syntax
```

---

## ref

[GNU Assembler Examples](https://cs.lmu.edu/~ray/notes/gasexamples/)
