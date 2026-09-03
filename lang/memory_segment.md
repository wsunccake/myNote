# Memory Segment

```
+---------------------------------------+ High Address
| Environment Variables & Cmd Args      | <-- envp, argv
+---------------------------------------+
|                 STACK                 |
|                  | (Grows Downward)   | <-- Local variables, function parameters
|                  v                    |
|                                       |
|                  ^                    |
|                  | (Grows Upward)     | <-- Dynamic allocation (malloc / new)
|                 HEAP                  |
+---------------------------------------+
|                 BSS                   | <-- Uninitialized global & static variables (Zeroed by OS)
+---------------------------------------+
|                 DATA                  | <-- Initialized global & static variables (Read-Write)
+---------------------------------------+
|              TEXT / CODE              | <-- Binary instructions, literal constants (Read-Only)
+---------------------------------------+ Low Address
```

- High Address / Low Address： 高位址 / 低位址。
- Environment Variables & Command Line Arguments： 環境變數與命令列參數。
- Grows Downward / Grows Upward： 向低位址延伸（向下增長）/ 向高位址延伸（向上增長）。
- STACK Segment： 堆疊段，存放 Local Variables（區域變數）與 Function Calls / Stack Frames（函式呼叫框架）。
- HEAP Segment： 堆積段，負責 Dynamic Allocation / Runtime Allocation（執行期動態配置）。
- BSS Segment (Block Started by Symbol)： 未初始化的全域與靜態變數區，由作業系統自動清零（Automatically zero-initialized by the OS）。
- DATA Segment (Initialized Data Segment)： 已初始化的全域與靜態變數區，具備可讀寫屬性（Read-Write）。
- TEXT Segment / CODE Segment： 程式碼與唯讀常數區，具備唯讀屬性（Read-Only）以防止指令被惡意篡改。

```
+----------------------------------------+  High Address
| Stack Segment   (區域變數 / 函數參數)     |  ↓ 向低位址成長
+----------------------------------------+
| Heap Segment    (動態記憶體 alloc / Box) |  ↑ 向高位址成長
+----------------------------------------+
| BSS Segment     (未初始化/全零全域資料)   |  可讀寫 RW (無 binary 實體體積)
+----------------------------------------+
| Data Segment    (有初始值的全域/static)   |  可讀寫 RW
+----------------------------------------+
| ROData Segment  (字串字面量/不可變static)|  唯讀 R
+----------------------------------------+
| Text Segment    (機器碼指令 / Code)     |  唯讀/可執行 RX
+----------------------------------------+  Low Address
```

- Heap / Stack：執行期才根據需求動態配置與釋放的記憶體。
- BSS Segment：開局不用預給值（或預設皆為 0）的全域變數。
- Data Segment：開局就有初始值的可變全域變數。
- ROData Segment：絕對不能被修改的唯讀常數與字串。
- Text Segment：CPU 執行的機器碼指令。

---

## Compiler Language

### C

在 C 語言中，寫程式的過程基本上就是一場「精準調度這五大記憶體割區（Segments）」的遊戲。以下為你整理 C 語言在實際開發時，什麼情境、寫了什麼關鍵字或語法，會用到哪一個記憶體片段：

1. TEXT Segment (Code Segment) — 程式指令與唯讀區

希望資料「絕對不能被修改」，或是程式要執行「邏輯運算」時，就是這個區域登場的時候。

- 寫死在程式裡的字串（String Literals）：

```c
char *str = "Hello World"; // "Hello World" 存在 TEXT 段
```

> **注意：** `str` 這個指標本身在 Stack，但指向的字串在 TEXT 段。如果你嘗試執行 `str[0] = 'X';`，系統會直接拋出 `Segmentation Fault` 崩潰，因為 TEXT 段是唯讀的（Read-Only）。
> 所有的函式主體與邏輯指令： 你寫的 if-else、for 迴圈、運算式，編譯後的二進位機器碼全部躺在這裡，等待 CPU 來讀取執行。

2. DATA Segment — 已初始化的全域維度

需要一個變數「活得跟程式一樣長」，而且「一開機就必須有特定的非零數值」。

