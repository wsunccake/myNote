# ld

ld 是 Linux 上的 linker（程式連結器），負責將編譯後的 object file（目標檔）與 library（函式庫）結合，生成可執行檔案或共享函式庫。它通常由 GNU Binutils 提供，完整名稱是 GNU ld。

## usage

1. 基本功能

- 將 .o 目標檔案合併，生成可執行檔或共享函式庫。
- 解析符號並解決相依性。
- 連結靜態 (.a) 或動態 (.so) 函式庫。
- 設定程式入口點（entry point）。
- 指定不同的記憶體區段，如 .text（程式碼）、.data（靜態變數）等。

2. 基本用法

ld 一般不直接使用，通常由編譯器（如 gcc 或 clang）呼叫，但也可以手動執行

```bash
linux:~ $ ld --version   # 查看版本
linux:~ $ ld --help      # 查看指令幫助

# 連結目標檔案
linux:~ $ ld -o my_program file1.o file2.o
# 將 file1.o 和 file2.o 連結成 my_program

# 指定函式庫
linux:~ $ ld -o my_program file.o -lc
# 連結 libc 標準 C 函式庫（相當於 gcc file.o -o my_program）。

# 指定起始點
linux:~ $ ld -o my_program file.o --entry=my_start
# 設定 my_start 為程式的入口點，而非預設的 main

# 產生共享函式庫
linux:~ $ ld -shared -o libmylib.so file.o
# 建立共享函式庫 libmylib.so
```

3. 進階用法

```ld
SECTIONS {
    .text 0x1000 : { *(.text) }
    .data 0x2000 : { *(.data) }
}
```

```bash
# 自訂 ld 指令檔（linker script）來控制記憶體區段
linux:~ $ ld -T myscript.ld -o my_program file.o

# 產生 output.map，顯示記憶體配置
linux:~ $ ld -o my_program file.o -Map=output.map
```

4. 與 gcc 的關係

```bash
# 通常，開發者不直接使用 ld，而是透過 gcc：
linux:~ $ gcc -o my_program file.c
# GCC 會自動：
# 1. 編譯 file.c 成 file.o。
# 2. 呼叫 ld 來進行連結。

# 檢視 GCC 呼叫 ld
linux:~ $ gcc -v -o my_program file.c
```

5. 常見錯誤

5.1 undefined reference / 未定義符號

```bash
linux:~ $ ld -o my_program file1.o file2.o
undefined reference to 'some_function'

連結了必要的函式庫
linux:~ $ ld -o my_program file.o -lmylib
```

5.2 cannot find -lxxx / 找不到函式庫

```bash
linux:~ $ ld -o my_program file.o -L/path/to/lib -lmylib
ld: cannot find -lmylib

使用 -L 指定函式庫路徑
linux:~ $ ld -o my_program file.o -L/path/to/lib -lmylib

檢查 LD_LIBRARY_PATH 環境變數
linux:~ $ export LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH
```

6. 相關環境變數

- LIBRARY_PATH
  編譯階段（Compile-time），指定 gcc 或 g++ 在 連結（Linking） 階段搜尋靜態庫（.a）或共享庫（.so）的位置

- LD_LIBRARY_PATH
  執行階段（Runtime），指定 動態連結器（dynamic linker）搜尋共享庫 (.so) 的位置

---

## history

在 Unix 系統發展的早期，loader（載入器） 和 linker（連結器） 曾經是密不可分的，但隨著技術發展，它們的職責逐漸分開，最終形成現代的 linker（連結器） 和 dynamic loader（動態載入器）。這段歷史涉及 Unix 的設計理念、硬體演進以及程式語言的發展。

1. Unix 早期（1960s - 1970s）：簡單的 Loader

在 Unix 系統的最早期，程式通常是靜態編譯的（statically compiled），也就是：

- 編譯（Compile）：程式碼轉換成機器碼（Object Code）。
- 連結（Linking）：透過簡單的 loader，將程式載入記憶體，解決符號（Symbol Resolution），然後執行。

早期 Unix 使用了一個簡單的 Loader（載入器），它的主要工作是：

- 將執行檔從磁碟載入到記憶體。
- 設定程式的起始位置（Entry Point）。
- 執行程式。

這時期的 Loader 主要負責載入，而 連結（Linking） 則通常發生在程式編譯階段，由 ld 負責將所有 .o 檔案和函式庫組合成一個完整的可執行檔案。
範例：
在早期 Unix（如 V6），執行 a.out 格式的可執行檔時，Loader 會將程式碼載入固定位置，然後執行。

2. 靜態 Linking（1970s - 1980s）：GCC 與 UNIX ld

到了 1970-80 年代，Unix 的 靜態連結（Static Linking） 概念變得更加明確：
ld（linker）開始獨立於 Loader，專門負責：

- 解析符號（Symbol Resolution）。
- 將多個 .o 檔案組合成單一可執行檔。
- 連結靜態函式庫（libXXX.a）。

這個時期的 Unix 仍然是以 靜態連結 為主，每個程式的執行檔包含所有必要的函式，這導致：

- 可執行檔案很大，每個程式都內含相同的函式（例如 printf()）。
- 更新函式庫困難，若 libc 更新，每個程式都必須重新編譯。

範例：

```bash
gcc -o myprog myprog.c
```

ld 會將 myprog.o 與靜態函式庫 libc.a 連結，生成 myprog 可執行檔。

3. 動態 Linking（1980s - 1990s）：Shared Libraries (.so)

