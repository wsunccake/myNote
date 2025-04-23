# nasm

組合語言通常長這樣

```asm
[label:] mnemonic [operand1, operand2] [; comment]

start:   mov ax, 0x1234   ; 把 0x1234 存進 AX register
```

## mnemonic / 指令

```
mnemonic | function                 | example
mov      | 資料傳送                 | mov ax, bx
add      | 加法                     | add ax, 1
sub      | 減法                     | sub bx, ax
inc      | +1                       | inc cx
dec      | -1                       | dec cx
cmp      | 比較（會設旗標）         | cmp ax, bx
jmp      | 無條件跳躍               | jmp start
je       | 相等則跳（zero flag）    | je label
jne      | 不等則跳                 | jne label
call     | 呼叫副程式               | call print_hello
ret      | 回傳（從 call 回來）     | ret
push     | 壓入堆疊                 | push ax
pop      | 彈出堆疊                 | pop bx
int      | 軟體中斷（呼叫 BIOS/OS） | int 0x10（顯示字元）
```

---

## register / 暫存器

```
type       | name（16-bit） | 說明
通用       | AX, BX, CX, DX | 可拿來存數值、做運算等
指標類     | SI, DI         | 來源與目的索引
位址類     | BP, SP         | Base Pointer、Stack Pointer
控制類     | IP             | Instruction Pointer（程式計數器）
段暫存器   | CS, DS, SS, ES | code/data/stack 段選擇子
標誌暫存器 | FLAGS          | 儲存邏輯比較的結果等旗標狀態
```

### General Purpose Register / 通用暫存器

```
Register | 功能與說明            | 可細分為（8-bit）
AX       | 累加器（Accumulator） | AH（高）、AL（低）
BX       | 基底暫存器（Base）    | BH、BL
CX       | 計數器（Counter）     | CH、CL
DX       | 資料暫存器（Data）    | DH、DL
```

這些暫存器可拿來存變數、做算術、指向位址、控制迴圈等等都可以，超靈活。

```asm
; AL 和 AH 是 AX 的低/高 8-bit
; AX = 0x1234，那 AH = 0x12, AL = 0x34
mov ax, 0x1234   ; AX = 1234h
mov al, 0x56     ; AL = 56h → AX = 1256h
```

### Segment Register / 段暫存器

```
Register | Name          | 用途
CS       | Code Segment  | 儲存程式碼所在段的 segment base（不能用 mov 設定）
DS       | Data Segment  | 預設存取資料的段，例如變數、常數等
SS       | Stack Segment | 堆疊區的段 base（和 SP 結合使用）
ES       | Extra Segment | 額外資料段，常在某些字串指令中用到（如 movs, stos）
```

這些暫存器用來定義 segment base，Real Mode 下的實體位址 = segment × 16 + offset

```
類別               | 名稱範例        | 位數        | 功能與用途                                | 能否直接運算 | 主要用在哪裡
段暫存器 (Segment) | CS, DS, SS, ES… | 16         | 指定記憶體「段基底位址」，用來計算實體地址 | ❌ 不行      | 存取程式、資料、堆疊記憶體
通用暫存器 (GPR)   | AX, BX, CX, DX… | 8/16/32/64 | 做計算、搬資料、暫存值                     | ✅ 可以      | 數學、迴圈、資料處理等
```

---

## 語法

1. 資料宣告

```asm
msg db 'Hello, world!', 0
num dw 1234
```

db（Define Byte）：定義一個 byte（8-bit）資料
dw（Define Word）：定義一個 word（16-bit）資料

2. 標籤 / Label

```asm
start:
```

代表這裡是個程式的跳躍點，可搭配 jmp、call 使用。

3. 跳躍與比較

```asm
cmp ax, bx     ; 比較 ax 和 bx
je equal       ; 如果相等，跳到 equal:
jne not_equal  ; 如果不相等，跳到 not_equal:
```

4. 呼叫副程式與回傳

```asm
call print_hello
...
print_hello:
    ; 印字程式
    ret
```

5. 堆疊操作

```asm
push ax      ; 將 ax 壓入堆疊
pop bx       ; 從堆疊彈出，存進 bx
```
