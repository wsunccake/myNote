# enum

## Enum

一、基本語法與實務使用

1. 基本宣告與定義

Rust 的 enum 允許每個變體（Variant）攜帶不同型別與數量的資料：

```rust
// 宣告一個描述網路請求狀態的 Enum
enum IpAddr {
    V4(u8, u8, u8, u8),      // 元組（Tuple）形式
    V6(String),              // 單一型別形式
    Unknown,                 // 無資料變體
    Custom { name: String }, // 具名結構體（Struct）形式
}
```

2. 建立與儲存變數（Instantiation）

```rust
fn main() {
    // 1. V4: 儲存 4 個 u8 數字
    let home = IpAddr::V4(127, 0, 0, 1);

    // 2. V6: 儲存 String 字串
    let loopback = IpAddr::V6(String::from("::1"));

    // 3. Unknown: 不帶任何資料
    let invalid_ip = IpAddr::Unknown;

    // 4. Custom: 帶有欄位名稱的 Struct 形式
    let internal_ip = IpAddr::Custom {
        name: String::from("Internal-Mesh-Network"),
    };
}
```

3. 使用 match 進行樣式比對與拆解（Deconstruction）

```rust
fn print_ip_info(ip: &IpAddr) {
    match ip {
        IpAddr::V4(a, b, c, d) => {
            println!("IPv4 位置: {}.{}.{}.{}", a, b, c, d);
        }
        IpAddr::V6(addr) => {
            println!("IPv6 位置: {}", addr);
        }
        IpAddr::Unknown => {
            println!("未知或未設定的 IP 位置");
        }
        IpAddr::Custom { name } => {
            println!("自訂網路名稱: {}", name);
        }
    }
}
```

4. impl 實作方法

```rust
impl IpAddr {
    // 判斷是否為 本機迴路位置 (Loopback)
    fn is_loopback(&self) -> bool {
        match self {
            IpAddr::V4(127, 0, 0, 1) => true,
            IpAddr::V6(addr) if addr == "::1" => true,
            _ => false,
        }
    }

    // 統一格式化輸出字串
    fn to_display_string(&self) -> String {
        match self {
            IpAddr::V4(a, b, c, d) => format!("{}.{}.{}.{}", a, b, c, d),
            IpAddr::V6(addr) => addr.clone(),
            IpAddr::Unknown => String::from("0.0.0.0"),
            IpAddr::Custom { name } => format!("Custom({})", name),
        }
    }
}

fn main() {
    let my_ip = IpAddr::V4(127, 0, 0, 1);

    println!("是否為 Loopback? {}", my_ip.is_loopback()); // true
    println!("顯示結果: {}", my_ip.to_display_string());  // "127.0.0.1"
}
```

5. 集合與陣列中的實際應用

```rust
fn main() {
    // 將不同型態的 IP 放在同一個 Vector 中
    let client_endpoints = vec![
        IpAddr::V4(192, 168, 1, 100),
        IpAddr::V6(String::from("fe80::1")),
        IpAddr::Unknown,
        IpAddr::Custom { name: String::from("Docker-Bridge") },
    ];

    for (index, ip) in client_endpoints.iter().enumerate() {
        println!("Client #{}: {}", index, ip.to_display_string());
    }
}
```

### 延伸四大核心支柱

Rust 很多高階、安全的語法特性，看作是以 enum 為核心建構出來的生態系：

1. 空值安全：Option<T>
   - 本質：標準庫裡的 enum。
   - 應用：用 Some(T) 包裹資料，用 None 代表空值。完全取代了傳統語言的 null，把 Null Pointer 崩潰的問題搬到編譯期解決。

2. 錯誤處理：Result<T, E>
   - 本質：標準庫裡的另一個 enum。
   - 定義：

   ```rust
   pub enum Result<T, E> {
       Ok(T),  // 成功：包裹成功的結果 T
       Err(E), // 失敗：包裹錯誤的原因 E
   }
   ```

   - 應用：Rust 沒有傳統語言的 try-catch 異常機制（Exception）。所有可能失敗的操作（如開檔、連線）都回傳 Result，強制你用處理 Option 的同一套邏輯（unwrap、match、? 運算子）來面對錯誤。

