# Error handler

遇到錯誤而提前結束時，仍要能做清理（關檔、刪暫存、釋放資源）。下面各語言是同一件事：先取得資源並掛上清理，再故意做一件會失敗的事。清理仍會跑，失敗點之後的那一行不會跑。

---

## C

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    char tmp_path[] = "/tmp/error-handler-XXXXXX";
    int fd = -1;
    int exit_code = 0;

    fd = mkstemp(tmp_path);
    if (fd == -1) {
        perror("mkstemp");
        return 1; /* 檔案還沒建立，沒有東西要清 */
    }

    /* 模擬發生錯誤 */
    if (access("/no/such/file", F_OK) != 0) {
        perror("access");
        exit_code = 1;
        goto cleanup;
    }

    printf("這行不會被執行\n");

cleanup:
    if (fd != -1) {
        printf("[Error Handler] 正在清除暫存檔: %s (Exit code: %d)\n",
               tmp_path, exit_code);
        close(fd);
        unlink(tmp_path);
    }
    return exit_code;
}
```

1. 順序：資源建立成功後，失敗路徑一律 `goto cleanup`，不要在中間 `return`，否則清理被跳過。取得失敗（還沒有資源）才直接 `return`。
2. 變數：指標與 fd 先設成 `NULL` / `-1`，cleanup 先檢查再釋放。多個資源依取得的相反順序釋放。
3. 結束方式：正常路徑也要落到 `cleanup`（不要在成功時另外 `return`）。`exit()`、`_exit()`、`longjmp` 不會走這個標籤。

---

## GCC

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* 參數是變數的位址：變數型別是 char *，這裡就是 char ** */
static void cleanup_path(char **path) {
    if (path && *path) {
        printf("[Error Handler] 正在清除暫存檔: %s\n", *path);
        unlink(*path);
    }
}

int main(void) {
    char storage[] = "/tmp/error-handler-XXXXXX";
    char *tmp_file __attribute__((cleanup(cleanup_path))) = NULL;
    int fd;

    fd = mkstemp(storage);
    if (fd == -1) {
        perror("mkstemp");
        return 1;
    }
    close(fd);
    tmp_file = storage; /* 指派之後，離開這個 scope 就會刪檔 */

    /* 模擬發生錯誤：提前 return，cleanup 仍會執行 */
    if (access("/no/such/file", F_OK) != 0) {
        perror("access");
        return 1;
    }

    printf("這行不會被執行\n");
    return 0;
}
```

1. 順序：`mkstemp` 成功後立刻把路徑指派給帶 `cleanup` 的變數，再做可能失敗的事。指派前就 `return`，回呼看到的是 `NULL`，檔案會漏掉。
2. 變數：回呼收到的是變數位址，不是值。回呼裡要檢查 `NULL`。區域陣列本身不要掛 `cleanup` 再讓別的指標指它；宣告在後面的變數先清，被指到的緩衝區要活得比回呼久。
3. 結束方式：`return` 離開 scope 就會跑，正常結束與錯誤結束都會。`exit()`、`_exit()`、`longjmp` 不會跑。這是 GCC / Clang 擴充，不是標準 C。

---

## Rust

```rust
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;

struct TempFile {
    path: PathBuf,
}

impl TempFile {
    fn create() -> std::io::Result<Self> {
        let path = std::env::temp_dir().join(format!("error-handler-{}", std::process::id()));
        let mut file = File::create(&path)?;
        writeln!(file, "data")?;
        Ok(Self { path })
    }
}

impl Drop for TempFile {
    fn drop(&mut self) {
        println!(
            "[Error Handler] 正在清除暫存檔: {}",
            self.path.display()
        );
        let _ = fs::remove_file(&self.path);
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let _tmp = TempFile::create()?;

    // 模擬發生錯誤：? 提前返回時，_tmp 離開 scope，Drop 仍會執行
    fs::read("/no/such/file")?;

    println!("這行不會被執行");
    Ok(())
}
```

1. 順序：先把守護值綁到區域變數，再做可能失敗的事。`?` 或 `return` 離開函式時，已建立的區域值會依宣告的相反順序 `drop`。
2. 變數：`Drop::drop` 拿到的是 `&mut self`。清理必須可以重複面對「只建了一半」的狀態；失敗的 `create()` 不會產生值，也就不會 `drop`。
3. 結束方式：正常離開 scope、`?`、`return` 都會 `drop`。panic 在 unwind 時也會；`panic = "abort"` 不會。`process::exit`、`mem::forget`、`ManuallyDrop` 會跳過 `Drop`。

---

## Go

```go
package main

import (
	"fmt"
	"os"
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run() (err error) {
	f, err := os.CreateTemp("", "error-handler-")
	if err != nil {
		return err
	}
	tmpFile := f.Name()
	f.Close()

	defer func() {
		fmt.Printf("[Error Handler] 正在清除暫存檔: %s (Error: %v)\n", tmpFile, err)
		os.Remove(tmpFile)
	}()

	// 模擬發生錯誤：return 之後 defer 仍會執行
	_, err = os.Open("/no/such/file")
	if err != nil {
		return err
	}

	fmt.Println("這行不會被執行")
	return nil
}
```

