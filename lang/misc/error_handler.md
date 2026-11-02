# Error Handler - Cleanup

## C

```bash
#include <stdio.h>
#include <stdlib.h>

int resource_set_ready() {
    FILE *fp = NULL;
    int status = -1;

    fp = fopen("/tmp/payload.json", "w");
    if (!fp) goto cleanup; // 出錯直接跳轉至清理區塊

    if (fputs("{\"type\": \"TENANT\"}", fp) == EOF) {
        goto cleanup;      // 中途出錯同樣跳轉
    }

    // 執行核心邏輯...
    status = 0; // 成功標記

cleanup:
    // 👈 相當於 finally / trap RETURN 區塊
    if (fp) {
        fclose(fp);
        remove("/tmp/payload.json");
    }
    return status;
}
```

## GCC / Clang


```c
void cleanup_file(char **filepath) {
    if (*filepath) {
        remove(*filepath);
        printf("Cleanup: %s deleted\n", *filepath);
    }
}

void resource_set_ready() {
    // 當變數 path 離開 scope 時，自動呼叫 cleanup_file(&path)
    char *path __attribute__((cleanup(cleanup_file))) = "/tmp/payload.json";
    
    // 寫入檔案與執行 curl...
}
```

## Python

```python
import os

def resource_set_ready():
    payload_file = "/tmp/payload_temp.json"
    try:
        # 建立並寫入暫存檔
        with open(payload_file, "w") as f:
            f.write('{"type": "TENANT", "keys": ["scaletesting4608@email.com"]}')
        
        # 執行 HTTP POST 請求
        # response = requests.post(url, ...)
        
    finally:
        # 👈 相當於 Bash 的 trap RETURN / Groovy 的 finally
        # 無論前面成功、出錯或提前 return，這裡必定被執行
        if os.path.exists(payload_file):
            os.remove(payload_file)
```

```python
import os
from contextlib import contextmanager

@contextmanager
def temp_payload_file(data: str):
    payload_file = f"/tmp/payload_{os.getpid()}.json"
    try:
        with open(payload_file, "w") as f:
            f.write(data)
        yield payload_file  # 將暫存檔路徑交給外部 with 區塊使用
    finally:
        # 離開 with 區塊時自動執行刪除
        if os.path.exists(payload_file):
            os.remove(payload_file)

# 使用方式：
def resource_set_ready():
    payload_data = '{"type": "TENANT", "keys": ["scaletesting4608@email.com"]}'
    
    with temp_payload_file(payload_data) as filepath:
        # 在此區塊內使用 filepath 發送請求
        print(f"Sending request with file: {filepath}")
    # 👈 一離開 with 區塊，temp_payload_file 的 finally 就會自動被觸發並刪除檔案
```

## Go

```go
package main

import (
    "os"
    "fmt"
)

func resourceSetReady() error {
    // 1. 建立暫存檔
    tmpFile, err := os.CreateTemp("", "payload_*.json")
    if err != nil {
        return err
    }
    
    // 2. 註冊 defer 清理動作（會在函數 return 前強制執行，相當於 trap RETURN / finally）
    defer func() {
        tmpFile.Close()
        os.Remove(tmpFile.Name())
        fmt.Println("Cleanup executed!")
    }()

    // 3. 寫入資料與執行 HTTP POST...
    tmpFile.WriteString(`{"type": "TENANT"}`)
    
    // 中途即使發生 error 或正常 return，defer 都保證會跑
    return nil 
}
```

## Rust

```rust
struct TempFile {
    path: String,
}

// 為結構實作 Drop 特性
impl Drop for TempFile {
    fn drop(&mut self) {
        println!("Cleanup: Deleting {}", self.path);
        let _ = std::fs::remove_file(&self.path);
    }
}

fn resource_set_ready() -> Result<(), Box<dyn std::error::error>> {
    let temp = TempFile { path: "/tmp/payload.json".to_string() };
    std::fs::write(&temp.path, r#"{"type": "TENANT"}"#)?;

    // 執行 curl 或 API 呼叫
    // ...

    Ok(()) 
    // 👈 無論是正常 Ok(()) 離開，或是中途用 `?` 拋出 Err 離開，
    // `temp` 離開 Scope 時都會自動觸發 `drop()` 清理檔案！
}
```


## Bash

```bash
resource_set_ready() {

trap 'rm -f "${payload_file}"' RETURN
}
```