- 系統預設的配置或全域狀態（帶初值）：

```C
int g_status_code = 200; // 成功狀態碼，存在 DATA 段
```

- 跨函式共享且需要記住上次狀態的區域變數：

```C
void count_calls() {
    static int call_count = 1; // 存在 DATA 段！
    printf("Called %d times\n", call_count++);
}
```

即使 count_calls 結束了，call_count 依然存在 DATA 段不會消失，下次進來會繼續累加。

3. BSS Segment — 未初始化的全域緩衝區

需要「超大空間的全域變數或陣列」，但「不需要給特別的初值（希望預設是 0）」。這就是我們前面提到，為了節省硬碟空間的「偷吃步」割區。

- 大型全域緩衝區（Buffers）： 例如自動化測試時用來接收封包、讀取 Log 的大陣列。

```C
char g_network_buffer[1024 * 1024]; // 1MB 的大快取，存在 BSS 段
```

寫在硬碟裡不佔空間，程式一啟動，作業系統會自動把它們全部刷成 0 (NULL)。

- 未初始化的全域/靜態變數：

```C
int g_total_devices; // 預設為 0，存在 BSS 段
```

4. HEAP Segment — 執行期的動態外包區

寫程式時，「無法預知資料會有多大」，或是需要「控制這個資料什麼時候死掉」。

- 動態決定大小的陣列（Scaling / Flexibility）： 比如寫自動化測試或 Scaling Test 時，設備數量（n）是由設定檔或使用者輸入決定的，沒辦法寫死。

```C
int n;
scanf("%d", &n); // 執行時才知道 n 是多少
int *device_list = (int *)malloc(n * sizeof(int)); // 存在 HEAP 段
```

- 跨函式傳遞大型結構體（過橋不死）： 在函式 A 裡面建立一個結構體，希望函式 A 結束後，這個結構體不要被銷毀，還能回傳給主程式繼續用。

```C
struct Node* create_node(int data) {
    struct Node *new_node = (struct Node*)malloc(sizeof(struct Node)); // HEAP
    new_node->data = data;
    return new_node; // 函式結束了，但 HEAP 記憶體還活著
}
```

代價： 用完必須手動呼叫 free(device_list)，否則就會 Memory Leak。

5. STACK Segment — 函式執行的工作檯

需要「快速、短暫、用完即丟」的變數，這是 C 語言最常被轟炸、也最頻繁使用的割區。

- 一般的區域變數（Local Variables）： 在函式或 {} 大括號裡面宣告的所有普通變數。

```C
void calculate() {
    int x = 10;    // STACK
    float y = 5.5; // STACK
} // 執行到這裡，x 和 y 瞬間在 STACK 釋放消失
```

- 函式的參數傳遞（Arguments）： 呼叫函式時傳進去的內容。

```C
void inspect_mac(char *mac) { ... } // mac 指標變數本身存在 STACK
```

函式呼叫的軌跡追蹤（Return Address）： 程式執行 A 函式，A 呼叫 B 函式。系統要把「A 執行到哪一行」的地址壓入 STACK。等 B 執行完，CPU 再從 STACK 彈出（Pop）這個地址，跳回 A 繼續跑。

| 開發需求                             | C 語言語法範例               | 佔用的記憶體割區             | 記憶體壽命 (Lifetime)  |
| ------------------------------------ | ---------------------------- | ---------------------------- | ---------------------- |
| 只是寫一串字串訊息做 Log 輸出        | "printf(""Test Failed\n"");" | TEXT                         | 永久（跟著程式死活）   |
| 設定一個全域、開機就是 1 的 Flag     | int g_flag = 1;              | DATA                         | 永久（跟著程式死活）   |
| 設定一個全域、開機預設為 0 的計數器  | int g_counter;               | BSS                          | 永久（跟著程式死活）   |
| 函式內部用完就不要的暫存計數器       | for(int i=0; ...)            | STACK                        | 短暫（離開大括號就死） |
| 執行時讀取設定檔，才知道要開多大空間 | malloc(config_size);         | HEAP,隨意（直到你呼叫 free） |

### C++

