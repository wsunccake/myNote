# Clean Code

Clean Code (潔淨程式碼) 的核心，不在於讓電腦讀懂（因為電腦什麼都讀得懂），而在於讓人讀懂。

## 實踐指南

1. 核心哲學：破窗效應與營地規則
   - 營地規則 (The Boy Scout Rule)： 走過路過，讓程式碼比你發現它時更乾淨一點。
   - 減少認知負荷： 好的程式碼應該像一篇優美的散文，閱讀時不需要停下來思考「這行到底在幹嘛？」。

2. 命名 (Naming)：見名知意
   命名是 Clean Code 的靈魂。好的命名應該直接回答：它為什麼存在？它做什麼？它怎麼被使用？
   - 避免誤導： 不要用 list 當變數名，除非它真的是個 List。
   - 使用可搜尋的名稱： 避免魔術數字（Magic Numbers）。
     - ❌ `if (status === 7)`
     - ✅ `const STATUS_PUBLISHED = 7; if (status === STATUS_PUBLISHED)`
   - 類別與方法： 類別（Class）應為名詞，方法（Method/Function）應為動詞。

3. 函式 (Functions)：短小、只做一件事
   函式是程式的基本單位，其核心原則如下：
   - 單一職責原則 (SRP)： 一個函式應該只做一件事，並把它做好。
   - 更短小： 函式不應超過 20 行，嵌套層次（if/else/for）不應超過兩層。
   - 參數越少越好： 最理想是 0 個，其次是 1~2 個，超過 3 個就應該考慮封裝成物件。
   - 無副作用： 函式不應偷偷修改全域變數或傳入的物件狀態。

4. 註解 (Comments)：不寫廢話
   「註解是為了彌補我們在程式碼表達能力上的失敗。」
   - 好的註解： 法律資訊、對意圖的解釋、警告可能的後果、TODO。
   - 壞的註解： 廢話（解釋代碼本身）、過時的註解、被註解掉的程式碼（直接刪掉，我們有 Git）。
     如果你需要寫長長的註解來解釋一段代碼，通常意味著你應該重構那段代碼。

5. 錯誤處理 (Error Handling)
   - 使用例外 (Exceptions) 而非回傳錯誤代碼： 這樣可以保持主邏輯的乾淨。
   - 別回傳 null： 這樣會強迫呼叫者到處寫 if (obj != null)。考慮回傳空集合或使用「特例模式 (Special Case Pattern)」。

6. 物件與資料結構
   - 德墨忒爾律 (Law of Demeter)： 最少知識原則。一個物件不應該知道它所操作物件的內部細節。
     - ❌ `user.getWallet().getMoney().amount()` (這是在「火車失事」)
     - ✅ `user.pay(amount)`

7. 格式 (Formatting)
   - 垂直密度： 相關的程式碼應該靠在一起。
   - 一致性： 團隊中應使用統一的格式化工具（如 Prettier, ESLint），不要在縮排是 2 格還是 4 格上浪費生命。

---

## SOLID 原則

五大原則（SOLID）是 Clean Code 的高階指引。核心目標是為了讓軟體易於擴充、易於維護、且低耦合。

### `S (Single Responsibility)`

單一職責。一個類別（或函式）應該只有一個引起它變化的原因。如果一個類別負責太多事（例如既處理資料又發送郵件），當郵件格式改變時，你可能會不小心弄壞資料處理的邏輯。

```python
# ❌ 錯誤示範：一個類別處理了儲存與輸出
class User:
    def __init__(self, name):
        self.name = name
    def save_to_db(self): # 職責 1: 資料庫操作
        print(f"Saving {self.name} to DB")
    def export_json(self): # 職責 2: 格式轉換
        return f'{{"name": "{self.name}"}}'

# ✅ 正確示範：將職責拆分
class User:
    def __init__(self, name):
        self.name = name

class UserRepository:
    def save(self, user):
        print(f"Saving {user.name} to DB")

class UserSerializer:
    def to_json(self, user):
        return f'{{"name": "{user.name}"}}'
```

### `O (Open/Closed)`

開放封閉原則（對擴展開放，對修改封閉）。軟體實體（類別、模組）應該對擴展開放，對修改封閉。當新需求進來時（例如增加新的折扣方式），應該是「增加新程式碼」，而不是「修改舊的 if-else」。

