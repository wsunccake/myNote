# nasm

## print string from char

```asm
; test.asm
section .text
    global _start

    _start:
        mov  rax, 0x0A41424344; '\nABCDE'
        push rax
        mov  rdx, 0x5     ; length of string is 5 bytes
        mov  rsi, rsp     ; Address of string is RSP because string is on the stack
        mov  rax, 0x1     ; syscall 1 is write
        mov  rdi, 0x1     ; stdout has a file descriptor of 1
        syscall           ; make the system call

        mov  rax, 0x3c    ; syscall 3c is exit
        xor  rdi, rdi     ; exit code 0
        syscall           ; make the system call
```

```makefile
# Makefile
ASM_FLAG = -f elf64
LD_FLAG = -m elf_x86_64 -s

.PHONY: run
run: test
	./test

.PHONY: clean
clean:
	-@rm *.o
	-@rm test
	@echo "clean workspace"

%.o : %.asm
	nasm ${ASM_FLAG} -o $@ $<

test: test.o
	ld ${LD_FLAG} -o test test.o
```

---

## print hello world

### sstem call

```asm
; test.asm

section .data
    msg db  "Hello World!", 10      ; '10' at end is line feed
    len equ $-msg

section .text
    global _start

    _start:
        mov  rdx, len               ; length of string is 13 bytes
        mov  rsi, dword msg         ; set rsi to pointer to string
        mov  rax, 0x1               ; syscall 1 is write
        mov  rdi, 0x1               ; stdout has a file descriptor of 1
        syscall                     ; make the system cal

        mov  rax, 0x3c    ; syscall 3c is exit
        xor  rdi, rdi     ; exit code 0
        syscall           ; make the system call
```

```makefile
# Makefile
ASM_FLAG = -f elf64
LD_FLAG = -m elf_x86_64 -s

.PHONY: run
run: test
	./test

.PHONY: clean
clean:
	-@rm *.o
	-@rm test
	@echo "clean workspace"

%.o : %.asm
	nasm ${ASM_FLAG} -o $@ $<

test: test.o
	ld ${LD_FLAG} -o test test.o
```

### c library

```asm
; test.asm
section .text
    default rel
    extern printf
    global main

    main:
        push rbp
        mov	rdi, fmt
        mov	rsi, message
        mov	rax, 0

        call printf wrt ..plt	; Call printf
        pop	rbp			        ; Pop stack

        mov	rax, 0	            ; Exit code 0
        ret		                ; Return

section .data

    message:  db "Hello, World", 10, 0
    fmt: db "%s", 10, 0
```

```makefile
# Makefile
CFLAG =

run: test
	./test

%.o : %.asm
	nasm ${ASM_FLAG} -o $@ $<

test: test.o
	gcc ${CFLAG} -o test test.o

clean:
	-@rm *.o
	-@rm test
	@echo "clean workspace"
```
