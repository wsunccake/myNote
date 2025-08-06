# masm - MS-DOS 16 bit

OS: MS-DOS 6.2x - 16 bit
Compiler: Microsoft Macro Assembler / masm

## run

### masm & link

```asm
; 1.asm
assume cs:codesg

codesg segment

        mov ax, 0123h
        mov bx, 0456h
        add ax, bx
        add ax, ax

        mov ax, 4c00h
        int 21h

codesg ends
end
```

```bat
C:\> masm 1.asm
C:\> link 1.obj
C:\> 1.exe
```

### ml

使用 ML.EXE 組譯時，數字系統可以用十進位、二進位、八進位和十六進位，預設是十進位。如果某個數值要使用其他進位系統，必須在數值後面標示，二進位標示「b」、八進位標示「o」、十六進位標示「h」，十進位標示「d」，這些 b、o、h、d 也可以用大寫。「100h」就表示十六進位的 100，換算成十進位就是 256D。

```asm
; a.asm
.MODEL  TINY          ; 記憶體模型為 TINY

.CODE
ORG     100H          ; 程式碼的起始位址設定為 100H

start:                ; Label, 標記程式的執行起始點
        mov ah, 2     ; 執行 DOS 的 "顯示字元到標準輸出" 功能。
        mov dl, 41H   ; 顯示的字元必須放在 DL 寄存器
        int 21H       ; 檢查 AH 寄存器的值，然後將 DL 寄存器中的字元顯示到螢幕上。

        int 20H       ; 程式終止
END start             ; 程式碼的結束
```

```bat
C:\> MASM611\BINR\NEW-VARS.BAT
C:\> ml a.asm
C:\> a.com
```

### debug

```bat
C:\> debug a.com
-u
-r
-t
-p
```

---

## ascii

```asm
; ascii.asm
.MODEL  TINY

.CODE
ORG     100H

start:
        mov ah, 2H      ; AH=2H 表示 "顯示字元到標準輸出 (stdout)"。
        mov dl, 0H      ; DL 暫存器用於存放要顯示的 ASCII 字元。
target:
        int 21H         ; AH 被設定為 2H，且 DL 包含要顯示字元，所以這指令會將 DL 字元列印到螢幕上。
        inc dl          ; 將 DL 暫存器的值加 1。
        jmp target      ; jmp 是無條件跳轉指令。使程式無條件地跳轉回 target

        int 20H
END start
```

```asm
; ascii2.asm
.MODEL  TINY

.CODE
ORG     100H

start:
        mov cx, 100H    ; CX 是 計數暫存器 (Count Register)
        mov ah, 2H
        mov dl, 0H
target:
        int 21H
        inc dl
        loop target     ; loop 是迴圈控制指令。
                        ; CX 不為零，則跳轉到 target
                        ; CX 為零，會繼續執行
        ; CX 最初被設定為 100H (256)
        ; 當執行迴圈時
        ; 1. DL 暫存器的 ASCII 字元到螢幕上。
        ; 2. DL 暫存器的值加 1，準備列印下一個 ASCII 字元。
        ; 3. CX 暫存器減 1，並檢查它是否為零。

        int 20H
END start
```

```asm
; hello.asm
.MODEL    TINY

.CODE
ORG       100H

start:
          mov dx, OFFSET message
          mov ah, 9h
          int 21h

          int 20h

message DB 'hello$'
END start
```

---

## pseudo-instructions

pseudo-instructions (偽指令) 或稱為 directive (指示詞)，是給組合器 (assembler) 的命令，它們本身不會被翻譯成 CPU 直接執行的機器碼，而是用來引導組合過程、定義資料、組織記憶體以及控制程式流程。

1.  Program Structure Directives / 程式結構指令

    這些指令定義了組合語言程式的整體結構和記憶體模型。