```python
# ❌ 錯誤示範：每增加一種折扣就要改一次原始碼
class DiscountService:
    def apply_discount(self, price, type):
        if type == "VIP":
            return price * 0.8
        elif type == "SALE":
            return price * 0.9

# ✅ 正確示範：使用繼承/多型擴展
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def calculate(self, price): pass

class VIPDiscount(Discount):
    def calculate(self, price): return price * 0.8

class SaleDiscount(Discount):
    def calculate(self, price): return price * 0.9

# 新增折扣時，只需建立新類別，不需要動到 DiscountService
```

### `L (Liskov Substitution)`

里氏替換（子類應可替換父類）。子類別必須能夠替換掉它們的父類別，且程式行為不變。確保繼承關係是正確的。如果子類別覆寫了父類別後，導致原本的邏輯崩潰，那這個繼承就是錯誤的（例如「鴕鳥」繼承「鳥類」，但鴕鳥不能飛，這就違反了 LSP）。

```python
# ❌ 錯誤示範：企鵝雖然是鳥，但不能飛，會導致呼叫者出錯
class Bird:
    def fly(self): pass

class Penguin(Bird):
    def fly(self):
        raise Exception("I can't fly!") # 違反 LSP，因為這破壞了 Bird 的行為預期

# ✅ 正確示範：重新定義抽象層級
class Bird: pass
class FlyingBird(Bird):
    def fly(self): pass
class Penguin(Bird):
    def swim(self): pass
```

### `I (Interface Segregation)`

介面隔離。不應該強迫客戶端依賴它們不使用的方法。避免「胖介面」。如果一個介面定義了太多方法，實作它的類別就必須實作所有方法，即使有些根本用不到。

```python
# ❌ 錯誤示範：印表機介面太過臃腫
class SmartPrinter(ABC):
    @abstractmethod
    def print(self): pass
    @abstractmethod
    def fax(self): pass

class OldPrinter(SmartPrinter):
    def print(self): print("Printing...")
    def fax(self): raise NotImplementedError("No fax support!") # 強迫實作不需要的功能

# ✅ 正確示範：拆分成細小的介面
class Printer(ABC):
    @abstractmethod
    def print(self): pass

class FaxMachine(ABC):
    @abstractmethod
    def fax(self): pass

class ModernAllInOne(Printer, FaxMachine):
    def print(self): pass
    def fax(self): pass
```

### `D (Dependency Inversion)`

依賴反轉。高層模組不應依賴低層模組，兩者都應依賴「抽象」。解開組件間的強耦合。例如，程式不應該直接依賴「MySQL」，而應該依賴「資料庫介面」，這樣以後換成 PostgreSQL 時，高層邏輯完全不需要更動。

```python
# ❌ 錯誤示範：高層直接依賴低層（強耦合）
class MySQLDatabase:
    def insert(self): print("Insert into MySQL")

class App:
    def __init__(self):
        self.db = MySQLDatabase() # 被綁死在 MySQL 了

# ✅ 正確示範：依賴抽象（解耦）
class Database(ABC):
    @abstractmethod
    def insert(self): pass

class MySQLDatabase(Database):
    def insert(self): print("MySQL")

class App:
    def __init__(self, db: Database): # 依賴介面
        self.db = db

# 現在可以輕易更換任何 Database 實作
app = App(MySQLDatabase())
```

---

## DIP

DIP - Dependency Inversion Principle (依賴反轉原則)，核心目標是解開模組之間的「強耦合」，讓系統更容易擴充與維護。

核心定義：

1. 高層模組（業務邏輯）：不應依賴低層模組（資料庫、UI、外部 API）。
2. 抽象（介面或抽象類別）：不應依賴細節（具體實作）。
3. 細節：應該依賴抽象。

簡單來說：不要讓大腦直接控制手指，而是讓大腦發出「抓取」的指令，至於手怎麼抓，由手的具體實現負責。而 DIP 是目標，而 DI 與 IoC 則是實現這個目標的手段與環境。

1. 降低耦合度： 如果高層直接依賴低層，當低層更換（例如從 MySQL 換到 MongoDB）時，高層也必須跟著修改。
2. 提高測試性： 依賴抽象後，我們可以在測試時輕易用一個「假物件 (Mock)」替換掉「真資料庫」。
3. 模組化： 高層邏輯（商業價值所在）變得很純粹，不被具體的技術工具所綁架。

❌ 違反 DIP 的情況（高層依賴低層）

這裡的 Notification（高層）直接依賴了 EmailSender（低層）。如果明天老闆說要加一個「簡訊通知」，你就得去改 Notification 的代碼。

```python
class EmailSender:
    def send(self, message):
        print(f"Sending Email: {message}")

class Notification:
    def __init__(self):
        # ❌ 直接依賴具體的實作類別
        self.sender = EmailSender()

    def send(self, message):
        self.sender.send(message)
```

