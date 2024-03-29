# gnu assembler

## example

```s
.global _start

_start:
    mov x0, #42     @ return value
    mov x8, #93     @ sys call exit
    svc #0
```

```makefile
TEST = test
CC   = aarch64-linux-gnu-gcc
GDB  = gdb-multiarch
DEBUG= qemu-aarch64-static
DEBUG_PORT = 1234

${TEST}.exe : ${TEST}.s
    @echo "compile..."
    ${CC} -g -nostartfiles -o ${TEST}.exe ${TEST}.s

.PHONY: run
run: ${TEST}.exe
    @echo "run..."
    ./${TEST}.exe

.PHONY: debug
debug: ${TEST}.exe
    @echo "debug..."
    ${DEBUG} -g ${DEBUG_PORT} ${TEST}.exe

.PHONY: clean
clean:
    @echo "clean..."
    -rm ${TEST}.exe

.PHONY: gdb
gdb:
    @echo "gdb..."
    ${GDB} -ex "layout src" \
  -ex "target remote :${DEBUG_PORT}" \
  -ex "set disassembly-flavor intel" \
  -ex "set print pretty"
```

```bash
# build 1
arm64:~ $ as -o test.o test.s
arm64:~ $ ld -o test test.o

# build 2
arm64:~ $ gcc -g -nostartfiles -o test test.s

# build 3
arm64:~ $ make

# run
arm64:~ $ ./test
arm64:~ $ echo $?
```

---

## hello world

```s
.global _start              // address to linker

_start:
// print message
    mov     X0, #1          // 1 = stdout
    ldr     X1, =msg        // string to print
    mov     X2, len         // length of string
    mov     X8, #64         // linux write system call
    svc     0               // call linux to output the string

// exit
    mov     X0, #0          // return 0
    mov     X8, #93         // 93 terminates this program
    svc     0               // call linux to terminate the program

.data
msg:      .ascii  "Hello World!\n"
len=      . - msg
```

X: 64 bit register

W: 32 bit register

---

## mov (wide immediate)

```s
.global _start

// load X2 with 0x1234FEDC4F5D6E3A first using MOV and MOVK
_start:
// dec number: #8
// hex number: #0x8
// mov: move 16-bit immediate to register
// movk: move 16-bit immediate into register, keeping other bits unchanged
    MOV     X2, #0x6E3A
    MOVK    X2, #0x4F5D, LSL #16
    MOVK    X2, #0xFEDC, LSL #32
    MOVK    X2, #0x1234, LSL #48

// move W2 into W1
    MOV     W1, W2

// all shift versions of MOV
    MOV     X1, X2, LSL #1      // logical shift left
    MOV     X1, X2, LSR #1      // logical shift right
    MOV     X1, X2, ASR #1      // arithmetic shift right
    MOV     X1, X2, ROR #1      // rotate right

// repeat the above shifts using the assembler mnemonics
    LSL     X1, X2, #1          // logical shift left
    LSR     X1, X2, #1          // logical shift right
    ASR     X1, X2, #1          // arithmetic shift right
    ROR     X1, X2, #1          // rotate right

// works with 8 bit immediate and shift
    MOV     X1, #0xAB000000     // too big for #imm16

// example of MVN
// move inverse of shifted 16-bit immediate to register.
    MOVN    W1, #45

// change to MVN
    MOV     W1, #0xFFFFFFFE     // (-2)

// exit
    MOV     X0, #0
    MOV     X8, #93
    SVC     0
```

---

## ldr

```s
.global _start

_start:
//    MOV X0, #12       // X0 = 12
//    LDR X0, =12       // X0 = 12

// ldr: loads a word or doubleword from memory and writes it to a register
    LDR X1, num         // X1 = num = 12
    LDR X0, [X1]        // X0 = X1

// add: adds a register value
    ADD X0, X0, 2       // X0 = X0 + 2
    MOV X8, #93
    SVC #0

.data
    num: .word  12
```

```text
.byte: 1 byte
.hword: 2 byte
.word: 4 byte
.quad: 8 byte
```

---

## condition

```s
// print a register in hex to stdout.
//
// X0-X2 - parameters to linux function services
// X1 - is also address of byte we are writing
// X4 - register to print
// W5 - loop index
// W6 - current character
// X8 - linux function number
//

.global _start

_start:
    MOV     X4, #0x6E3A
    MOVK    X4, #0x4F5D, LSL #16
    MOVK    X4, #0xFEDC, LSL #32
    MOVK    X4, #0x1234, LSL #48

    LDR     X1, =hexstr     // start of string
    ADD     X1, X1, #17     // start at least sig digit
// loop: FOR W5 = 16 TO 1 STEP -1
    MOV     W5, #16         // 16 digits to print
loop:   AND W6, W4, #0xf    // mask of least sig digit
// if: W6 >= 10 then goto letter
    CMP W6, #10             // is 0-9 or A-F
    B.GE    letter
// else: its a number so convert to an ASCII digit
    ADD W6, W6, #'0'
    B   cont                // goto to end if
letter:                     // handle the digits A to F
    ADD W6, W6, #('A'-10)
cont:   // end if
    STRB    W6, [X1]        // store ascii digit
    SUB X1, X1, #1          // decrement address for next digit
    LSR X4, X4, #4          // shift off the digit we just processed

// next W5
    SUBS        W5, W5, #1  // step W5 by -1
    B.NE        loop        // another for loop if not done

// print our hex number and call Linux to do it
    MOV     X0, #1          // 1 = StdOut
    LDR     X1, =hexstr     // string to print
    MOV     X2, #19         // length of our string
    MOV     X8, #64         // linux write system call
    SVC     0               // call linux to output the string

    MOV     X0, #0
    MOV     X8, #93
    SVC     0

.data
hexstr:      .ascii  "0x123456789ABCDEFG\n"
```