- `.MODEL memory_model`：定義程式的記憶體模型。這會影響 MASM 如何處理記憶體區段 (segments) 和位址。

  - **TINY** (微小)：所有程式碼、資料和堆疊都在一個 64KB 的區段中（用於 .COM 程式）。`CS=DS=SS=ES` (程式碼段、資料段、堆疊段、附加段暫存器都指向同一個位址)。
  - **SMALL** (小)：獨立的程式碼段和資料段，兩者都小於等於 64KB。`CS!=DS` (程式碼段和資料段指向不同位址)。
  - **MEDIUM** (中)：多個程式碼段，單一資料段。
  - **COMPACT** (緊湊)：單一程式碼段，多個資料段。
  - **LARGE** (大)：多個程式碼段，多個資料段。
  - **HUGE** (巨大)：類似於 `LARGE`，但允許陣列大小超過 64KB。
  - **FLAT** (平坦)：用於 32 位元保護模式（不常用於 16 位元 DOS）。

- `.STACK size`：定義堆疊區段的大小。這用於除了 TINY 以外的記憶體模型。

  - 範例：`.STACK 200h` (分配 512 位元組作為堆疊)。

- `.DATA`：標記已初始化資料區段的開始。在這裡定義的變數，其初始值會儲存在執行檔中。

- `.DATA?` 或 `.BSS`：標記未初始化資料區段的開始。在這裡定義的變數只會保留空間，但不會在執行檔中初始化（通常在程式載入時會被載入器清零）。

- `.CODE`：標記程式碼區段的開始，你的指令都在這裡。

- `SEGMENT ... ENDS`：定義區段的傳統方式。`.CODE`、`.DATA` 等是這種方式的簡化巨集。

  - 範例：

  ```asm
  MY_SEG SEGMENT PARA PUBLIC 'CODE'
    ; ... 程式碼在此
  MY_SEG ENDS
  ```

- `ASSUME seg_reg:segment_name[, ...]`：告訴組合器哪個區段暫存器 (CS, DS, SS, ES) 指向哪個區段。這有助於組合器解析位址並選擇適當的指令編碼。

  - 範例：`ASSUME CS:CODE_SEG, DS:DATA_SEG, SS:STACK_SEG`

- `END [start_label]`：標記整個原始程式的結束。可選的 `start_label` 指定程式執行應從何處開始。

  - 範例：`END start`

2. Data Definition Directives / 資料定義指令

   這些指令用於分配記憶體並在資料區段中初始化資料。

- `DB` (**Define Byte**, 定義位元組)：保留一個或多個位元組的記憶體空間，並可選地進行初始化。

  - 範例：`my_byte DB 10` ; 定義一個值為 10 的位元組
  - 範例：`my_string DB 'Hello', 0` ; 定義一個以空字元結尾的字串

- `DW` (**Define Word**, 定義字)：保留一個或多個字 (2 位元組) 的記憶體空間，並可選地進行初始化。

  - 範例：`my_word DW 1234h` ; 定義一個值為 1234h 的字
  - 範例：`my_array DW 10 DUP(0)` ; 定義一個包含 10 個字的陣列，所有字都初始化為 0

- `DD` (**Define Double Word**, 定義雙字)：保留一個或多個雙字 (4 位元組) 的記憶體空間，並可選地進行初始化。

  - 範例：`my_dword DD 12345678h`

- `DQ` (**Define Quad Word**, 定義四字)：保留一個或多個四字 (8 位元組) 的記憶體空間。

  - 範例：`my_qword DQ 123456789ABCDEF0h`

- `DT` (**Define Ten Bytes**, 定義十位元組)：保留 10 個位元組的記憶體空間（用於 BCD 或擴展浮點數）。

- `?` (**Uninitialized**, 未初始化)：與 `DB`、`DW`、`DD` 等一起使用，用於保留空間而不初始化它。

  - 範例：`my_var DW ?`

- `DUP(...)`：用於保留並可選地初始化多個相同項目。

  - 範例：`buffer DB 100 DUP(?)` ; 保留 100 個未初始化位元組。
  - 範例：`zero_words DW 50 DUP(0)` ; 保留 50 個字，都初始化為 0。

