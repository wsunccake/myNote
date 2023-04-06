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

## hello world

### system call - 64 bit

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

### system call - 32 bit

```asm
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

```makefile
# Makefile
ASM_FLAG = -f elf32
LD_FLAG = -m elf_i386 -s

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

## jump

```asm
; if (rax == 0) {
;     printf("rax == 0");
; } else {
;     printf("rax != 0");
; }

section .data
    msg1 db "rax == 0", 10
    len1 equ $-msg1

    msg2 db "rax != 0", 10
    len2 equ $-msg2

section .text
    global _start

    _start:
        cmp rax, 1

        jz thenblock            ; ZF=0
        mov rdx, len2
        mov rsi, dword msg2

        jmp endif

    thenblock:
        mov rdx, len1
        mov rsi, dword msg1

    endif:
        mov rax, 0x1
        mov rdi, 0x1
        syscall

        mov rax, 0x3c
        xor rdi, rdi
        syscall
```

```asm
; if (rax >= 0) {
;     printf("rax >= 0");
; } else {
;     printf("rax < 0");
; }

section .data
    msg1 db "rax >= 0", 10
    len1 equ $-msg1

    msg2 db "rax < 0", 10
    len2 equ $-msg2

section .text
    global _start

    _start:
        cmp rax, 0

        js singon       ; SF=1
        jo elseblock    ; SF=0, OF=1 => RAX<5
        jmp thenblock   ; SF=0, OF=0 => RAX>= 5


    singon:
        jo thenblock    ; SF=0, OF=0 => RAX>=0

    elseblock:
        mov rdx, len2
        mov rsi, dword msg2
        jmp endif

    thenblock:
        mov rdx, len1
        mov rsi, dword msg1

    endif:
        mov rax, 0x1
        mov rdi, 0x1
        syscall

        mov rax, 0x3c
        xor rdi, rdi
        syscall
```

```asm
; if / else
; if( condition )
;    then_block;
; else
;    else_block;

        cmp  xx, xx
        jxx     else_block  ; false condition
        ;; true condition statement
        jmp     end_if

    else_block:
        ;; true condition statement

    end_if:
```

```asm
; while loops
; while( condition ) {
;    statement;
; }

    while:
        cmp  xx, xx
        jxx end_while   ; false condition
        ...             ; loop statement
        jmp while
    end_while:
```

```asm
; do while loops
; do {
;   statement
; } while( condition );

    do:
        cmp xx, xx
        jxx do ; true condition
```