3. 複合資料解構：match 與 Pattern Matching
   - 本質：專為 enum 打造的控制流語法。
   - 應用：因為 enum 可以攜帶資料，傳統的 switch-case 根本無法勝任。match 應運而生，讓你既能「檢查是哪種變體」，又能在同一時間把包裹裡面的資料「拆出來（Unpack）」。

4. 領域模型設計（Domain Modeling）
   - 本質：自定義多狀態結構。
   - 應用：在 Web 開發或遊戲開發中，用 enum 可以完美表達「非此即彼，且各帶不同資料」的狀態機（State Machine）：
   ```rust
   enum WebEvent {
       PageLoad,                 // 不帶資料
       KeyPress(char),           // 帶一個字元
       Paste(String),            // 帶一個字串
       Click { x: i64, y: i64 }, // 帶一個匿名結構體
   }
   ```

```
               ┌── Option<T>   ──────> 代替 null (Some / None)
               │
               ├── Result<T, E> ─────> 代替 try-catch (Ok / Err)
Rust enum  ────┼─ Pattern Matching ──> match / if let / let-else (拆包取值)
               │
               └── State Machine ────> 自訂複雜多變體資料結構
```

Rust 透過把 enum（可攜帶資料的列舉） 與 Pattern Matching（模式匹配） 結合在一起，一次性優雅地解決了 Null 安全、錯誤處理 與 狀態管理 這三大編程難題。

---

## Some

在 Rust 中，Some 不是一個獨立的函數或關鍵字，而是標準庫內建型別 Option<T> 的其中一個變體（Variant）。

核心目的只有一個：代表「有資料」，並將真正的數值包裹（Wrap）起來。

在 Rust 中，Option 列舉（Enum）的定義如下：

```rust
// 這就是 Rust 標準庫中 Option 的真實定義！
pub enum Option<T> {
    None,    // 變體 1：代表「沒有資料」
    Some(T), // 變體 2：代表「有資料」，並將型別為 T 的資料包裹在裡面
}
```

1. 打包資料（Wrap）

當一個函數可能回傳資料、也可能回傳空值時，如果有資料，就用 Some(資料) 包起來回傳：

```rust
// 尋找陣列中的第一個偶數
fn find_first_even(numbers: Vec<i32>) -> Option<i32> {
    for num in numbers {
        if num % 2 == 0 {
            return Some(num); // 找到偶數，用 Some 包裹回傳
        }
    }
    None // 沒找到偶數，回傳 None
}

fn main() {
    let numbers = vec![1, 3, 5, 8, 9];
    let result = find_first_even(numbers); // 型別為 Option<i32>，值為 Some(8)
}
```

2. 拆包取值（Unwrap / Destructuring）

被 Some 包起來的值不能直接拿來做運算（例如 Some(5) + 3 會編譯錯誤）。你必須用安全的方式將裡面的值「拆出來」：

- 方法 A：使用 match（最完整的模式匹配）

```rust
let config_max: Option<u8> = Some(10);

match config_max {
    Some(max) => println!("最大值是：{max}"), // 自動解構出 max (u8)
    None => println!("沒有設定最大值"),
}
```

- 方法 B：使用 if let（只關心有值的情況）

```rust
let user_name: Option<String> = Some(String::from("Alice"));

// 只要是 Some，就解構出 name 變數供內部使用
if let Some(name) = user_name {
    println!("Hello, {name}!");
}
```

- 方法 C：使用 .unwrap_or()（提供預設後備值，最簡短）

```rust
let score: Option<i32> = Some(95);

// 有值就拿 95，如果是 None 就拿預設值 0
let final_score = score.unwrap_or(0);
println!("分數：{final_score}"); // 95
```

3. 快速對照與選用指南