從 C 演進到 C++，雖然底層的作業系統記憶體割區（TEXT, DATA, BSS, HEAP, STACK）完全沒有變，但 C++ 引入了物件導向（OOP）、RAII（資源取得即初始化）、Lambda 以及標準函式庫（STL）。

這使得 C++ 的記憶體使用情境變得比 C 複雜且精妙得多。以下整理 C++ 在現代開發時，各個記憶體割區的經典實戰情境：

1. TEXT / CODE Segment (唯讀指令與常數區)

C++ 延伸了唯讀的概念，並在「編譯期優化」做到了極致。

- constexpr 與 consteval（編譯期常數）：

```C++
constexpr int MAX_CONNECTIONS = 1000;
```

記憶體實相： 這些變數在編譯時就被計算出結果，並直接內聯（Inline）到機器指令中。它在執行期通常不佔用任何獨立的變數記憶體空間，直接融為 TEXT 段指令的一部分。

- 虛擬函式表 (vtable - Virtual Table)：

當類別包含 virtual 關鍵字（實作多型/Polymorphism）時：

```C++
class Base { virtual void show() {} };
```

記憶體實相： 編譯器會為這個類別產生一張虛擬函式指標表（vtable），用來在執行期決定該呼叫哪個子類別的方法。這張指標表（vtable）是唯讀的，存放在 TEXT 段（有些系統會放在專屬的唯讀資料段 .rodata，本質上都屬於 TEXT 割區）。

2. DATA Segment (已初始化全域/靜態區)

- 單例模式 (Singleton Pattern) 的實體：

在 C++11 之後，這通常用來實作執行緒安全的單例。

```C++
class Database {
public:
    static Database& getInstance() {
        static Database instance; // 關鍵字 static，初始化後躺在 DATA 段
        return instance;
    }
};
```

生命週期： 第一次呼叫 getInstance() 時，instance 會在 DATA 段被建構，並且一直活到整個程式結束。

3. BSS Segment (未初始化全域/靜態區)

- 全域或類別內部的靜態計數器/快取（未給初值）：

```C++
// 某個自動化測試類別
class TestAgent {
    static int total_spawned_agents; // 類別靜態變數宣告
};
int TestAgent::total_spawned_agents; // 未給初值，留在 BSS 段（系統自動清零）
```

4. HEAP Segment (動態配置區) — C++ 的重頭戲

C++ 雖然保留了 malloc，但現代 C++（Modern C++）的操作物件基本上都活在 HEAP，並且高度依賴「智慧指標」來管理。

- 標準容器 (STL Containers) 的底層資料：

這是最常被誤解的地方。當你在函式裡宣告一個 std::vector 或 std::string：

```C++
void run_test() {
    std::vector<int> v = {1, 2, 3, 4, 5};
}
```

記憶體實相（結合 STACK 與 HEAP）：

v 這個物件本身（包含指向底層的指標、Size、Capacity，總共約 24 Bytes）是放在 STACK。

但是！{1, 2, 3, 4, 5} 這五個整數真正佔用的記憶體空間，是 std::vector 自動在內部呼叫 new 申請出來並放在 HEAP 的。當函式結束 v 離開 STACK 時，它的解構式會自動去 HEAP 執行 delete。

- 智慧指標 (Smart Pointers) 管理的動態物件：

為了防止 C 語言常見的 Memory Leak，現代 C++ 強烈建議不要直接寫 new，而是寫：

```C++
auto target_device = std::make_unique<Device>(); // Device 物件肉體在 HEAP
```

- Lambda 表達式捕捉大型物件 (Capture by Value)：

```C++
auto huge_data = get_large_matrix(); // 假設這很大
auto lam = [huge_data]() { /* 處理資料 */ };
```

如果把這個 Lambda 閉包（Closure）物件透過 std::function 丟給其他執行緒非同步執行，這個閉包體通常會被搬移到 HEAP 裡。

5. STACK Segment (函式工作檯)

C++ 的 STACK 除了放基本的區域變數，更承載了 C++ 核心設計哲學：RAII (Resource Acquisition Is Initialization)。

- 自動資源鎖 (Scoped Locks) — 執行緒安全控制：