✅ 符合 DIP 的情況（兩者依賴抽象）

定義一個抽象層 MessageSender。高層只管呼叫 send，不管是誰實作的。

```python
from abc import ABC, abstractmethod

# 1. 定義抽象 (Interface)
class MessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

# 2. 低層模組依賴抽象 (細節依賴抽象)
class EmailSender(MessageSender):
    def send(self, message):
        print(f"Sending Email: {message}")

class SmsSender(MessageSender):
    def send(self, message):
        print(f"Sending SMS: {message}")

# 3. 高層模組也依賴抽象
class Notification:
    def __init__(self, sender: MessageSender): # 注入抽象而非具體
        self.sender = sender

    def announce(self, message):
        self.sender.send(message)

# 使用時：
email_notif = Notification(EmailSender())
sms_notif = Notification(SmsSender())
```

### DI

Dependency Injection (依賴注入)

核心： 外部將依賴物件「注入」給類別，而不是類別自己去 new（建立）物件。
解耦： 類別不需要知道依賴物件是怎麼產生的。
測試： 可以輕鬆注入假物件（Mock）。

範例：發送歡迎郵件的服務

❌ 反例：不使用 DI (硬編碼依賴)

```python
# 低層模組：具體的發信工具
class EmailTool:
    def send(self, recipient, message):
        print(f"正在發送郵件給 {recipient}: {message}")

# 高層模組：業務邏輯
class UserService:
    def __init__(self):
        # ❌ 錯誤：在內部直接實例化依賴物件
        self.email_tool = EmailTool()

    def register_user(self, email):
        print(f"用戶 {email} 註冊成功！")
        self.email_tool.send(email, "歡迎加入我們！")

# 使用方式
service = UserService()
service.register_user("test@example.com")
```

1. 難測試： 想寫單元測試，每次執行 register_user 都會真的發出一封郵件。沒辦法輕鬆地換成一個「假郵件工具 (Mock)」。
2. 違反 OCP (開放封閉原則)： 如果明天要改成「發送簡訊 (SMS)」，必須打開 UserService.py 修改內部的代碼。
3. 強耦合： UserService 必須知道 EmailTool 如何初始化（例如是否需要 API Key）。

✅ 使用 DI (建構子注入)

```python
from abc import ABC, abstractmethod

# 1. 定義抽象介面 (符合 DIP 原則)
class MessageSender(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass

# 2. 實作具體的工具
class EmailSender(MessageSender):
    def send(self, recipient, message):
        print(f"📩 郵件發送成功至 {recipient}")

class SmsSender(MessageSender):
    def send(self, recipient, message):
        print(f"📱 簡訊發送成功至 {recipient}")

# 3. 高層模組：透過 DI 接收工具
class UserService:
    def __init__(self, sender: MessageSender):
        # ✅ 正確：依賴由外部注入，且依賴於抽象
        self.sender = sender

    def register_user(self, email):
        print(f"用戶 {email} 註冊完成。")
        self.sender.send(email, "歡迎！")

# --- 執行時的靈活性 ---

# 場景 A：正式環境發郵件
email_tool = EmailSender()
service_v1 = UserService(email_tool)
service_v1.register_user("boss@company.com")

# 場景 B：客戶要求改用簡訊，完全不需要改 UserService 的代碼
sms_tool = SmsSender()
service_v2 = UserService(sms_tool)
service_v2.register_user("client@phone.com")
```

注入方式：

- 建構子注入 (Constructor Injection)：最推薦，透過 public MyClass(IService service) 傳入。
- 屬性注入 (Property Injection)：透過 public IService Service { get; set; } 賦值。
- 方法注入 (Method Injection)：僅在特定方法呼叫時傳入依賴。

#### 建構子注入 (Constructor Injection)

最推薦且最常用 的方式。在物件初始化（**init**）時，就將所有必要的依賴傳進去。

- 優點： 確保物件在建立後就是「完整」的，且依賴關係非常透明。
- 缺點： 如果依賴太多，建構子的參數清單會變得很長。

```python
class Database:
    def connect(self):
        return "Connected to DB"

class UserService:
    def __init__(self, db: Database):
        # 在初始化時就注入依賴
        self.db = db

    def get_user(self):
        return f"User data from {self.db.connect()}"

# 使用方式
db = Database()
service = UserService(db) # 建立時就必須給予依賴
```

#### 屬性注入 (Property / Setter Injection)