- `EQU` (**Equate**, 等同)：為常數值或表達式賦予一個符號名稱。組合器會在符號被使用的任何地方替換為其值。`EQU` 定義的符號不能被重新定義。

  - 範例：`CR EQU 0DH` ; 定義 `CR` 為換行符的 ASCII 碼。
  - 範例：`BUFFER_SIZE EQU 256`

- `=` (**Equal Sign**, 等號)：類似於 `EQU`，但可以在程式碼後面重新定義。

  - 範例：`counter = 1`
  - 範例：`counter = counter + 1`

3. Procedure and Macro Directives / 程序與巨集指令

   這些指令有助於定義程序 (函式) 和巨集。

- `PROC ... ENDP`：定義一個程序。可以指定屬性，如 `NEAR` (近), `FAR` (遠), `PUBLIC` (公開), `PRIVATE` (私有)。

  - 範例：

  ```asm
  MyProc PROC NEAR
    ; ... 程序碼
    RET
  MyProc ENDP
  ```

- `LOCAL`：在 `PROC` 內部使用，用於宣告堆疊幀上的局部變數。（在 MASM 6.x 及更高版本中更常見，但適用於 16 位元程式設計）。

- `MACRO ... ENDM`：定義一個巨集，它是一段程式碼區塊，組合器會在每次調用時將其內聯展開。

  - 範例：

  ```asm
  PRINT_MSG MACRO msg
    mov ah, 9
    lea dx, msg
    int 21h
  ENDM
  ```

- `IRP` / `IRPC` / `REPT`：巨集的疊代指令，允許程式碼重複。

4. Listing and Control Directives / 列表與控制指令

   這些指令影響組合器如何處理原始碼並生成列表文件。

- `ORG address`：設定定位計數器（原點）到一個特定的位址。對於 `.COM` 文件至關重要，它們總是從 `100H` 開始。

  - 範例：`ORG 100H`

- `ASSUME`： (已在「程式結構指令」中解釋，但它也影響組合器如何生成程式碼)。

- `INCLUDE filename`：在組合時將另一個原始碼文件的內容包含到當前文件中。

  - 範例：`INCLUDE 'DOSMACRO.INC'`

- `%OUT string`：在組合過程中顯示一條訊息。對於組合器邏輯的除錯很有用。

- `IF ... ENDIF` / `IFDEF ... ENDIF` / `IFNDEF ... ENDIF`：條件組合指令。允許只有在滿足特定條件（例如，某個符號被定義）時才組合程式碼的某些部分。

- `PUBLIC symbol[, ...]`：使符號對其他模組可見（用於連結）。

- `EXTRN symbol:type[, ...]`：聲明一個在其他模組中定義的符號。

- `.LIST` / `.NOLIST`：控制生成的列表文件是否包含原始碼和目標程式碼。

- `.CREF` / `.NOCREF`：控制列表文件中的交叉參考資訊。

- `NAME program_name`：為模組指定一個名稱。

**16 位元 MASM 在 DOS 環境下的重要注意事項**

- 實模式重點：這些指令主要用於 MS-DOS 下的 16 位元實模式程式設計。在此模式下，記憶體區段化是一個核心概念。

- `.COM` vs. `.EXE`：

  - `.COM` 文件是簡單的單區段程式（最大 64KB），通常使用 `.MODEL TINY` 和 `ORG 100H` 來創建。
  - `.EXE` 文件更複雜，可以有多個區段，並且需要連結器來生成最終的執行檔。

- 版本依賴性：雖然核心指令保持一致，但較新的 MASM 版本（如 MASM 6.x）引入了更高級的功能（例如，帶有堆疊幀生成的簡化程序定義 `PROC`，用於高階呼叫的 `INVOKE` 等），這些功能可能在非常舊的 MASM 版本中不完全可用或功能不同。

## loop