在做高效能並發測試、多執行緒搶奪資源時：

```C++
std::mutex mtx;
void update_shared_data() {
    std::lock_guard<std::mutex> lock(mtx); // lock 變數存在 STACK
    // 開始處理共享資料...
} // 函式結束，lock 在 STACK 被彈出並銷毀，解構式自動觸發 mtx.unlock()！
```

這是 C++ 最優雅的特色。利用 STACK「離開大括號一定會被銷毀」的鐵律，來確保死鎖（Deadlock）絕對不會發生。

- 普通的類別區域物件：

```C++
MyClass obj; // 直接宣告，沒有 new。obj 完整躺在 STACK 上
```

### Rust

從 C/C++ 跨越到 Rust，記憶體的世界觀迎來了一次顛覆性的革命。

雖然作業系統底層的五大割區（TEXT, DATA, BSS, HEAP, STACK）依然穩固不變，但 Rust 徹底廢除了 C/C++ 的「手動記憶體管理」，同時也拒絕了 Java/Python 的「執行期垃圾回收（GC）」。它改用一套在編譯期（Compile-time）嚴格執行的「所有權（Ownership）與生命週期（Lifetimes）」系統，在不犧牲任何效能的情況下，把記憶體安全玩到了極致。

以下為你拆解 Rust 語言在實際開發時，各個記憶體割區的使用情境與底層實相：

1. TEXT / CODE Segment (Read-Only)

Rust 追求極致的零成本抽象（Zero-Cost Abstractions），這讓它的 TEXT 段優化變得非常瘋狂。

- const（編譯期常數）的全面內聯（Inline）：

```Rust
const MAX_RETRIES: u32 = 5;
```

記憶體實相： Rust 的 const 在編譯期會被直接替換（Inline）到所有使用它的程式碼中。它在執行期完全不佔用獨立的記憶體位址，直接融為 TEXT 段機器指令的一部分。

- 唯讀字串切片（String Literals）：

```Rust
let s: &str = "Hello Rust";
```

記憶體實相： "Hello Rust" 這段文字被硬編碼在 TEXT 段（或 .rodata 唯讀資料段）。而變數 s 是一個胖指標（Fat Pointer，包含 8 位元組位址 + 8 位元組長度），躺在 STACK 上指向 TEXT 段。

- 靜態分發的方法（Static Dispatch via Generics）：

使用泛型或 impl Trait 時，Rust 會在編譯期進行「單態化（Monomorphization）」，把泛型代碼複製並生成具體的機器碼。這些生成的函式全部整齊地排在 TEXT 段，呼叫時直接跳躍（Jump），速度極快。

2. DATA Segment / BSS Segment (Static Region)

Rust 對於全域狀態控制得極為嚴苛，因為全域變數是多執行緒資料競爭（Data Race）的溫床。

- 全域靜態配置（static）：

```Rust
static APP_VERSION: &str = "2.6.15"; // DATA 段
static mut GLOBAL_COUNTER: u64 = 0;   // BSS 段 (因為初值為 0)
```

- 安全使用全域變數的情境（如 Lazy / OnceLock）：

因為修改 static mut 是危險的，現代 Rust 常用 OnceLock 來延遲初始化全域常數。

```Rust
use std::sync::OnceLock;
static CONFIG: OnceLock<String> = OnceLock::new(); // BSS 段
```

生命週期： 它們的生命週期標記都是 'static，伴隨整個進程。

3. STACK Segment (核心防線：所有權與 RAII 的發源地)

在 Rust 中，STACK 是預設的戰場。不論是基本型態、結構體（Struct）還是列舉（Enum），只要你沒有明確指定，它們通通預設配置在 STACK 上。

- 預設的結構體與物件配置（極速）：

在 C++ 或 Java 中，物件很常一不小心就跑到 Heap。但在 Rust 裡：

```Rust
struct Device { id: u32, port: u16 }

fn process() {
    let dev = Device { id: 101, port: 8080 }; // 完整躺在 STACK 上！
} // 離開大括號，dev 瞬間在 STACK 彈出銷毀，完全不花多餘 CPU 週期
```

- 移動語意（Move Semantics）下的 STACK 資料轉移：

