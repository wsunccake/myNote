# assembly

## syntax

一般來說，Assembly Language / 組合語言 寫法分兩大流派：

| 分類             | 特點                                                                         | 常見的工具                            |
| ---------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| **Intel Syntax** | 操作數順序是 `目的地, 來源`（destination, source），指令像 `mov ax, bx`。    | MASM、TASM、NASM（可以設）            |
| **AT&T Syntax**  | 操作數順序是 `來源, 目的地`（source, destination），指令像 `movw %bx, %ax`。 | GAS (GNU Assembler, 也就是 `.s` 檔案) |

---

## Intel Syntax （MASM、NASM, .asm）

```S
mov ax, 0x1234
mov ds, ax
mov bx, 0x7C00
mov es, bx
```

- 沒有 % 符號
- mov 目標, 來源
- 立即數寫法直接是 0x 開頭
- : 用來標示 label，例如 start:

---

## AT&T Syntax （GNU as/gas, .S）

```asm
movw $0x1234, %ax
movw %ax, %ds
movw $0x7C00, %bx
movw %bx, %es
```

- 暫存器前面有 %
- 立即數前面有 $
- movw 來源, 目的地
- 指令後面常有大小（b=byte, w=word, l=long，例如 movb, movw, movl）

---

## 常見組合語言格式

| 類型                     | 說明                             | 代表工具               |
| ------------------------ | -------------------------------- | ---------------------- |
| **Intel ASM (純 Intel)** | 最傳統 BIOS/OS loader 常用格式。 | MASM, TASM, NASM       |
| **GNU Assembly (GAS)**   | Linux Kernel、GCC 編譯器用。     | `as` (assembler)       |
| **NASM 格式**            | 類似 Intel，但更乾淨，不依賴 C。 | NASM 專用              |
| **FASM 格式**            | Flat Assembler，結構超簡單。     | FASM                   |
| **MASM**                 | 微軟 MASM，支援 Macro。          | Visual Studio 早期工具 |
| **TASM**                 | Borland Turbo Assembler。        | DOS 時代很流行         |

---

## 語法轉換

| Intel 風格   | AT&T 風格                      |
| ------------ | ------------------------------ |
| `mov ax, bx` | `movw %bx, %ax`                |
| `add ax, 1`  | `addw $1, %ax`                 |
| `jmp label`  | `jmp label` （跳躍類指令一樣） |