```asm
; loop1.asm
.MODEL    TINY

.CODE
ORG       100H

start:
      mov ax, 2000H   ; 將十六進位值 2000H 載入到 AX 暫存器。
                      ; 因為段暫存器不能直接載入立即數。
      mov ds, ax      ; 將 AX 暫存器中的值 (2000H) 載入到 DS (資料段) 暫存器。
                      ; 現在，所有預設的資料記憶體存取都將以 DS * 16 的物理位址為基底。
                      ; 也就是說，數據將從物理位址 2000H * 16 = 20000H 開始存取。
      mov bx, 1000H   ; 將 1000H 載入到 BX 暫存器。
                      ; BX 暫存器在 x86 中常用作基底暫存器 (base register)，
                      ; 用來儲存記憶體偏移量。
      mov ax, [bx]
      inc bx
      inc bx
      mov [bx], ax
      inc bx
      inc bx
      mov [bx], ax
      inc bx
      mov [bx], al
      inc bx
      mov [bx], al

      mov ax, 4C00H   ; 程式終止的標準步驟：
                      ; AH (AX 的高位元組) 為 4CH，「終止程式並返回 DOS」的功能號碼。
                      ; AL (AX 的低位元組) 為 00H，程式退出碼 (exit code)，0 表示程式正常結束。
      int 21H         ; 軟體中斷 (Software Interrupt) 指令，用於呼叫 DOS 系統服務。

END start
```

```bat
C:\> ml loop1.asm
C:\> debug loop1.com
-r
-u
-t
-t
-t
-d 2000:1000
-q
```

```asm
; loop2.asm
; m ^ n+1 => 2^11
.MODEL  TINY

.CODE
ORG     100H

start:
    mov cx, 10      ; 設定迴圈計數器為 10
    mov ax, 2       ; 設定 AX 初始值為 2

target:
    add ax, ax      ; 將 AX 的值乘以 2 (迴圈會執行 10 次)
                    ; 迴圈結束後，AX = 2 * (2^10) = 2^11 = 2048
    loop target     ; CX 減 1，若不為零則跳轉回 target

    mov ah, 4CH     ; DOS 服務: 終止程式
    int 21h         ; 呼叫 DOS
END start
```

ex:

將 ffff:0 ~ 12 複製到 0020:0 ~ 12

```asm
; move_seg1.asm
.MODEL  TINY

.CODE
ORG     100H

start:
        mov bx, 0
        mov cx, 12

s:
        mov ax, 0ffffh
        mov ds, ax
        mov dl, [bx]

        mov ax, 0020h
        mov ds, ax
        mov [bx], dl

        inc bx
        loop s

        mov ax, 4c00h
        int 21h

END start
```

```bat
C:\> ml move_seg1.asm
C:\> debug move_seg1.com
-d ffff:0 l12
-d 0020:0 l12
-g
-d ffff:0 l12
-d 0020:0 l12
-q
```

```asm
; move_seg2.asm
.MODEL  TINY

.CODE
ORG     100H

start:
        mov ax, 0ffffh
        mov ds, ax
        mov ax, 0020h
        mov es, ax
                      ; ds:bx -> ffff:0
                      ; es:bx -> 0020:0
        mov bx, 0
        mov cx, 12
s:
        mov dl, [bx]
        mov es:[bx], dl

        inc bx
        loop s

        mov ax, 4c00h
        int 21h

END start
```

```asm
; move_seg3.asm
.MODEL  TINY

.CODE
ORG     100H

start:
        mov ax, 0ffffh
        mov ds, ax
        mov ax, 0020h
        mov es, ax

        mov si, 0   ; si (來源位移)
        mov di, 0   ; di (目的位移)
        mov cx, 12  ; cx (計數器)

        cld         ; 清除方向旗標，讓字串操作從低位址往高位址移動
        rep movsb   ; 重複執行 movsb 指令，直到 cx 變為 0

        mov ax, 4c00h
        int 21h

END start
```

ex:

0123h, 0456h, 0789h, 0abch, 0defh, 0fedh, 0cbah, 0987h

```asm
.MODEL  TINY

.DATA
        DW 0123h, 0456h, 0789h, 0abch, 0defh, 0fedh, 0cbah, 0987h
        ; 儲存在 cs:0 ~ F

.CODE
ORG     100H


start:
        mov bx, 0
        mov ax, 0
        mov cx, 8

s:
        add ax, cs:[bx]
        add bx, 2
        loop s

        mov ax, 4c00h
        int 21h

END start
```