把一個 STACK 上的變數傳給另一個函式時，如果它沒有實作 Copy 屬性，Rust 記憶體層面會進行 Bitwise Copy（把 STACK 的記憶體塊直接複製過去），但編譯器會讓舊的變數失效。這不需要動到 Heap，效率極高。

4. HEAP Segment (動態配置：智慧指標的天下)

Rust 的 HEAP 配置非常透明。如果你需要資料在函式結束後繼續活著，或是資料大小是動態變動的，你必須明確使用 智慧指標（Smart Pointers） 或 標準容器（Collections）。

- 把物件強制塞進 Heap（Box<T>）：

需要跨函式傳遞大型結構體，又不想在 STACK 上傳遞巨大的資料塊時：

```Rust
// Device 物件肉體被 new 在 HEAP 裡
// target 變數本身只是一個指標（8 位元組），躺在 STACK 上
let target = Box::new(Device { id: 1, port: 80 });
```

- 動態增長的容器（Vec<T>, String, HashMap）：

這點跟 C++ 非常像（名在 STACK，肉在 HEAP）。

```Rust
let mut v = vec![1, 2, 3];
```

記憶體實相： v 包含（指標、Capacity、Length）共 24 位元組躺在 STACK。但當你 v.push(4) 導致容量不足時，它會自動在 HEAP 重新尋找更大的空間、把資料搬過去，並釋放舊的 HEAP 空間。

- 多執行緒共享與算改（Arc<Mutex<T>>）：

在寫多執行緒或並發架構時：

```Rust
use std::sync::{Arc, Mutex};
let shared_data = Arc::new(Mutex::new(5));
```

記憶體實相： 引用計數（Reference Count）控制塊和鎖的本體，全部存放在 HEAP。多個執行緒在各自的 STACK 拿著克隆（Clone）出來的指標，共同指向 HEAP 裡的同一塊肉。

---

## RAII

RAII 是 Resource Acquisition Is Initialization 的縮寫，中文通常翻譯為「資源取得即初始化」。這個名字取得非常抽象、甚至有點爛（連 C++ 的發明者 Bjarne Stroustrup 自己都說過這個名字取得不夠好），但它卻是 C++ 和 Rust 能在「不使用垃圾回收器（GC）」的情況下，做到記憶體與資源絕對安全的最高核心哲學。簡單來說，RAII 的核心思想就是：「把『資源』的生命週期，死死地跟『 Stack 變數』的生命週期綁在一起。」

### 傳統 C 語言的痛點

在沒有 RAII 的時代（例如 C 語言），向系統借了資源（記憶體、檔案、資料庫連線、執行緒鎖），必須手動還錢。這會導致程式碼充滿危機。

```C
void process_file() {
    FILE *f = fopen("test.log", "r"); // 1. 取得資源 (打開檔案)

    int *buffer = (int *)malloc(1000); // 2. 取得資源 (記憶體)

    if (read_data(f, buffer) == -1) {
        // ❌ 慘劇 1：如果讀取失敗，提早 return，忘記 free 和 fclose
        // 導致 Memory Leak 與 File Descriptor 洩漏！
        return;
    }

    if (validate_data(buffer) == false) {
        free(buffer);
        // ❌ 慘劇 2：忘記寫 fclose(f)，檔案依然被鎖死
        return;
    }

    free(buffer);  // 正常釋放
    fclose(f);     // 正常關閉
}
```

在實際開發中，函式只要一長、邏輯一多（各種 if-else、拋出異常 exception、提早 return），工程師就極度容易忘記在每個出口手動釋放資源，導致系統慢性中毒崩潰。

### RAII 的運作機制

RAII 利用了硬體與作業系統的一個鐵律：「放在 STACK 割區的區域變數，只要離開大括號 {}（生命週期結束），系統絕對會瞬間把這塊 Stack 彈出並銷毀。」

RAII 的具體作法是，用一個物件（Object）把資源包起來：

1. 初始化（建構式 Constructor）： 當物件在 Stack 上被建立時，它會自動去申請資源（例如 malloc 或打開檔案）。
2. 銷毀（解構式 Destructor）： 當物件離開大括號、從 Stack 被彈出銷毀時，系統會自動呼叫它的解構式。我們把「釋放資源」的代碼寫在解構式裡。

