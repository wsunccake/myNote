# Functional Programming

`Functional Programming`（ 簡稱 `FP`, 函數式編程 ）是一種 Programming Paradigm（ 編程範式 ），它將電腦運算視為 數學函數 的計算，並且極力避免 `改變狀態` 與 `使用可變數據`。
在現代軟體開發中，`FP` 是解決併發處理、系統複雜度與代碼可維護性的核心工具。

---

## 演進過程與歷史 (History)

`Functional Programming`

- 1930年代：`λ` 演算 (Lambda Calculus)
  數學家 Alonzo Church 提出了 `λ` 演算，這成了 `FP` 的理論基石。它證明了僅用函數定義就能表達所有可計算函數。

- 1950年代：`LISP`
  John McCarthy 在 MIT 發明了 `LISP`，這是第一種體現 `λ` 演算思想的程式語言，引入了遞迴與符號處理。

- 1970-80年代：強型別 `FP` 的崛起
  `ML` (Meta Language) 與隨後的 `Haskell` 出現，引入了強大的靜型別系統與「懶惰求值 (Lazy Evaluation)」概念。

- 2000年代至今：混合式範式 (Multi-paradigm)
  `FP` 的概念開始大規模滲入主流語言。`Java 8` 引入 `Lambda`，`Python` 的 decorator 與 `map`/`filter`，以及 `JavaScript` (`ES6+`) 對 `FP` 的全面擁抱。

---

## 概念 (Conpcet)

`FP` 的世界觀與傳統的 `Imperative Programming`（ 命令式編程 ）截然不同：

- **純函數 (Pure Functions)**： 給定相同的輸入，永遠得到相同的輸出，且不會產生「副作用」（如修改全域變數、寫入資料庫）。
- **不可變性 (Immutability)**： 數據一旦創建就不能修改。若要改變，則是創建一份包含新值的新數據。
- **一等公民與高階函數 (First-class & Higher-order Functions)**： 函數可以像變數一樣被傳遞、作為參數或作為回傳值。
- **宣告式 (Declarative) 而非命令式 (Imperative)**： 關注「要做什麼 (What to do)」而非「怎麼做 (How to do)」。例如使用 map 處理陣列，而不是寫 for 迴圈。

---

## 準則與規範 (Principles)

1. 數據與邏輯分離 (Separation of Data and Logic)
   在 `OO`（物件導向）中，數據與方法封裝在一起。而在 `FP` 中，數據只是單純的結構（如 Map 或 Record），函數則是獨立的轉換邏輯。
   - 準則： 保持數據結構簡單透明，邏輯則以純函數形式存在。

2. 避免共享狀態 (No Shared State)
   共享狀態會導致函數的輸出變得不可預測（依賴於誰先修改了變數）。
   - 規範： 函數內的所有資訊都應來自其輸入參數，嚴禁讀取或修改外部作用域的變數。

3. 宣告式轉換 (Declarative Data Transformations)
   當需要處理集合（Arrays/Lists）時，永遠優先考慮以下「三大將」：
   - Map： 1 對 1 轉換（如：將清單中所有數字平方）。
   - Filter： 篩選符合條件的元素。
   - Reduce： 將集合歸納為單一數值（如：總和、格式轉換）。

4. 顯性化 (Explicitness)
   函數不應有「隱藏的輸入」或「隱藏的輸出」。
   - 規範： 如果一個函數可能失敗，回傳值應顯式地包含錯誤狀態（例如回傳 Result<T, E>），而不是直接拋出 Exception 讓程式中斷。

---

## 實踐方法

1. 管道化與組合 (Pipelining & Composition)
   不要寫嵌套層層的函數呼叫（如 fn3(fn2(fn1(x)))），應將邏輯拆解為小的單一功能函數，再串接起來。
   - 技巧： 使用 compose（由右往左）或 pipe（由左往右）。
   - 效果： 程式碼讀起來像是一條流水線。

2. 柯里化 (Currying) 與 部份應用 (Partial Application)
   將一個多參數函數轉化為一系列單參數函數的過程。
   - 技巧： 預先填入部分參數，產生一個功能更專一的新函數。
   - 例子： 一個 add(x, y) 可以變成 add5 = add(5)，之後只需調用 add5(10)。

3. 遞迴代替迴圈 (Recursion over Loops)
   `FP` 傾向於不使用 `for` 或 `while`，因為這些語法依賴於狀態的變更（如計數器 i++）。
   - 技巧： 使用遞迴處理重複性邏輯。
   - 注意： 確保語言支援 尾調用優化 (Tail Call Optimization)，否則應改用內建的高階函數（如 reduce）。

4. 封裝副作用 (Functors & Monads)
   處理 I/O、錯誤或非同步操作時，不直接在主邏輯中執行，而是將其包裝在一個「容器」中。
   - 技巧： 透過 Option (或 Maybe) 處理空值，透過 Either 處理錯誤，而不是用 try-catch 或 if(null)。

---

## 特色分析

1. 優點
   - 易於測試與除錯： 純函數不依賴外部環境，單元測試極其簡單。
   - 併發處理優勢： 因為數據不可變，不需要擔心多執行緒競爭（Race Condition）或鎖（Lock）的問題。
   - 代碼精簡與復用： 透過組合（Composition）與高階函數，可以用極少的代碼完成複雜邏輯。
   - 數學正確性： 程式邏輯更趨向於數學證明，減少了因狀態錯誤導致的 bug。

2. 缺點
   - 學習曲線陡峭： 習慣了 for 迴圈與變數賦值的開發者，需要翻轉思維來理解 Monad、Currying 等概念。
   - 效能開銷： 不可變性意味著頻繁的對象創建與內存回收（GC），在極端性能要求的場景下可能不如原地修改（In-place update）。
   - 遞迴壓力： FP 依賴遞迴，若編譯器不支持尾調用優化（Tail Call Optimization），容易導致堆疊溢位（Stack Overflow）。

3. 情境
   - 並行與分散式運算： 如 Apache Spark、Erlang（電信系統）。
   - 前端開發： React 的單向數據流與 Hooks、Redux 的狀態管理深受 FP 啟發。
   - 金融與科學計算： 需要極高精確度與可驗證性的領域。
   - 大數據處理： ETL 流程中數據的轉換與過濾。