物件建立時不傳入依賴，而是事後透過「屬性」或「Setter 方法」來設定。

- 優點： 適合「可選」的依賴，或是需要在執行期間動態更換依賴的場景。
- 缺點： 物件建立後可能處於「不完整」狀態（如果忘記設定屬性，呼叫方法會報錯）。

```python
class Logger:
    def log(self, msg):
        print(f"LOG: {msg}")

class OrderService:
    def __init__(self):
        # 初始時依賴可能為 None
        self.logger = None

    def process_order(self):
        if self.logger:
            self.logger.log("Processing order...")
        print("Order processed.")

# 使用方式
service = OrderService()
service.process_order()  # 此時沒有 Logger，只會印出 Order processed.

service.logger = Logger() # 事後注入
service.process_order()  # 此時會印出 LOG 並處理訂單
```

#### 方法注入 (Method Injection)

依賴不儲存在物件的屬性中，而是直接作為「方法參數」傳入。

- 優點： 最靈活。物件本身不持有依賴，只有在「執行特定任務」時才需要依賴。
- 缺點： 每次呼叫該方法都要傳入依賴，如果多個方法都需要同一個依賴，會造成重複。

```python
class Validator:
    def is_valid(self, data):
        return "@" in data

class EmailManager:
    def __init__(self, email_address):
        self.email = email_address

    # 依賴 (validator) 只在執行此方法時傳入
    def send_email(self, validator: Validator):
        if validator.is_valid(self.email):
            print(f"Sending email to {self.email}")
        else:
            print("Invalid email address")

# 使用方式
manager = EmailManager("test@example.com")
val = Validator()
manager.send_email(val) # 呼叫方法時才注入
```

| 注入方式   | 注入時機   | 適用場景                       | 強制性     |
| ---------- | ---------- | ------------------------------ | ---------- |
| 建構子注入 | 物件建立時 | 核心依賴，確保物件安全。       | 強制       |
| 屬性注入   | 物件建立後 | 可選依賴，或需要隨時切換實作。 | 非強制     |
| 方法注入   | 方法執行時 | 單次依賴，只有特定行為才需要。 | 視方法而定 |

### IoC

IoC - Inversion of Control (控制反轉)

是軟體工程中的一種設計思想，它是許多現代框架（如 Spring, Django, FastAPI）的靈魂。簡單來說，IoC 就是將程式中「物件的建立」與「流程的控制權」，從開發者手寫的代碼中抽離，交給一個外部容器或框架來管理。

❌ 反例：直接耦合 (沒有 IoC)

```python
class PostgreDatabase:
    def save(self, data):
        print(f"存入 PostgreSQL: {data}")

class UserService:
    def __init__(self):
        # ❌ 缺點：UserService 綁死了 PostgreDatabase
        self.db = PostgreDatabase()

    def create(self, user):
        self.db.save(user)
```

✅ 使用 IoC (手動 IoC)

step 1. 定義抽象 (Interface)

高層不依賴低層。

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass
```

step 2. 實作具體類別

變得「被動」，它們等待別人把依賴送進來。

```python
class MySQLDatabase(Database):
    def save(self, data):
        print(f"存入 MySQL: {data}")

class UserService:
    def __init__(self, db: Database):
        # ✅ 透過 DI 接收依賴，自己不建立
        self.db = db

    def create(self, user):
        self.db.save(user)
```

step 3. 建立 IoC 容器

把「建立物件」與「組裝依賴」的邏輯全部抽離到這裡。

```python
class ManualContainer:
    """
    這就是 IoC 容器。它負責：
    1. 實例化所有物件。
    2. 管理它們的生命週期 (例如是否為 Singleton)。
    3. 處理複雜的依賴鏈。
    """
    def __init__(self):
        # 這裡可以根據環境變數切換不同的資料庫實作
        self._db = MySQLDatabase() 
        
        # 組裝 UserService 並注入 db
        self._user_service = UserService(db=self._db)

    @property
    def user_service((self)):
        return self._user_service