到了 1980-90 年代，隨著 Unix 變得更加廣泛應用（特別是 BSD 和 System V），動態連結（Dynamic Linking） 概念被引入，以解決靜態連結的問題。

這時期的創新包括：

a. 共享函式庫（Shared Libraries, .so）

- 函式庫不再嵌入每個執行檔，而是獨立於程式，程式執行時才載入。
- 例如：libc.so 存在於系統中，所有程式共用它，減少可執行檔的大小。

2 .ld.so（Dynamic Loader）

a. 負責在程式執行時動態載入 .so 函式庫。
b. 允許程式執行時解析動態符號。

3. ELF 格式（Executable and Linkable Format，1995）

a. ELF 取代了 a.out 和 COFF 格式，使得動態載入更加高效。
b. ld.so 變得更加強大，支援 動態重定位（relocation） 和 延遲綁定（lazy binding）。

範例：
現代 Unix/Linux 透過 ldd 指令查看可執行檔的共享函式庫：

```bash
linux:~ $ ldd /bin/ls
linux-vdso.so.1 =>  (0x00007ffcc7c00000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7c1e000000)
/lib64/ld-linux-x86-64.so.2 (0x00007f7c1e400000)
```

4. 現代 Linking（2000s - 2020s）：動態載入、RTLD、dlopen()
   到了 2000 年代之後，Linker 和 Loader 已經完全分離，並且更加靈活：

a. ld（Linker）：

- 負責在編譯時連結。

b. ld.so（Dynamic Loader）：

- 負責程式執行時的函式庫載入。

c. dlopen() 機制：

- dlopen() 允許程式在運行時載入共享函式庫，而非在啟動時載入。
- 這使得 插件系統（Plugin System） 變得可能，例如 Web 瀏覽器的擴充功能。

範例：
這段程式碼會在運行時載入 libm.so.6（數學函式庫）

```c
#include <dlfcn.h>
void *handle = dlopen("libm.so.6", RTLD_LAZY);
```

5. 未來發展：更高效的 Linking

目前，Linker 和 Loader 仍然在進步，未來可能的發展方向包括：

- 全新的 Linking 方式：如 LLVM lld 提供更快的連結方式。
- 靜態與動態 Linking 混合：某些系統如 Go 語言 採用靜態連結，但仍然允許動態函式庫。
- WebAssembly（WASM）：取代傳統 Linking，允許跨平台執行。

6. 總結

Linker 和 Loader 的分離，讓 Unix/Linux 系統變得更加靈活，也促進了現代軟體開發的便利性。

| 時代          | 主要技術                        | 說明                                 |
| ------------- | ------------------------------- | ------------------------------------ |
| 1960s - 1970s | Loader (a.out)                  | 直接載入執行檔，無動態連結。         |
| 1970s - 1980s | 靜態 Linking (ld, libXXX.a)     | 可執行檔包含所有函式庫，浪費空間。   |
| 1980s - 1990s | 動態 Linking (.so, ld.so)       | 共享函式庫減少程式大小，執行時載入。 |
| 1990s - 2000s | ELF 格式、ldd、dlopen()         | 允許延遲載入、插件系統。             |
| 2000s - 2020s | 現代 Linking (lld, WebAssembly) | 更高效的連結方式。                   |

---

## ldd

ldd 是一個分析工具，用來檢查已編譯的可執行檔或共享函式庫，找出它們運行時所需的 .so 動態函式庫。

```bash
# 檢查可執行檔的函式庫
linux:~ $ ldd /bin/ls
    linux-vdso.so.1 =>  (0x00007fffab7fe000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4c8c000000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f4c8c800000)
# /bin/ls 依賴 libc.so.6（標準 C 函式庫）。
# ld-linux-x86-64.so.2 是動態載入器（dynamic linker），負責載入 ls 及其函式庫。

# 檢查共享函式庫
linux~: $ ldd /lib/x86_64-linux-gnu/libm.so.6
# 如果這是一個完整的 .so 檔案，它會顯示它的依賴關係。

# 檢查未解析的函式庫
    libxyz.so => not found
# 如果某個函式庫遺失，ldd 會顯示 not found
```

---

## 設定函式庫路徑

1. ld.so.conf

動態連結器 (ld.so) 預設會從 /lib 和 /usr/lib 這些系統路徑中搜尋共享函式庫（.so 檔案）。如果你想讓 ld 搜尋其他路徑，可以修改 /etc/ld.so.conf 或新增自訂的 .conf 檔案。

```bash
# 檢查現有設定
linux:~ # cat /etc/ld.so.conf

# 加入新的函式庫路徑，比如 /usr/local/lib/my_lib，可以手動編輯
linux:~ # vi /etc/ld.so.conf
/usr/local/lib/my_lib

# 儲存後執行
linux:~ # ldconfig

# 查看目前快取的函式庫
linux:~ # ldconfig -p
```

2. /etc/ld.so.conf.d/

```bash
# 新增一個 .conf 檔案
linux:~ # vi /etc/ld.so.conf.d/my_lib.conf
/usr/local/lib/my_lib

# 儲存後執行
linux:~ # ldconfig

# 查看目前快取的函式庫
linux:~ # ldconfig -p
```

3. LD_LIBRARY_PATH

```bash
# 設定環境變數
linux:~ $ export LD_LIBRARY_PATH=/usr/local/lib/my_lib:$LD_LIBRARY_PATH

# 檢查是否生效
linux:~ $ echo $LD_LIBRARY_PATH
linux:~ $ ldd my_program
```