| 操作 / 方法                    | 安全性   | 說明 / 適用場景                                 |
| ------------------------------ | -------- | ----------------------------------------------- |
| Some(x)                        | Safe     | Wrap (包裹)：把值包成 Option<T>。               |
| None                           | Safe     | 表示「無資料 / Null」。                         |
| .unwrap()                      | ⚠️ 高風險 | 確定 100% 有值或寫 Unit Test 時才用。           |
| ".expect(""msg"")"             | ⚠️ 高風險 | 比 unwrap() 好，崩潰時會印出說明。              |
| .unwrap_or(val)                | Safe     | 最推薦：沒值就用後備常數。                      |
| if let Some(x)                 | Safe     | 只想對「有值」的情況處理時。                    |
| let Some(x) = opt else { ... } | Safe     | 函數開頭進行 Guard Clause（檢查不通過就離開）。 |
| match opt { ... }              | Safe     | 有值與沒值兩者都要執行複雜邏輯時。              |

4. if, match, let if

- if

```rust
fn main() {
    let val = Some(10);
    let res = if val.is_some() { val.unwrap() } else { 0 };

    println!("val: {val:?}, res: {res:?}");
}
```

- match

```rust
fn main() {
    let val = Some(10);
    let res = match val {
        Some(x) => x,
        _ => 0,
    };

    println!("val: {val:?}, res: {res:?}");
}
```

- if let

```rust
fn main() {
    let val = Some(10);
    let res = if let Some(x) = val {x} else {0};

    println!("val: {val:?}, res: {res:?}");
}
```

---

## Option

Option<T> 是 Rust 用來完全取代 null 的核心型別。它在標準庫中本質上就是一個列舉（enum），專門用來處理「資料可能存在，也可能不存在」的情境。

透過型別系統，Rust 在編譯期就強制要求你處理「空值（None）」的情況， 從根本上杜絕了執行期 Null Pointer 崩潰的隱患。

Option<T> 的底層定義

```rust
pub enum Option<T> {
    Some(T), // 有值：將型別為 T 的資料包裹在裡面
    None,    // 沒值：代表空值（相當於 null）
}
```

- 不需要 Option:: 前綴：因為太常用，Rust 自動包含了 Option、Some 與 None，可以直接使用。

常見建立與使用方式

1. 建立 Option 變數

```rust
let has_value: Option<i32> = Some(42);   // 確定有值，用 Some 包裹
let no_value: Option<i32> = None;        // 沒有值，直接賦予 None
```

2. 在結構體（Struct）中作為可選欄位

```rust
struct User {
    id: u64,
    username: String,
    email: Option<String>, // email 可填（Some）可不填（None）
}

let user1 = User {
    id: 1,
    username: String::from("Alice"),
    email: Some(String::from("alice@example.com")),
};

let user2 = User {
    id: 2,
    username: String::from("Bob"),
    email: None, // 沒有 email
};
```

提取 Option 內部數值（解包/Unwrap）的 4 種實務寫法

被 Option 包裹的值無法直接使用（如 Some(5) + 3 會編譯錯誤），必須透過以下方式安全地取出裡面的值：

- 寫法 A：.unwrap_or()（最推薦、最簡短）

有值就拿，是 None 就直接使用你給的預設值。

```rust
let score: Option<i32> = None;
let final_score = score.unwrap_or(0); // 取不出值就用 0 代替
println!("最終分數：{final_score}"); // 輸出 0
```

- 寫法 B：if let（只關心「有值」的情況）

適用於當資料是 Some 時才執行特定邏輯，是 None 就直接忽略。

```rust
let msg: Option<String> = Some(String::from("Hello World"));

if let Some(text) = msg {
    println!("收到訊息：{text}");
}
```

- 寫法 C：match（強制處理「有值」與「無值」兩種情況）

適用於 Some 與 None 都需要執行較複雜的邏輯時。

```rust
fn check_user_email(user: &User) {
    match &user.email {
        Some(email) => println!("傳送郵件至：{email}"),
        None => println!("該使用者未設定 Email，跳過發送"),
    }
}
```

- 寫法 D：let-else（Guard 寫法，失敗直接離開）

適合用於函數開頭進行條件檢查，若為 None 則直接 return 或 break。