### C++ 中的 RAII 經典實戰

C++ 是 RAII 的發源地。現代 C++ 幾乎看不到 new / delete 或 malloc / free，全部改用 RAII 類別。

- 管理 HEAP 記憶體（智慧指標）

```C++
#include <memory>

void memory_example() {
    // std::unique_ptr 是一個區域物件，躺在 STACK 上
    // 它在建構時，悄悄在 HEAP 申請了 Device 的記憶體
    std::unique_ptr<Device> dev = std::make_unique<Device>();

    if (test_failed) {
        return; // 🌟 提早離開！
    }
    // 不管是提早 return 還是正常結束，只要離開這個大括號，
    // dev (STACK) 被銷毀，就會自動觸發解構式，把 HEAP 裡的 Device 自動 delete！
}
```

- 管理執行緒鎖（執行緒安全）

```C++
#include <mutex>
std::mutex mtx;

void safe_print() {
    // 建構式自動觸發 mtx.lock()
    std::lock_guard<std::mutex> lock(mtx);

    // 執行一堆複雜的測試邏輯
    if (critical_error) {
        throw std::runtime_error("Crash!"); // 🌟 即使噴出異常、程式中斷
    }
} // 🌟 離開大括號的瞬間，lock 變數被彈出 STACK，解構式自動觸發 mtx.unlock()！
```

### Rust 中的 RAII

Rust 沒有建構式/解構式的名詞，但它把 RAII 發揚光大，融入了核心的所有權（Ownership）系統，並透過 Drop 特性（Trait）來實作。

```Rust
use std::fs::File;

fn rust_raii() {
    {
        let f = File::open("debug.txt").unwrap(); // 取得檔案資源
        // 處理檔案...
    } // 🌟 這裡大括號結束，f 的所有權到期，Rust 編譯器在編譯時
      // 就會在這裡自動插入 `drop(f)` 的機器碼，檔案自動安全關閉。
}
```

### 其他語言沒有 RAII 怎麼辦

不是每個語言都支援 RAII。支援 RAII 的前提是：語言必須允許物件在 Stack 上建立，且在離開 Scope 時能立刻觸發特定代碼。像 Java、Python 這種「萬物皆在 Heap」的語言，無法使用標準的 RAII，所以它們演進出了類似的補償機制：

- Python 的做法 (with 語法 / 上下文管理器)：

```Python
with open("test.txt", "r") as f:
    data = f.read()
# 離開 with 區塊時，Python 會自動呼叫 f.close()
```

- Java 的做法 (try-with-resources)：

```Java
try (BufferedReader br = new BufferedReader(new FileReader("test.txt"))) {
    return br.readLine();
} // 離開 try 區塊時，自動呼叫 br.close()
```

---

## Hybrid Language - Java

JVM 語言（以 Java、Kotlin、Scala 為例）在分類上屬於 「混合式（Hybrid）」 或者是 「雙階段：先編譯、後直譯/即時編譯」 的語言。它不屬於純粹的編譯式（如 C/Rust），也不屬於純粹的直譯式（如 Shell）。它的運作本質非常精彩：

1. 前端編譯（Compile Time）： 你寫的 .java 原始碼，會先被 Java 編譯器（javac）編譯成一種中間格式，叫做 字節碼（Bytecode），也就是 .class 檔案。

2. 運行期執行（Runtime）： 當你執行程式時，JVM（Java 虛擬機） 登場。JVM 本身是一個用 C/C++ 寫成的巨大執行檔。它會讀取這些字節碼，並透過兩種方式執行：
   - 直譯（Interpreter）： 逐行把字節碼轉成機器碼並執行（開機快，但跑起來慢）。
   - 即時編譯（JIT Compiler - Just In Time）： 當 JVM 發現某段程式碼（例如 MAC Address 計算的迴圈）被反覆執行很多次，它會啟動 JIT，在執行過程中直接把這段字節碼編譯成硬體專屬的純機器碼，然後直接丟給 CPU 跑（越跑越快）。

