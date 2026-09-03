# dymanic function

## example

```python
def msg(p, u):
    print(f"{p} {u}")

###
### raw function
###

def hello(u):
    msg("hello", u)

def hi(u):
    msg("hi", u)

def bye(u):
    msg("bye", u)

###
### => globals()[func] = value
###

from functools import partial

funs = ['hello', 'hi', 'bye']
for f in funs:
    globals()[f] = partial(msg, f)

###
### => etattr(module, func, value)
###

from functools import partial
import sys

current_module = sys.modules[__name__]
funs = ['hello', 'hi', 'bye']
for f in funs:
    setattr(current_module, f, partial(msg, f))

###
### run
###

hello('py')
hi('py')
bye('py')
```

**globals() (字典操作)**

1. 優點：
   - 速度快：直接對字典賦值，沒有函數呼叫與尋找物件屬性的開銷。
   - 程式碼短：一行搞定，不需要處理 sys.modules。
2. 缺點：
   - 魔法感太強：對於不熟悉 Python 內部機制的初學者來說，會覺得變數「憑空出現」。
   - 限制性：只能操作「當前模組」的全域空間，無法跨模組操作。
3. 適用：
   - 腳本內部的動態生成：在同一個 .py 檔案裡，根據 funs = ['hello', ...] 動態產生對應的函數給之後的邏輯使用。
   - 快速原型開發：不需要額外 import，隨手寫隨手用。

**setattr() (物件反射)**

1. 優點：
   - 統一性：在 Python 中，「一切皆物件」。用處理普通 Class 物件的方法來處理模組，邏輯非常一致。
   - 跨模組能力：它可以設定任何模組的變數。例如你可以 import other_mod 然後 setattr(other_mod, 'var', 1)。
2. 缺點：
   - 稍慢：涉及一次函數呼叫 (setattr) 與屬性查找。
   - 稍臃腫：需要處理 sys.modules[__name__]。
3. 適用：
   - 框架或 Plugin 開發：需要從一個主程式去注入（Inject）變數或函數到「其他的模組」中時。
   - 嚴謹的物件導向設計：代碼風格保持一致（全部都用 getattr/setattr），不希望混用字典操作。

---

**Command Pattern (命令模式)**：將「請求」（執行函數）封裝成一個物件。在這裡 partial 函數就是被封裝的命令，可隨時決定何時執行它。

**Dispatch Pattern (調度模式)**：透過一個中央入口（Dispatcher），根據傳入的字串或參數，動態地找到並執行對應的邏輯。

**Factory Pattern(工廠模式)**：不需要知道具體的函數是什麼，只需要告訴工廠一個「標籤」，工廠就會「生產」出對應的函數物件。

```python
from functools import partial

def msg(p, u):
    print(f"{p} {u}")

# Command Pattern
tasks = ['hello', 'hi', 'bye']
command_registry = {name: partial(msg, name)  for name in tasks}

# Dispatcher Pattern
def run_task1(task_name, *args, **kwargs):
    func = command_registry.get(task_name) or globals().get(task_name)

    if callable(func):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {task_name} fail: {e}")
    else:
        print(f"Error: not found '{task_name}'")

run_task1('hello', 'py')
run_task1('invalid_task', 'py')

# Factory Pattern
def run_task2(task_name):
    func = command_registry.get(task_name) or globals().get(task_name)

    if callable(func):
        try:
            print(f"--- {task_name} run ---")
            return func
            print(f"--- {task_name} done ---")
        except Exception as e:
            print(f"Error: {task_name} expect: {e}")
    else:
        print(f"Error: no found '{task_name}'")
        return lambda *args, **kwargs: print(f"Cannot run {task_name}")

run_task2('hello')('py')
run_task2('invalid_task')('py')
```
