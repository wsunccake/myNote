# nasm

## package

```bash
debian:~ # apt-get install nasm
```

---

## section

```assembly
section .data
    ...

section .bss
    ...

section .text
    ...
```

```assembly
; hello.asm
section	.text
   global _start

_start:
   mov	edx,len             ;message length
   mov	ecx,msg             ;message to write
   mov	ebx,1               ;file descriptor (stdout)
   mov	eax,4               ;system call number (sys_write)
   int	0x80                ;call kernel

   mov	eax,1               ;system call number (sys_exit)
   int	0x80                ;call kernel

section	.data
msg db 'Hello, world!', 0xa ;string to be printed
len equ $ - msg             ;length of the string
```

```bash
# for 32 bit
debian:~ $ nasm -f elf -o hello.o hello.asm
debian:~ $ ld -m elf_i386 -s -o hello hello.o
debian:~ $ ./hello

# for 64 bit
debian:~ $ nasm -f elf64 -o hello.o hello.asm
debian:~ $ ld -m elf_x86_64 -s -o hello hello.o
debian:~ $ ./hello

debian:~ $ file hello.o         # ELF 64-bit LSB relocatable
debian:~ $ file hello           # ELF 64-bit LSB executable
debian:~ $ objdump -D hello.o   # disassembly
```

---

## cpu

address bus

data bus

control bus

```
cpu
    RAM
    ROM (BIOS)

    MEM     RAM
    VGA     RAM
            ROM (BIOS)
    NIC     ROM (BIOS)
```

---

## register

```
            data register
32-bit                              16-bit
 |        31     16 15   8 7     0   |
 v       +---------+------+------+   v
EAX      |         |  AH  |  AL  |  AX  Accumulator
EBX                   BH     BL     BX  Base
ECX                   CH     CL     CX  Count
EDX                   DH     DL     DX  Data
```

```
            pointer register
32-bit                        16-bit
 |        31     16 15      0   |
 v       +---------+--------+   v
ESP      |         |  SP    |  Stack Pointer
EBP                   BP       Base Pointer
```

```
            index register
32-bit                        16-bit
 |        31     16 15      0   |
 v       +---------+--------+   v
ESI      |         |  SI    |  Source Index
EDI                   DI       Destination Index
```

```
control register
Overflow Flag (OF)
Direction Flag (DF)
Interrupt Flag (IF)
Trap Flag (TF)
Sign Flag (SF)
Zero Flag (ZF)
Auxiliary Carry Flag (AF)
Parity Flag (PF)
Carry Flag (CF)
```

---

## word

---

---

## address

physical address = segment address + offset address

effective address

---

## segment

code segment (CS)

data segment(DS)

extra segment (ES)

stack segment(SS)

```asm
; syntax
mov  <register>, [<memory address>]

<register>: register
[memory address]: offset address


mov  ax, 1      ; (v)
mov  ds, 1000H  ; (x)

mov  bx, 1000H  ; 1000H segment address
mov  ds, bx     ;
mov  [0]; al    ; [0] offset address
```

---

## ref

[NASM Tutorial](https://cs.lmu.edu/~ray/notes/nasmtutorial/)

[Assembly Programming Tutorial](https://www.tutorialspoint.com/assembly_programming/index.htm)