# --- 使用方式 ---
container = ManualContainer()
service = container.user_service  # 開發者只需要向容器「要」物件
service.create("Alice")
```

1. 控制權轉移： UserService 不再控制 db 的建立，控制權轉移到了 ManualContainer 手中。
2. 解耦： 如果你想把 MySQL 換成 PostgreSQL，你只需要修改 ManualContainer 的一行代碼，UserService 完全不需要動。
3. 單一出口： 整個應用程式的物件組裝邏輯都在同一個地方，不會散落在代碼各處。

---

## 經典實踐

### `DRY (Don't Repeat Yourself)`

同一套邏輯不應該在多個地方重複出現。邏輯散落在各處，修改時容易漏掉。這會導致「修好 A 卻壞了 B」的窘境。

```python
# ❌ 錯誤：重複的計算邏輯
def get_admin_emails(users):
    return [u.email for u in users if u.is_admin and u.is_active]

def count_active_admins(users):
    # 重複了上面的過濾邏輯
    return len([u for u in users if u.is_admin and u.is_active])

# ✅ 正確：將邏輯提取到單一出口
def filter_active_admins(users):
    return [u for u in users if u.is_admin and u.is_active]

def get_admin_emails(users):
    return [u.email for u in filter_active_admins(users)]
```

### `KISS (Keep It Simple, Stupid)`

如果有簡單的寫法，就不要炫技。為什麼這樣做： 複雜的程式碼是 Bug 的溫床。過度設計（Over-engineering）會讓接手的人（或三個月後的你）看不懂。

```python
# ❌ 錯誤：過度使用複雜的 lambda 與 map (炫技但難讀)
process = lambda x: (x**2 if x % 2 == 0 else x + 1)
result = list(map(process, filter(lambda x: x > 0, data)))

# ✅ 正確：易讀的列表生成式或迴圈
result = []
for x in data:
    if x > 0:
        val = x**2 if x % 2 == 0 else x + 1
        result.append(val)
```

### `YAGNI (You Ain't Gonna Need It)`

只寫目前需要的代碼。不要為了「未來可能擴充」而寫一堆沒用的抽象層。

- 為什麼： 預測通常是不準的。沒用到的代碼也是負債，會干擾閱讀。
- 實踐： 發現自己在想「萬一以後要支援 X 功能...」時，請立刻停下來。

### `Principle of Least Astonishment`

程式碼的行為應該符合讀者的直覺。如果一個叫 get_user_name() 的函式偷偷修改了資料庫（副作用），開發者會非常驚訝且崩潰。

```python
# ❌ 錯誤：函式名稱與行為不符
def is_valid_user(user):
    if not user.email:
        user.delete() # 驚訝！檢查有效性竟然會刪除使用者？
        return False
    return True

# ✅ 正確：行為與名稱一致
def check_user_validity(user) -> bool:
    return bool(user.email)
```

### `Law of Demeter`

不要跟「陌生人」講話。只呼叫直接對象的方法。減少耦合。當底層結構改變時，高層不需要跟著改。

```python
# ❌ 錯誤：火車失事 (Chain calling)
# 這段代碼知道太多細節：User 有 Wallet, Wallet 有 Currency
if user.wallet.currency.type == "USD":
    pass

# ✅ 正確：封裝行為
if user.uses_currency("USD"):
    pass
```

### `Defensive Programming`

預設環境是不安全的，主動處理可能的異常輸入，而不是讓它崩潰。增加系統的穩定性與容錯力。

```python
def calculate_average(numbers):
    # 防禦性檢查：防止傳入空列表導致 ZeroDivisionError
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

### `TDD (Test-Driven Development)`

先寫測試再寫 Code。流程是：紅燈 (失敗) -> 綠燈 (通過) -> 重構。

- 確保每一行 Code 都有被測試覆蓋。
- 強迫思考「需求」而非「實作細節」。
- 重構時有安全感，不怕改壞。

### `Refactoring`

重構不是一個獨立的專案，而是日常開發的一環。

重構時機:

- 三則轉向法： 同樣的程式碼寫了第三次時。
- 增加新功能前： 為了讓新功能好寫，先重構舊代碼（Prep-refactoring）。
- 修復 Bug 時： 順便把周邊難懂的地方理順。
- Code Review 時： 團隊討論出的最佳實踐。

### 優先順序

1. KISS & YAGNI (先求簡單、不寫廢話)
2. DRY (消除重複)
3. SOLID & Law of Demeter (處理複雜度與耦合)

### 實踐工具

- Linter (靜態檢查)： 如 Python 的 flake8 或 pylint，檢查語法風格。
- Formatter (自動格式化)： 如 black 或 yapf，強制統一縮排與空白，避免團隊爭議。
- Type Hinting (型別標註)： Python 3.5+ 支援 typing，雖然 Python 是動態語言，但標註型別能極大提升閱讀性。

### 境界

- 底層： 格式化、命名、註解（讓程式碼「好看」）。
- 中層： SOLID、DRY、KISS（讓程式碼「好改」）。
- 高層： 設計模式、領域驅動設計 DDD（讓系統「好擴張」）。

---