```rust
fn process(data: Option<i32>) {
    // 若為 None 則執行 else 塊並跳出函數，否則將內部數值直接提取並綁定給 val
    let Some(val) = data else {
        println!("無效資料，退出程序");
        return;
    };

    println!("順利拿到資料進行處理：{val}");
}
```

綜合範例：查詢與處理資料

```rust
fn find_user_by_id(id: u64) -> Option<String> {
    if id == 100 {
        Some(String::from("Alice"))
    } else {
        None
    }
}

fn main() {
    let user_id = 100;

    // 呼叫會回傳 Option<String> 的函數
    let user_name = find_user_by_id(user_id);

    // 透過語法糖 `.map()` 在確定有值時轉換文字，並用 .unwrap_or() 作為後備
    let greeting = user_name
        .map(|name| format!("歡迎回來，{name}！"))
        .unwrap_or_else(|| String::from("歡迎，訪客！"));

    println!("{greeting}");
}
```

遇到可能為空的資料 ➔ 函數簽名或欄位型別一律宣告為 Option<T>。
有資料時 ➔ 回傳 Some(value)。
無資料時 ➔ 回傳 None。
拿取資料時 ➔ 優先使用 .unwrap_or()、if let 或 let-else 進行安全解包，避免使用會導致崩潰的暴力解包 .unwrap()。

### Option 的組合子（Combinator）

在 Rust 中，如果每次處理 Option 都寫 match 或 if let，程式碼很快就會變得冗長且層層巢狀。

組合子（Combinator） 是 Option 提供的一套高階函數，允許你使用宣告式（Declarative）與鏈式呼叫（Method Chaining）的方式，在不解包（Unwrap）的情況下直接對包裹內部的值進行轉換、過濾或串接。

1. .map()：轉換內部的資料
   - 作用：如果 Option 是 Some(v)，就將內部的 v 傳入閉包（Closure）進行轉換，並把結果重新包成 Some 回傳；如果是 None，則直接回傳 None，完全不執行閉包。
   - 閉包簽名：FnOnce(T) -> U（回傳普通數值 U）。
   - 使用時機：單純想改變資料型別或內容（例如：字串轉長度、數字乘倍數），且轉換過程不會失敗。

   ```rust
   let num: Option<i32> = Some(5);
   let string_len: Option<usize> = Some(String::from("Rust"));

   // 5 -> 10，結果仍為 Option<i32>
   let doubled = num.map(|x| x * 2); // Some(10)

   // "Rust" -> 4，結果變為 Option<usize>
   let len = string_len.map(|s| s.len()); // Some(4)

   let none_val: Option<i32> = None;
   let result = none_val.map(|x| x * 2); // None（閉包不會執行）
   ```

2. .and_then()：串接可能失敗的操作 (FlatMap)
   - 作用：如果 Option 是 Some(v)，就將 v 傳入閉包。這個閉包自身也會回傳一個 Option；如果是 None，則直接回傳 None。
   - 閉包簽名：FnOnce(T) -> Option<U>（回傳另一個 Option）。
   - 使用時機：當下一步轉換操作本身也可能回傳 None 時（例如：查資料庫、轉型、存取陣列）。使用 .and_then() 可以避免產生 Option<Option<T>> 這種尷尬的雙層包裹（自動扁平化 / Flatten）。

   ```rust
   fn parse_number(s: &str) -> Option<i32> {
       s.parse().ok() // 解析成功回傳 Some(i32)，失敗回傳 None
   }

   let input: Option<&str> = Some("123");

   // 如果用 .map() 會變成 Option<Option<i32>>：
   // let bad: Option<Option<i32>> = input.map(|s| parse_number(s));

   // 使用 .and_then() 會自動扁平化，維持 Option<i32>：
   let number: Option<i32> = input.and_then(|s| parse_number(s)); // Some(123)

   let invalid_input: Option<&str> = Some("abc");
   let failed = invalid_input.and_then(|s| parse_number(s)); // None
   ```

