# Meta Programming

`Meta-Programming` 是程式設計中高級、也最像「魔法」的領域。核心理念是：讓程式碼具備自我意識，能夠觀察、修改、甚至創造自己。
「Code as Data」（程式即資料）是 `Meta-Programming` 設計的核心哲學。這意味著程式碼不再是死板、編譯後就固定的指令，而是可以像字串、列表一樣，在執行期被讀取、修改、甚至重新產生。

---

## 演進過程與歷史 (History)

`Meta-Programming` 並非新技術，它的發展與程式語言對「抽象化」的追求息息相關：

- 早期：LISP (1950s) - 始祖
  LISP 引入了 S-expression，讓程式碼的結構與數據結構（列表）完全一致。這催生了 Macro (巨集) 系統，工程師可以編寫巨集來在編譯前重新改寫程式邏輯。這是「代碼即數據」的最早實踐。

- 中期：C++ Template (1990s) - 編譯時元編程
  C++ 引入了模板（Templates），原本是為了泛型程式設計，但開發者發現它可以在編譯時期進行複雜計算（Template Metaprogramming, TMP），這讓程式在運行前就已經「自我進化」完成。

- 現代：Python, Ruby, JavaScript (2000s - 現在) - 執行時元編程
  動態語言將元編程推向巔峰。透過反射 (Reflection) 機制（如 Python 的 getattr, type(), metaclass），程式可以在執行中 (Runtime) 隨時增減屬性、動態產生函數或修改類別行為。

---

## 概念 (Conpcet)

- **Code as Data (程式碼即數據)**: 這是元程式設計的核心哲學。將程式的原始碼、類別定義、函式等結構不視為靜態的指令，而是看作可以被存取、分析和操作的數據結構。
- **Introspection (自省)**: 指程式在執行時期**檢查**自身結構和狀態的能力。例如，一個物件可以知道自己的類別是什麼、它有哪些屬性和方法。這是一種「唯讀」的操作。
- **Reflection (反射)**: 是自省的更進一步，指程式在執行時期**修改**自身結構和狀態的能力。例如，不僅能發現一個物件有某個屬性，還能動態地為它新增屬性、呼叫方法或甚至建立全新的類別。這是一種「讀寫」操作。
- **Compile-time vs. Run-time (編譯時期 vs. 執行時期)**:
  - **編譯時期元程式設計**: 在程式被編譯成可執行檔的過程中執行，其結果是直接改變了最終產生的程式碼。C++ Templates 是典型代表。優點是沒有執行時期的效能開銷。
  - **執行時期元程式設計**: 在程式執行的過程中動態地改變其行為。Python 的元程式設計大部分屬於此類。優點是極度靈活，可以根據執行環境的變化做出反應。
- **Code Generation (程式碼生成)**: 元程式設計的一種直接應用，即根據某些輸入或範本，自動產生出程式原始碼。例如，許多框架會根據一個設定檔或資料庫 schema 來自動產生對應的類別定義。

---

## 準則與規範 (Principles)