1. 順序：`CreateTemp` 成功後立刻 `defer`，再做可能失敗的事。`defer` 在 `CreateTemp` 之前註冊的話，路徑還是空的。多個 `defer` 依註冊的相反順序執行。
2. 變數：`defer f(tmpFile)` 的參數在註冊當下就求值。要讀到回傳前的最新值，用 `defer func() { ... }()`。具名回傳值 `err` 在 `defer` 執行時已經設好，所以清理看得到這次的錯誤。
3. 結束方式：函式 `return`（含錯誤）會跑 `defer`。`panic` 也會，且可在 `defer` 裡 `recover`。`os.Exit` 不會跑 `defer`。

---

## Bash

```bash
#!/usr/bin/env bash
set -e # 遇到 error 即刻停止

cleanup() {
  local exit_code=$?
  if [ -n "$tmp_file" ] && [ -f "$tmp_file" ]; then
    echo "[Error Handler] 正在清除暫存檔: $tmp_file (Exit code: $exit_code)"
    rm -fv "$tmp_file"
  fi
}

# 註冊 EXIT 訊號：不論是正常結束還是因為 set -e 觸發錯誤退出，都會執行 cleanup
trap cleanup EXIT

tmp_file=$(mktemp)

# 模擬發生錯誤
ls -l ab

echo "這行不會被執行"
```

1. 順序極為重要：trap 一定要放在 mktemp 之後、任何可能失敗的命令之前。
2. 變數引用：trap 內部的變數建議在外層 double quote 或單引號展開時注意變數作用域，例如 'rm -fv "$tmp_file"' 能確保函式結束前讀取到的 $tmp_file 路徑正確。
3. Signal 選擇：
   - RETURN：當前函式返回時觸發（適合封裝在 function 內部的區域資源清理）。
   - EXIT：腳本 exit 時觸發（適合腳本層級的全域資源清理）。
   - ERR：僅在指令回傳非 0 狀態時觸發。

---

## Python

`try` / `finally`：離開 `try` 時一定進 `finally`，例外不會被吃掉。

```python
import os
import tempfile

def main():
    fd, tmp_file = tempfile.mkstemp()
    os.close(fd)
    try:
        # 模擬發生錯誤
        open("/no/such/file")
        print("這行不會被執行")
    finally:
        if os.path.exists(tmp_file):
            print(f"[Error Handler] 正在清除暫存檔: {tmp_file}")
            os.remove(tmp_file)

if __name__ == "__main__":
    main()
```

`with`：離開區塊時呼叫 `__exit__`，區塊裡發生例外也一樣。

```python
import os
import tempfile

class TempFile:
    def __enter__(self):
        fd, self.path = tempfile.mkstemp()
        os.close(fd)
        return self.path

    def __exit__(self, exc_type, exc, tb):
        if self.path and os.path.exists(self.path):
            print(f"[Error Handler] 正在清除暫存檔: {self.path} (Error: {exc})")
            os.remove(self.path)
        return False  # 不吞掉例外，讓它繼續往外丟

with TempFile() as path:
    open("/no/such/file")  # 模擬發生錯誤
    print("這行不會被執行")
```

1. 順序：先建立暫存檔，再進入 `try` 或 `with`。建立失敗就不該刪一個還沒有的路徑。`with` 的建立放在 `__enter__`，清理放在 `__exit__`。
2. 變數：`finally` 讀的是外層變數當下的值。`__exit__` 的三個參數是例外型別、例外物件、traceback；沒有例外時都是 `None`。
3. 結束方式：`return`、`break`、`continue`、例外都會跑 `finally` / `__exit__`。`__exit__` 回傳真值會把例外吞掉，清理完要回傳 `False`。`os._exit()` 與 `SIGKILL` 不會跑。

---

## Java

```java
import java.nio.file.Files;
import java.nio.file.Path;

public class ErrorHandler {
    public static void main(String[] args) throws Exception {
        Path tmp = Files.createTempFile("error-handler-", ".tmp");
        try {
            // 模擬發生錯誤
            Files.readString(Path.of("/no/such/file"));
            System.out.println("這行不會被執行");
        } finally {
            System.out.println("[Error Handler] 正在清除暫存檔: " + tmp);
            Files.deleteIfExists(tmp);
        }
    }
}
```

1. 順序：`createTempFile` 成功後才進入 `try`。建立丟出例外時還沒有 `finally` 要清的檔。多個資源在 `finally` 裡依取得的相反順序關閉。
2. 變數：`finally` 看得到 `try` 外面的 `tmp`。`try` 裡新宣告的變數，`finally` 看不到。
3. 結束方式：例外、`return`、`break`、`continue` 都會跑 `finally`，跑完例外仍往外丟。`System.exit()` 不會跑。資源若實作 `AutoCloseable`，改用 try-with-resources：`close()` 在 `finally` 之前、依宣告的相反順序執行；本體與 `close()` 都丟例外時，本體是主要例外，`close()` 的掛在 suppressed。