3. .filter()：根據條件過濾資料
   - 作用：如果 Option 是 Some(v)，且 v 滿足閉包中的布林條件（回傳 true），則保留 Some(v)；如果不滿足（回傳 false），則將其轉換為 None。若原本就是 None 則維持 None。
   - 閉包簽名：FnOnce(&T) -> bool。
   - 使用時機：當你只想保留符合條件的資料時。

   ```rust
   let age: Option<i32> = Some(20);

   // 檢查是否大於等於 18 歲
   let adult = age.filter(|&a| a >= 18); // Some(20)

   let kid: Option<i32> = Some(12);
   let not_adult = kid.filter(|&a| a >= 18); // None (不符合條件被剔除)
   ```

- 實務鏈式呼叫（Chaining）完整範例

```rust
fn parse_user_id(raw_input: Option<&str>) -> u64 {
    raw_input
        .map(|s| s.trim())                         // 1. 去除空白: " 42 " -> "42"
        .filter(|s| !s.is_empty())                 // 2. 確定不是空字串
        .and_then(|s| s.parse::<u64>().ok())       // 3. 解析成數字 (解析失敗會回傳 None)
        .filter(|&id| id > 0)                      // 4. 確保 ID > 0
        .unwrap_or(0)                              // 5. 若過程有任何一步是 None，預設給 0
}

fn main() {
    // 成功案例
    assert_eq!(parse_user_id(Some("  42  ")), 42);

    // 失敗案例：非數字 -> Parse 失敗變 None -> 最後拿 0
    assert_eq!(parse_user_id(Some(" invalid ")), 0);

    // 失敗案例：不符合大於 0 條件 -> Filter 變 None -> 最後拿 0
    assert_eq!(parse_user_id(Some("0")), 0);

    // 失敗案例：原本就是 None -> 直接拿 0
    assert_eq!(parse_user_id(None), 0);

    println!("所有測試皆通過！寫法簡潔且完全無痛處理空值。");
}
```

    1. 假設我們在開發一個使用者系統，流程為：
    2. 取得輸入（Option<&str>）。
    3. 去除前後空白（.map()）。
    4. 過濾空字串（.filter()）。
    5. 解析成數字 ID（.and_then()，因為解析文字有可能失敗）。
    6. 過濾出合法 ID（.filter()，ID 必須大於 0）。
    7. 提供預設後備方案（.unwrap_or()）。

- 組合子速查對照表

| 方法                | 傳入閉包的回傳值 | 結果型別  | 核心用途                                   |
| ------------------- | ---------------- | --------- | ------------------------------------------ |
| .map(f)             | U                | Option<U> | 資料轉換（不可能失敗的操作）               |
| .and_then(f)        | Option<U>        | Option<U> | 鏈式轉換（下一步操作也可能失敗/回傳 None） |
| .filter(p)          | bool             | Option<T> | 條件篩選（不合條件變 None）                |
| .unwrap_or(default) | (非閉包)         | T         | 終結鏈式（拿值，遇到 None 給預設值）       |

### 高階組合子

除了基礎的 .map() 與 .and_then() 之外，Rust 的 Option 還提供了一系列針對多重包裹處理、備案回溯與組合運算的高階組合子。

這些組合子能讓你完全免去寫 match 的繁瑣，繼續保持宣告式（Declarative）的鏈式風格。

1. .flatten()：去除多餘的包裹層（扁平化）
   - 作用：當你遇到 Option<Option<T>>（嵌套包裹）時，.flatten() 可以將它「拆開一層」，直接壓平成 Option<T>。
   - 運算規則：
     - Some(Some(v)) $\rightarrow$ Some(v)
     - Some(None) $\rightarrow$ None
     - None $\rightarrow$ None

   ```rust
   let nested: Option<Option<i32>> = Some(Some(10));
   let flattened: Option<i32> = nested.flatten(); // Some(10)

   let nested_none: Option<Option<i32>> = Some(None);
   let flattened_none: Option<i32> = nested_none.flatten(); // None
   ```

   💡 Tip：opt.map(f).flatten() 的效果完全等同於 opt.and_then(f)！