JVM 語言的記憶體五段分配（底層實相）

當 JVM 語言執行時，作業系統看見的進程（Process）其實是 java（JVM 本身）。因此，這五大割區（TEXT, DATA, BSS, HEAP, STACK）裡面裝的，全部都是 JVM 為了伺候你的 Java 程式所規劃的內部架構。

JVM 在這五大割區上，蓋了一座屬於自己的記憶體大樓（我們常聽到的 JVM Memory Area）：

```
+-------------------------------------------------------------+ High Address
|                STACK (作業系統核心/Thread Stack)              |
|  [JVM Stack Frame] <-- 每個 Thread 專屬，放局部變數(指標/基本型態)|
+-------------------------------------------------------------+
|                HEAP (虛擬機全域堆積)                          |
|  [Java Objects Region] <-- 🌟 所有 new 出來的物件肉體都擠在這裡  |
+-------------------------------------------------------------+
|                BSS / DATA / TEXT (JVM 自身的割區)            |
|  [Metaspace / Method Area] <-- 放載入的 Class 資訊、static 指標|
|  [JIT Native Code] <-- JIT 即時編譯出來的超快純機器碼指令        |
+-------------------------------------------------------------+ Low Address
```

1. TEXT Segment (程式碼與常數區)

在 JVM 世界中，這個割區主要用來放 JVM 核心的 C++ 機器碼，以及 JIT 編譯出來的極速機器碼。

    - JVM 存放內容：
        - 當 JIT（即時編譯器）發現 Java 程式碼效能需求很高，把字節碼直接編譯成物理 CPU 指令時，這些指令就會被安置在 TEXT 段附近（JVM 內部稱為 Code Cache）。
        - 程式裡寫死的常數字串，會被載入到 JVM 的「字串常數池（String Constant Pool）」中，底層也是唯讀的資料區。

2. DATA / BSS Segment (靜態全域區)

JVM 在這裡劃分了一塊非常有名的虛擬割區，叫做 Method Area（方法區，在 Java 8 之後由 Metaspace 實作）。

    - Java 語法情境： static 關鍵字。
    - JVM 存放內容： 当一個 .class 檔案被載入時，它的結構資訊（有哪些 Method、有哪些欄位）以及 static 變數的「引用指標（Reference/Pointer）」 或者是基本型態數值，通通存在這裡。
    - 底層實相： 這裡的記憶體生命週期跟著 ClassLoader 一起死活，基本上也是程式不關就不會釋放。

3. HEAP Segment (堆積區)

JVM 的絕對主力戰場

    - Java 著名的口號是：「萬物皆物件」，這意味著 Java 的 HEAP 負擔極重。
    - Java 語法情境： 只要你寫了 new。
    - JVM 存放內容： 所有物件的「肉體實體」通通在 HEAP。

```java
static Person manager = new Person();
```

這行程式碼在 JVM 底層的物理割區分佈是：

- `manager` 這個名字（指標，4 或 8 位元組），躺在 **DATA/Method Area** 割區。
- `new Person()` 真正的物件肉體（裡面包含他的姓名、年齡等資料），實實在在地躺在 **HEAP** 割區。
  特點： JVM 擁有全世界最複雜、最精密的 GC（垃圾回收器）。它會把 HEAP 切成伊甸園（Eden）、倖存區（Survivor）和老年代（Old Generation），專職在這裡掃描並回收沒人要的物件肉體。

4. STACK Segment (堆疊區)

每個執行緒（Thread）在啟動時，作業系統都會配給它一個獨立的 STACK。

- Java 語法情境： 函式內的區域變數、傳入參數。
- JVM 存放內容： \* 基本型態（Primitive Types）： 如果你寫 int x = 10;，這個 10 會直接以二進位數值躺在 STACK 裡，速度極快。
- 物件引用（Object Reference）： 如果 Person p = new Person();，這個 p 只是個記憶體地址（指標），它躺在 STACK 上，指向 HEAP 裡面的肉體。

### JVM 語言的記憶體特性