- 非必要，不使用：這是最重要的原則。如果能用一般的物件導向或函式式編程解決，就不要動用元程式設計。過度使用會顯著增加程式的複雜度。
- DRY (Don't Repeat Yourself)：元程式設計應服務於減少重複代碼，例如自動生成重複性極高的資料庫存取層（ORM）或處理繁瑣的樣板代碼。
- 最小驚訝原則 (Principle of Least Astonishment)：元程式設計不應改變開發者對語言行為的基本預期。例如，不應在背後偷偷修改標準函式庫的基礎行為，否則會讓除錯變得極其困難。

---

## 實踐方法

`Meta-programming` 主要透過其「一切皆物件」的特性與強大的內省（Introspection）機制來實現。以下是幾種常見的實踐方法：

1. 自省與反射 (Introspection & Reflection)
   - 工具：內建函數 `dir()`, `type()`, `getattr()`, `setattr()`, `hasattr()`, 以及 `inspect` 模組。
   - 核心：「在執行期查看並操縱物件」。自省（Introspection）是看，反射（Reflection）是動。
   - 實踐：利用字串名稱來存取物件屬性，打破靜態程式碼的束縛。
   - 應用場景：根據設定檔動態載入套件、將 JSON 資料自動對應到物件屬性。

   ```python
   class Plugin:
       def start(self):
           print("插件啟動")

   obj = Plugin()
   method_name = "start"  # 可能來自使用者輸入或設定檔

   if hasattr(obj, method_name):
       func = getattr(obj, method_name)
       func()
   ```

2. 裝飾器 (Decorators)
   - 工具：`@` 語法糖、閉包 (Closures)。
   - 核心：「不修改原程式碼，動態擴充功能」。它接收一個函數並返回一個增強版的函數。
   - 實踐：利用高階函數的概念，將邏輯「包裹」在目標函數外層。
   - 應用場景：權限驗證 (Auth)、效能監控 (Timing)、Flask/FastAPI 的路由定義。

   ```python
   def timer(func):
       def wrapper(*args, **kwargs):
           import time
           start = time.time()
           result = func(*args, **kwargs)
           print(f"耗時: {time.time() - start:.4f}s")
           return result
       return wrapper

   @timer
   def heavy_task(): time.sleep(1)
   ```

3. 動態類型與工廠 (Dynamic Type Creation)
   - 工具：三參數版的 type(name, bases, dict) 函數。
   - 核心：「類別也是物件，可以在執行期即時製造」。
   - 實踐：不使用 class 關鍵字，而是透過 type() 函數動態定義類別名稱、繼承關係與屬性。
   - 應用場景：根據資料庫結構動態產生對應的 Model 類別、自動化測試中的 Mock 物件。

   ```python
   # 動態建立一個繼承自 list 的類別
   DynamicClass = type("MyList", (list,), {"version": "1.0"})
   instance = DynamicClass([1, 2, 3])
   print(instance.version)  # 1.0
   ```

4. 元類別 (Metaclasses)
   - 工具：繼承 `type` 的類別，並在類別定義中使用 `metaclass=` 宣告。
   - 核心：「控制類別生成的模板」。如果說類別是物件的模板，元類別就是「類別的模板」。
   - 實踐：改寫元類別的 `__new__` 方法，在類別建立的瞬間攔截並修改其結構。
   - 應用場景：Django ORM 的欄位定義、強制 API 實作者必須包含特定方法、自動註冊所有子類別。

   ```python
   class Singleton(type):
       _instances = {}
       def __call__(cls, *args, **kwargs):
           if cls not in cls._instances:
               cls._instances[cls] = super().__call__(*args, **kwargs)
           return cls._instances[cls]

   class Database(metaclass=Singleton): pass
   ```

| 層次 | 技術方法             | 實作手段                          | 介入時機                | 適用情境                                   |
| ---- | -------------------- | --------------------------------- | ----------------------- | ------------------------------------------ |
| 初級 | 反射 (Reflection)    | `getattr`, `setattr`, `globals()` | 執行時 (隨時)           | 動態調用函數、根據配置檔綁定方法。         |
| 中級 | 裝飾器 (Decorators)  | `@wrapper` 語法                   | 定義時 (載入模組時)     | 日誌紀錄、權限檢查、快取機制 (Cache)。     |
| 高級 | 描述符 (Descriptors) | `__get__`, `__set__`              | 存取時 (讀寫屬性時)     | 驗證資料格式 (如 property)、類型檢查。     |
| 頂級 | 元類別 (Metaclasses) | 繼承 `type` 類別                  | 建立時 (類別物件生成時) | 框架開發、強制執行編碼規範、自動註冊插件。 |
| 極端 | 抽象語法樹 (AST)     | `ast` 模組                        | 編譯前 (解析原始碼)     | 代碼靜態分析、程式碼自動重寫。             |

---

## 特色分析

1. 優點
   - 減少重複程式碼 (DRY)：撰寫能生成程式碼的程式，避免手動撰寫大量相似或重複的邏輯，完美實踐「Don't Repeat Yourself」(DRY) 原則。
   - 提高開發效率與靈活性：透過動態生成程式碼，讓程式根據不同的情境（如資料庫欄位變化）自動調整行為，而不需要人工逐一修改代碼。
   - 增強程式抽象化能力：允許開發者定義更高階的抽象概念。例如在 Ruby 或 Elixir 中，可以利用巨集（Macros）或動態定義方法來創造更簡潔、更具表現力的 DSL（領域特定語言）。
   - 最佳化執行效能 (編譯期元程式設計)：如 C++ 的模板元程式設計（Template Metaprogramming），將計算或邏輯檢查移至編譯期完成，能生成更高效的機器碼，並在編譯時就發現類型錯誤。
   - 簡化維護工作：當底層邏輯需要變更時，只需修改負責「生成代碼」的元程式，所有受影響的邏輯會自動同步更新，減少遺漏錯誤的風險。

2. 缺點
   - 程式碼可讀性大幅下降：由於程式碼是在執行期動態生成或編譯期展開，在編輯器中看到的內容並非最終執行的邏輯。這種「程式碼不存在於原始碼中」的特性，會讓其他團隊成員難以理解程式的真實行為。
   - 除錯（Debug）極其困難：當程式出錯時，堆疊追蹤（Stack Trace）可能會指向動態生成的區塊，而非實際撰寫的檔案。例如在 C++ 中，模板錯誤訊息往往極其冗長且難以解讀。
   - 學習曲線陡峭：它要求開發者對程式語言的底層機制（如 AST 抽象語法樹、反射機制或編譯原理）有極深理解。對於經驗不足的開發者來說，過度使用元程式設計可能導致代碼變得過於「魔幻」（Magical）而失控。
   - 效能負擔與編譯耗時：
     - 執行期 (Runtime)：如 Ruby 或 Python 的動態方法定義，會增加額外的記憶體消耗與執行負擔。
     - 編譯期 (Compile-time)：如 C++ 的模板，過度使用會導致編譯時間劇增，且生成的二進位檔案體積可能因程式碼過度展開而變得巨大。
   - 潛在的安全風險：若元程式設計涉及將外部輸入（如字串）轉換為可執行程式碼，若過濾不當，極易引發代碼注入等資安漏洞。
   - IDE 與工具支援不佳：許多自動補全、靜態分析工具或語法檢查器無法預測動態生成的內容，這會降低開發效率並增加出錯機率。

3. 情境
   - API 封裝與 SDK 開發： 當你需要為幾百個 REST API 端點建立對應的 Python 函數時，動態註冊是唯一選擇。
   - ORM (Object-Relational Mapping)： 將資料庫的欄位（Table Column）自動映射成類別的屬性（Class Attribute）。
   - 裝飾器 (Decorators)： 統一處理日誌 (Logging)、權限驗證、快取等橫切關注點 (Cross-cutting concerns)。
   - DSL (Domain Specific Language)： 建立特定領域語言，讓非程式員也能透過簡單語法描述邏輯。