2. .or_else()：惰性後備備案（Fallback Chaining）
   - 作用：與 .unwrap_or_else() 不同，.unwrap_or_else() 會直接解包取出裡面的值 T（終結鏈式呼叫）；而 .or_else() 回傳的依然是 Option<T>，允許你繼續進行後續的 Option 鏈式操作。
   - 閉包簽名：FnOnce() -> Option<T>（惰性求值：只有在前面的 Option 是 None 時才會執行閉包）。
   - 使用時機：當第一步沒拿到資料時，試著執行第二個「也可能失敗/回傳 None 的備案操作」（如：先查快取 $\rightarrow$ 沒拿到再查資料庫 $\rightarrow$ 沒拿到再查遠端 API）。

   ```rust
   fn fetch_from_cache() -> Option<String> { None }
   fn fetch_from_db() -> Option<String> { Some(String::from("資料庫資料")) }
   fn fetch_from_api() -> Option<String> { Some(String::from("API資料")) }

   fn main() {
       let data = fetch_from_cache()
           .or_else(|| fetch_from_db())  // 快取是 None，執行查 DB -> 成功拿到 Some
           .or_else(|| fetch_from_api()) // 前一步成功了，API 這行會直接跳過（惰性）
           .unwrap_or_else(|| String::from("預設預備資料"));

       println!("{data}"); // 輸出："資料庫資料"
   }
   ```

3. .zip()：將兩個 Option 打包成配對 Tuple
   - 作用：將 Option<T> 與另一個 Option<U> 結合。只有當兩者都是 Some 時，才會回傳包含配對的 Option<(T, U)>；只要其中一個是 None，結果就是 None。
   - 使用時機：需要同時擁有兩個獨立的 Optional 資料才能進行下一步運算時（例如：必須同時有 firstName 與 lastName 才能組合出全名）。

   ```rust
   let first_name: Option<&str> = Some("John");
   let last_name: Option<&str> = Some("Doe");

   // 兩者皆為 Some，組合為 Option<(&str, &str)>
   let full_name = first_name.zip(last_name).map(|(f, l)| format!("{f} {l}"));
   println!("{:?}", full_name); // Some("John Doe")

   // 只要其中一個是 None
   let middle_name: Option<&str> = None;
   let bad_name = first_name.zip(middle_name); // None
   ```

4. .zip_with()：延伸進階
   - 作用：zip 的進階版。它在完成配對的同時，直接傳入一個閉包將兩者合成新值，不需要再額外接 .map()。

   ```rust
   let x: Option<i32> = Some(10);
   let y: Option<i32> = Some(20);

   // 自動相加，回傳 Option<i32>
   let sum = x.zip_with(y, |a, b| a + b); // Some(30)
   ```

- 高階組合子綜合對照表

| 方法                  | 傳入參數 / 閉包              | 回傳型別       | 核心用途                                           |
| --------------------- | ---------------------------- | -------------- | -------------------------------------------------- |
| .flatten()            | 無                           | Option<T>      | 消除多餘包裹：Option<Option<T>> → Option<T>        |
| .or_else(f)           | FnOnce() -> Option<T>        | Option<T>      | 多級備案：前一步是 None 才執行下一次可能失敗的嘗試 |
| .zip(other)           | Option<U>                    | Option<(T, U)> | 雙值配對：兩者皆為 Some 才打包，否則回傳 None      |
| ".zip_with(other, f)" | Option<U>, FnOnce(T, U) -> R | Option<R>      | 配對並直接運算：結合配對與 .map() 的一步到位寫法   |

---

## Result

在 Rust 中，Result<T, E> 是專門用來處理「可能失敗的操作」的核心列舉（enum）。

Rust 沒有傳統語言的 try-catch 例外機制（Exception），所有包含檔案 IO、網路請求、字串轉型等可能出錯的操作，一律回傳 Result。這樣能強迫呼叫者在編譯期就必須面對並處理錯誤。

一、 Result<T, E> 的底層定義

