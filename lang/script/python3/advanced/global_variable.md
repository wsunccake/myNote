# Global Variable

##　Global

1. 單一檔案內的 Global 使用：global

在同一個 .py 檔案內，定義在所有函數之外的變數就是全域變數。但想在函數內修改它，就必須聲明 global。

```bash
x = 10  # 全域變數

def update_x():
    global x  # 聲明：要修改的是外面那個 x，不是建立新的區域變數
    x = 20

update_x()
print(x)  # 輸出 20
```

**注意**：如果只是「讀取」全域變數而不用修改，則不需要加 global。

2. 跨檔案模組的 Global

```python
# config.py
val = 100
```

**使用 import** (推薦)

這種方式是透過「模組物件」來存取，變數會隨著模組的狀態同步更新。

```python
import config

config.val = 200  # 直接修改模組屬性
print(config.val) # 輸出 200
```

**使用 from ... import \*** (危險！)

這種方式會將變數複製一份到當前的命名空間。如果 val 是不可變類型（如整數、字串），修改後兩邊會失去同步。

```python
from config import val

val = 200  # 這只改了 main 裡的 val，config.py 裡的 val 還是 100
```

3. Sngleton Pattern

在多個檔案之間共享同一個全域狀態，最專業的做法是建立一個專門的 shared_data.py。

```python
# shared_data.py
MY_DATA = {}
```

```python
# worker.py
import shared_data

def update_data():
    # 這裡不需要 global，因為我們是在操作 shared_data 物件的屬性
    shared_data.MY_DATA['status'] = 'Active'
```

```python
# main.py
import shared_data
import worker

worker.update_data()
print(shared_data.MY_DATA)  # 輸出 {'status': 'Active'}
```

| 方式              | 作用域       | 推薦程度   | 說明                                     |
| ----------------- | ------------ | ---------- | ---------------------------------------- |
| global x          | 單一檔案內部 | ⭐⭐       | 少量使用 OK，多了會讓邏輯混亂。          |
| import module     | 跨檔案       | ⭐⭐⭐⭐⭐ | 最安全，透過 module.x 存取，路徑明確。   |
| from mod import x | 跨檔案       | ⭐         | 容易產生副本，導致不同步問題。           |
| 專屬變數檔案      | 全專案       | ⭐⭐⭐⭐⭐ | 適合存放配置（Config）或大型共享資料夾。 |

4. Assignment & Reference

**from shared_data import MY_DATA**

```python
# shared_data.py
MY_DATA = {}

def init_data():
    global MY_DATA
    # ⚠️ 致命傷：這裡用了重新賦值（建立新物件）
    MY_DATA = {'user': 'admin', 'status': 'active'}
    print(f"[share_data.py] 資料已初始化，地址: {id(MY_DATA)}")
```

```python
# main.py
from shared_data import INP_DATA, init_data

print(f"[main.py] 初始地址: {id(INP_DATA)}")

# 呼叫初始化函數
init_data()

# ❌ 這裡會出錯（或說結果不符合預期）
print(f"[main.py] 初始化後的資料: {INP_DATA}")
# 預期：{'user': 'admin', ...}
# 結果：{}  <-- 還是空的！
```

風險在於：

- 不可變物件 (int, str)：一旦修改，兩邊絕對不同步。
- 可變物件 (dict, list)：只要發生 = (重新賦值)，兩邊就會立刻斷開連結。

**MY_DATA = shared_data.MY_DATA**

```python
# shared_data.py
# 初始狀態
MY_DATA = {"version": "1.0"}

def reload_config():
    global MY_DATA
    # ⚠️ 致命動作：將變數重新指向一個新的記憶體位址
    MY_DATA = {"version": "2.0", "status": "updated"}
```

```python
import shared_data

# 建立捷徑：讓本地的 MY_DATA 指向目前 shared_data.MY_DATA 的記憶體位址
MY_DATA = shared_data.MY_DATA

print(f"原始資料: {MY_DATA}") # 輸出 {"version": "1.0"}

# 執行重新載入
shared_data.reload_config()

# ❌ 發生錯誤：本地的 MY_DATA 不會更新
print(f"更新後的本地 MY_DATA: {MY_DATA}")            # 依然是 {"version": "1.0"}
print(f"真正的 shared_data.MY_DATA: {shared_data.MY_DATA}") # 已經是 {"version": "2.0"}
```

| 寫法    | 代碼                            | 同步效果 | 評語                                  |
| ------- | ------------------------------- | -------- | ------------------------------------- |
| ❌ 錯誤 | from shared_data import MY_DATA | 差       | 容易產生副本，且無法追蹤來源。        |
| ⚠️ 風險 | MY_DATA = shared_data.MY_DATA   | 中       | 只要發生重新賦值（=），同步就會失效。 |
| ✅ 推薦 | shared_data.MY_DATA             | 完美     | 永遠指向原始物件，最安全。            |

---

## Singleton Clas

用 Singleton 包裝，即便內部字典換了，存取的屬性也會自動導向新位址。

```python
class GlobalConfig:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
        return cls._instance

# 這樣就算執行 GlobalConfig().data = {...}
# 任何地方呼叫 GlobalConfig().data 都會拿到最新版
```