JVM 語言透過「名在 Metaspace/Stack，肉在 Heap」的混合操作，創造了高度的安全感：
永遠碰不到物理記憶體地址： 在 STACK 拿到的 p 雖然是指標，但 JVM 嚴格禁止你像 C 語言那樣對指標做加減法（例如 p++ 在 Java 是行不通的），這徹底杜絕了記憶體被破壞的風險。
效能的代價在 HEAP： 因為連 Integer、String、List 預設都是物件、都得去 HEAP 蹲著，所以 Java 的 new 和 GC 頻率遠高於 C/C++/Rust，這也是為什麼早期 Java 被嫌慢、耗記憶體的主因。不過現代 JVM 靠著極度強大的 JIT 編譯優化，在多數商業場景下，效能已經逼近編譯式語言了。

---

## Interpreted Language - Python

執行一個 Python 程式時，作業系統（OS）看到的進程（Process）其實是 Python 直譯器本身（最常用的官方版本是 CPython，它是用 C 語言寫成的）。
因此，作業系統配給進程的物理五大割區（TEXT, DATA, BSS, HEAP, STACK），裡面裝的全部都是 CPython 直譯器自己的代碼與狀態。而你寫的 Python 程式、變數和物件，全部都被 CPython 當成「資料」，強行塞進了它的 HEAP（堆積區）裡。

1. HEAP Segment

在 Python 的世界裡，有一句核心名言：「萬物皆物件（Everything is an Object）」。不論是整數、字串、函式、類別，甚至是編譯後的字節碼（Bytecode），通通都是活在 HEAP 裡的 C 語言結構體（PyObject）。

- 一般的變數與常數

```Python
# 在 Python 裡，這不是單純的 100，而是一個肥大的整數物件
x = 100
PI = 3.14159
```

底層實相： CPython 會在 HEAP 申請一塊記憶體，建立一個 PyLongObject 結構體（約 28 萬位元組），裡面記錄了型態、引用計數（Reference Count）和數值 100。
變數 x 本身只是一個「標籤（指標）」，它指著 HEAP 裡的那個 100。

- 類別變數與靜態屬性
```Python
class TestAgent:
    total_count = 0  # 類別變數（等同於其他語言的 static）
```
底層實相： 當 Python 讀到類別定義時，它會在 HEAP 裡建立一個「類別物件」。這個類別物件內部有一個字典（__dict__）。你寫的 total_count 只是這個字典裡的一個 Key-Value 鍵值對，完全躺在 HEAP 裡。

- 常數優化區

Python 雖然沒有 const 關鍵字，但它會在 HEAP 裡為每個模塊建立一個 Code Object。寫死在程式裡的字串或小數字（例如 -5 到 256 之間的整數），Python 會在 HEAP 裡開闢一塊快取區（Integer Cache / Interned Strings）讓它們重複使用，避免重複 new 造成效能低下。

2. STACK Segment

Python 每個執行緒也擁有作業系統配給的 STACK，但 Python 的 STACK 非常「輕量化」。

使用情境： 函式呼叫、區域變數。

底層實相： 

```python
def calculate():
    local_val = "hello"
```

呼叫 `calculate()` 時，Python 會在作業系統的 STACK 壓入一個 Frame。**但是，這個 Frame 裡面絕對不放 "hello" 這串文字的肉體。**
* `"hello"` 的肉體依然被 new 在 **HEAP** 裡。
* **STACK 裡面只放一個 8 位元組的記憶體指標**，指向 HEAP 的位址。

這就是 Python 為什麼不容易噴 Stack Overflow（除非無窮遞迴），但也為什麼比較慢的原因——因為每次存取變數，CPU 都必須從 STACK 的指標「右轉」去 HEAP 撈資料。

3. TEXT / DATA / BSS Segment

這三個割區跟你的 Python 程式碼內容沒有直接關係，它們是 CPython 直譯器（/usr/bin/python3 執行檔）的物理割區。

- TEXT Segment： 存放的是 Python 直譯器核心的 C 語言二進位指令（例如負責垃圾回收的代碼、負責解析 def / if 的邏輯）。
- DATA / BSS Segment： 存放的是 Python 直譯器內部的全域狀態配置、內建模組的初始狀態等。