```rust
pub enum Result<T, E> {
    Ok(T),  // 成功：包裹成功的結果資料 T
    Err(E), // 失敗：包裹失敗的錯誤原因 E
}
```

- T：代表操作成功時回傳的資料型別。
- E：代表操作失敗時回傳的錯誤型別。
- 同樣不需要寫 Result:: 前綴，直接使用 Ok 與 Err 即可。

二、 處理 Result 的 4 種常用方式

1. 使用 match（完整窮舉處理）

當需要針對成功與失敗分別執行複雜邏輯時使用。

```rust
fn divide(numerator: f64, denominator: f64) -> Result<f64, String> {
    if denominator == 0.0 {
        Err(String::from("除數不能為零"))
    } else {
        Ok(numerator / denominator)
    }
}

fn main() {
    match divide(10.0, 2.0) {
        Ok(result) => println!("計算結果：{result}"),
        Err(e) => println!("計算失敗：{e}"),
    }
}
```

2. 使用問號運算子 ?（最推薦、最慣用的錯誤傳播方式）

當你在寫一個函數，內部呼叫了可能會失敗的操作，且希望「若失敗就直接提前 return 錯誤，若成功就解包繼續執行」時，使用 ? 是 Rust 最精緻的語法糖。

```rust
use std::num::ParseIntError;

// 將兩個字串轉為數字並相加
fn add_str_numbers(a: &str, b: &str) -> Result<i32, ParseIntError> {
    // 若 parse() 成功，? 會自動解包拿到 i32；若失敗，會立刻從函數提前 return 出 Err
    let num_a: i32 = a.parse()?;
    let num_b: i32 = b.parse()?;

    Ok(num_a + num_b)
}

fn main() {
    match add_str_numbers("10", "20") {
        Ok(sum) => println!("總和：{sum}"), // 30
        Err(e) => println!("解析錯誤：{e}"),
    }
}
```

3. 提供備案與解包（.unwrap_or() / .unwrap_or_else()）

如果不關心具體錯在哪裡，只想在失敗時給出後備數值：

```rust
let input = "abc";

// 解析失敗時，直接提供預設值 0
let num: i32 = input.parse().unwrap_or(0);
println!("數字：{num}"); // 0
```

4. 使用 if let（只關心成功或失敗其中一種）

```rust
let result: Result<i32, &str> = Ok(200);

if let Ok(code) = result {
    println!("狀態碼為：{code}");
}
```

三、 實務綜合範例：讀取檔案並解析資料

以下展示真實專案中，結合 Result 與 ? 運算子鏈式處理檔案讀取與解析的完整流程：

```rust
use std::fs::File;
use std::io::{self, Read};

// 讀取檔案內容並轉為整數
fn read_number_from_file(path: &str) -> Result<i32, String> {
    // 1. 嘗試打開檔案（將 io::Error 轉為 String）
    let mut file = File::open(path).map_err(|e| format!("無法開啟檔案: {e}"))?;

    // 2. 嘗試讀取檔案內容
    let mut content = String::new();
    file.read_to_string(&mut content)
        .map_err(|e| format!("讀取檔案失敗: {e}"))?;

    // 3. 嘗試解析成數字
    let number: i32 = content
        .trim()
        .parse()
        .map_err(|e| format!("數字解析失敗: {e}"))?;

    Ok(number)
}

fn main() {
    match read_number_from_file("config.txt") {
        Ok(num) => println!("成功取得設定值：{num}"),
        Err(err_msg) => println!("程序執行錯誤：{err_msg}"),
    }
}
```

四、 Option 與 Result 快速對照

| 特性     | Option<T>                         | "Result<T, E>"                  |
| -------- | --------------------------------- | ------------------------------- |
| 核心意義 | 代表資料 **「存在」或「不存在」** | 代表操作 **「成功」或「失敗」** |
| 變體內容 | Some(T) / None                    | Ok(T) / Err(E)                  |
| 失敗資訊 | None 不帶任何理由                 | Err(E) 帶有具體的錯誤原因       |
| 轉換方法 | .ok_or(err) → 轉成 Result         | .ok() → 轉成 Option             |
