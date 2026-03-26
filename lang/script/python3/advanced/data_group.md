# Data Group

## Comprehension

1. 列表推導式 (List Comprehension)

最常用的推導式，用於從一個可迭代對象（Iterable）快速生成一個新的 List。

- 語法結構：`[expression for item in iterable if condition]`
- 核心優點：程式碼高度壓縮，且執行效率通常比手動 `append` 快。
- 特性：立即運算並將所有結果儲存在記憶體中。
- 符號：方括號 [ ]
- 範例：生成 1 到 10 之間偶數的平方。

  ```python
  # 傳統寫法 (程序導向)
  squares = []
  for x in range(1, 11):
      if x % 2 == 0:
          squares.append(x**2)

  # 推導式寫法 (宣告式)
  squares = [x**2 for x in range(1, 11) if x % 2 == 0]
  # 結果: [4, 16, 36, 64, 100]
  ```

2. 字典推導式 (Dictionary Comprehension)

用於快速構建 Dict，特別適合用於鍵值對（Key-Value）的轉換或過濾。

- 語法結構：`{key_expr: value_expr for item in iterable if condition}`
- 使用時機：反轉字典（Swap key/value）、從兩個列表合併成字典、過濾特定 Key。
- 特性：生成 Dict (字典)，以鍵值對形式儲存。
- 符號：花括號 { }
- 範例：將名字列表轉為「名字: 長度」的字典。

  ```python
  names = ['Alice', 'Bob', 'Charlie']
  name_lengths = {name: len(name) for name in names if len(name) > 3}
  # 結果: {'Alice': 5, 'Charlie': 7}
  ```

3. 集合推導式 (Set Comprehension)

與列表推導式類似，但生成的是 Set（會自動去重且無序）。

- 語法結構：`{expression for item in iterable if condition}`
- 使用時機：需要提取唯一元素集合時。
- 特性：生成 Set (集合)，會自動去重且無序。
- 符號：花括號 { }
- 範例：從一段文字中提取所有出現過的母音。

  ```python
  text = "hello world python"
  vowels = {char for char in text if char in 'aeiou'}
  # 結果: {'o', 'e'} (順序不固定，且不會重複)
  ```

4. 生成器運算式 (Generator Expression)

雖然語法非常像「元組推導式（Tuple Comprehension）」，但 Python 實際上並沒有 Tuple Comprehension。括號 () 生成的是一個 Generator 物件。

- 語法結構：`(expression for item in iterable if condition)`
- 核心特色：惰性求值（Lazy Evaluation）。它不會立即在記憶體中建立整個列表，而是在需要時才「產出」下一個值。
- 使用時機：處理海量數據（如數百萬筆 Log）時，為了節省內存必用。
- 符號：圓括號 ( )
- 範例：計算一億個數字的平方和。

  ```python
  # 不會一次佔用大量 RAM，而是邊算邊加
  total_sum = sum(x**2 for x in range(1000000))
  ```

| 類型      | 括號符號 | 返回類型  | 記憶體占用        | 特點                     |
| --------- | -------- | --------- | ----------------- | ------------------------ |
| List      | [ ]      | list      | 較高 (一次性生成) | 最通用，支援索引存取。   |
| Dict      | { : }    | dict      | 中                | 鍵值對映射。             |
| Set       | { }      | set       | 中                | 自動去重。               |
| Generator | ( )      | generator | 極低 (隨用隨取)   | 效能優化利器，不可索引。 |

---

## Nested Comprehension

1. 邏輯拆解：由內而外 vs 由左而右

二維矩陣（Matrix）攤平成一維列表（Flat List）

```python
matrix = [[1, 2, 3], [4, 5, 6]]

# nested loop
flat = []
for row in matrix:           # 1. 外層迴圈
    for item in row:         # 2. 內層迴圈
        flat.append(item)    # 3. 執行動作

# nested comprehension
# [ 執行動作 | 外層迴圈 | 內層迴圈 ]
flat = [item for row in matrix for item in row]
```

2. 進階應用：加入條件判斷

提取矩陣中的偶數

```python
matrix = [[1, 2, 3], [4, 5, 6]]

# nested loop
even_nums = []
for row in matrix:
    for item in row:
        if item % 2 == 0:
            even_nums.append(item)

# nested comprehension
even_nums = [item for row in matrix for item in row if item % 2 == 0]
```

3. 建立巢狀結構 (Nested List Creation)

初始化一個 $3 \times 3$ 的零矩陣

```python
# nested loop
matrix = []
for i in range(3):
    row = []
    for j in range(3):
        row.append(0)
    matrix.append(row)

# nested comprehension
# [ [內層推導式] for 外層 in range ]
matrix = [[0 for j in range(3)] for i in range(3)]
```

| 特性         | nested loop                       | nested comprehension             |
| ------------ | --------------------------------- | -------------------------------- |
| 可讀性       | 高。邏輯分層明確，適合複雜邏輯。  | 中/低。超過兩層會變得難以閱讀。  |
| 程式碼長度   | 較長 (4-6 行)。                   | 極短 (1 行)。                    |
| 執行效能     | 稍慢 (因為頻繁呼叫 .append())。   | 較快 (底層經過優化)。            |
| 調試 (Debug) | 容易。可以中途 print 或設斷點。   | 困難。報錯時通常只會指出一整行。 |
| 使用時機     | 包含複雜 if-else 或多個副作用時。 | 簡單的數據轉換或矩陣扁平化。     |

---

## 兩組資料間的關聯 (Inter-group Mapping)

這類模式主要描述如何將集合 $D$ 與集合 $Z$ 的元素進行配對

1.  **Grouping / One-to-Many Mapping / 分群映射**

    這是最常見的組織方式。將 $Z$ 集合中的元素，根據某種隸屬關係「分配」給 $D$ 集合中的特定對象。
    - 邏輯： 每個 $d_i$ 像是一個「容器」或「標籤」，擁有一組屬於它的 $z_j$ 元素。在標準分群中，一個 $z_j$ 通常只會屬於一個 $d_i$。
    - 數學表達： 函數 $f: Z \to D$，將每個 $z$ 映射到一個唯一的 $d$。
    - 範例：
      - $d_1 = \{z_1, z_2\}$
      - $d_2 = \{z_3, z_4\}$
    - 應用場景：
      - 資料庫： GROUP BY 語句（如：按「分店」統計「銷售紀錄」）。
      - 檔案系統： 資料夾（$d$）與其中的檔案（$z$）。

    a. **Distributed Grouping / Streaming Grouping / Interleaved / 分散式分群**

         資料以交錯方式出現。
         - 特徵： z 元素以交錯或隨機順序對應到 d。這在處理即時串流或是未排序的日誌時非常常見。
         - 邏輯： 建立一個持續存在的對照表（Dictionary），每讀到一筆資料就往對應的分類裡「丟」。

         ```python
         from collections import defaultdict

         d_list = ['d1', 'd2', 'd3']
         z_list = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6']

         # 模擬分散的資料對 [d1, z1], [d2, z2], [d3, z3], [d1, z4]...
         distributed_pairs = [
             (d_list[0], z_list[0]), (d_list[1], z_list[1]), (d_list[2], z_list[2]),
             (d_list[0], z_list[3]), (d_list[1], z_list[4]), (d_list[2], z_list[5])
         ]

         # 使用 defaultdict 來自動處理首次出現的 key
         groups = defaultdict(list)
         for d, z in distributed_pairs:
             groups[d].append(z)

         print("Distributed Grouping Result:")
         print(dict(groups))
         # 輸出: {'d1': ['z1', 'z4'], 'd2': ['z2', 'z5'], 'd3': ['z3', 'z6']}
         ```

         ```python
         # Round-Robin

         a_list = ['a1', 'a2', 'a3']
         b_list = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8']
         c_list = []
         a_len = len(a_list)
         b_len = len(b_list)

         # basic
         i = 0
         for b in b_list:
             c_list.append([a_list[i % a_len], b])
             i += 1
         print(c_list)

         # list comprehension
         c_list = [[a_list[i % a_len], b] for i, b in enumerate(b_list)]
         print(c_list)

         # cycle iterator
         from itertools import cycle
         a_iter = cycle(a_list)
         c_list = [[next(a_iter), b] for b in b_list]
         print(c_list)
         ```

        ```python
        def expand_cycle(list1, list2):
            list1_iter = cycle(list1)
            data = []
            for l2 in list2:
                data.append([next(list1_iter), l2])
            return data

        def expand_cycle(list1, list2, strategy):
            data = [strategy(next(list1_iter), l2) for l2 in list2]
            return data
        ```

    b. **Contiguous Grouping / Block / Ordered Grouping / 區塊式分群**

        資料已經按照類別排序或分塊。
        - 特徵： 相同的 d 會連續出現。這種方式非常節省記憶體，因為只需要盯著當前的 d 看，一旦 d 變了，代表上一組已經結束。
        - 邏輯： 使用「快照」的概念，只有當 Key 改變時才開啟新組。

        ```python
        import itertools

        # 模擬連續的資料對 [d1, z1], [d1, z2], [d2, z3], [d2, z4]...
        contiguous_pairs = [
            ('d1', 'z1'), ('d1', 'z2'),
            ('d2', 'z3'), ('d2', 'z4'),
            ('d3', 'z5'), ('d3', 'z6')
        ]

        # itertools.groupby 是處理連續資料的神器
        # 注意：若資料非連續，groupby 會產生重複的 key 分組
        result = {k: [v for _, v in g] for k, g in itertools.groupby(contiguous_pairs, lambda x: x[0])}

        print("Contiguous Grouping Result:")
        print(result)
        # 輸出: {'d1': ['z1', 'z2'], 'd2': ['z3', 'z4'], 'd3': ['z5', 'z6']}
        ```

        ```python
        # Load Balancing / Chunking

        a_list = ['a1', 'a2', 'a3']
        b_list = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8']
        c_list = []

        q, r = divmod(len(b_list), len(a_list))  # quotient, remainder
        idx_begin = 0

        # basic
        for a in a_list:
            idx_end = idx_begin + q
            if r != 0:
                idx_end += 1
                r -= 1

            for b in b_list[idx_begin:idx_end]:
                c_list.append([a, b])
            idx_begin = idx_end
        print(c_list)

        # slice
        for i, a in enumerate(a_list):
            idx_end = idx_begin + q + (1 if i < r else 0)
            for b in b_list[idx_begin:idx_end]:
                c_list.append([a, b])
            idx_begin = idx_end
        print(c_list)

        # list comprehension
        c_list = [
            [a, b]
            for i, a in enumerate(a_list)
            for b in b_list[i * q + min(i, r): (i + 1) * q + min(i + 1, r)]
        ]
        print(c_list)

        # generator
        def chunk_list(lst, num_chunks):
            q, r = divmod(len(lst), num_chunks)
            for i in range(num_chunks):
                idx_begin = i * q + min(i, r)
                idx_end = (i + 1) * q + min(i + 1, r)
                yield lst[idx_begin:idx_end]

        # list comprehension
        c_list = [
            [a, b]
            for a, chunks in zip(a_list, chunk_list((b_list), len(a_list)))
            for b in chunks
        ]
        print(c_list)
        ```

        ```python
        def expand_chunk(list1, list2):
            q, r = divmod(len(list2), len(list1))
            data = []
            idx_start = 0
            for i, l1 in enumerate(list1):
                idx_end = idx_start + q
                if i < r:
                    idx_end += 1
                for l2 in list2[idx_start:idx_end]:
                    data.append([l1, l2])
                idx_start = idx_end
            return data

        def expand_chunk(list1, list2):
            q, r = divmod(len(list2), len(list1))
            data = []
            for i, l1 in enumerate(list1):
                for l2 in list2[i*q + min(i, r):(i+1)*q + min(i+1, r)]:
                    data.append([l1, l2])
            return data

        def expand_chunk(list1, list2, strategy):
            data = [strategy(l1, l2) for i, l1 in enumerate(
                list1) for l2 in list2[i*q + min(i, r):(i+1)*q + min(i+1, r)]]
            return data
        ```


        | Model       | Item                | Python Util        | Data Required                            |
        | ----------- | ------------------- | ------------------ | ---------------------------------------- |
        | Distributed | Hash-based Grouping | dict / defaultdict | 資料可亂序，需較多記憶體儲存 Hash Map。  |
        | Contiguous  | Stream / Sort-based | itertools.groupby  | 資料必須先排序（Sorted），非常省記憶體。 |

2.  **Cartesian Product / Cross Join / 笛卡兒積**

    這是一種「全組合」模式。它不考慮任何條件，強行將兩個集合的所有可能性配對。
    - 邏輯： 如果 $D$ 有 $m$ 個元素，$Z$ 有 $n$ 個元素，最終會產生 $m \times n$ 個配對組合。
    - 數學表達： $D \times Z = \{(d, z) \mid d \in D, z \in Z\}$。
    - 範例：
      - $D = \{紅色, 藍色\}$
      - $Z = \{S, M, L\}$
      - 結果：$\{(紅, S), (紅, M), (紅, L), (藍, S), (藍, M), (藍, L)\}$
    - 應用場景：
      - 測試工程： 測試軟體在所有硬體與操作系統組合下的相容性。
      - 電商： 生成商品的所有規格組合（顏色 $\times$ 尺寸）。

    ```python
    import itertools

    d = ['d1', 'd2', 'd3']
    z = ['z1', 'z2']

    # 產生全組合
    cartesian = list(itertools.product(d, z))

    print(cartesian)
    # 輸出: [('d1', 'z1'), ('d1', 'z2'), ('d2', 'z1'), ('d2', 'z2'), ('d3', 'z1'), ('d3', 'z2')]
    ```

    ```python
    def expand_cross(list1, list2):
        data = []
        for l1 in list1:
            for l2 in list2:
                data.append([l1, l2])
        return data

    def expand_cross(list1, list2):
        data = [[l1, l2] for l1 in list1 for l2 in list2]
        return data

    def expand_cross(list1, list2, strategy):
        data = [strategy(l1, l2) for l1 in list1 for l2 in list2]
        return data
    ```

3.  **Zip / Pairwise Matching / 點對點配對**

    這是一種「平行並行」的模式，兩組資料像拉鍊一樣依序咬合。
    - 邏輯： 取 $D$ 的第 $i$ 個元素與 $Z$ 的第 $i$ 個元素配對。通常當其中一組耗盡時，配對就會停止。
    - 特點： 強烈依賴資料的原始順序。
    - 範例：
      - $d = [姓, 名]$， $z = [王, 小明]$
      - 結果：$(姓, 王), (名, 小明)$
    - 應用場景：
      - 資料對齊： 將「時間戳記列表」與「感測器數值列表」合併。
      - 模型訓練： 在深度學習中，將「圖片路徑」與對應的「標籤」進行配對。

    ```python
    d = ['d1', 'd2', 'd3']
    z = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6']

    # 1對1配對 (長度以短的為主)
    zipped = list(zip(d, z))

    print(zipped)
    # 輸出: [('d1', 'z1'), ('d2', 'z2'), ('d3', 'z3')]
    ```

4.  **Conditional Join / Theta Join / 條件結合**

    這是最靈活但也最複雜的模式。配對的建立不再是隨機或按順序，而是基於特定的布林邏輯 (Predicate)。
    - 邏輯： 只有當 $d$ 與 $z$ 滿足特定的運算關係（如：大於、等於、包含、相似度 > 0.8）時，才會形成配對。
    - 數學表達： $\{(d, z) \mid d \in D, z \in Z, \text{Condition}(d, z) \text{ is True}\}$。
    - 範例：
      - $D = [薪資標準 5萬]$
      - $Z = [員工A(6萬), 員工B(4萬)]$
      - 條件：$z.\text{salary} > d.\text{standard}
      - $結果：$(5萬, 員工A)$
    - 應用場景：
      - 關聯式資料庫： INNER JOIN 或 LEFT JOIN（如：根據 User_ID 媒合使用者與訂單）。
      - 模糊比對： 將兩個名稱相似但不完全相同的資料表進行合併。

    ```python
    # 範例：只有當數字 d 與 z 相加等於 10 時才配對
    d_nums = [2, 5, 8]
    z_nums = [3, 5, 7, 8]

    conditional_pairs = [(a, b) for a in d_nums for b in z_nums if a + b == 10]

    print(conditional_pairs) # 輸出: [(2, 8), (5, 5)]
    ```

| Model       | Keyword            | 決定配對的因素   | 輸出數量             |
| ----------- | ------------------ | ---------------- | -------------------- |
| Grouping    | Belonging / 隸屬   | 類別屬性         | 等於 Z 的總數        |
| Cartesian   | Combination / 組合 | 窮舉所有可能     | D長度 × Z長度        |
| Zip         | Sequence / 序列    | 索引位置 (Index) | min(D,Z) 的長度      |
| Conditional | Logic / 邏輯       | 自定義條件       | 視符合條件的數量而定 |

---

## 單組資料內的組織 (Intra-group Organization)

這類模式主要描述如何處理單一序列或集合內的元素結構。重點在於如何根據特定的結構、順序或機率，從一個大序列中產生子集。

1. **Sliding Window / 滑動窗口**

   這是在處理序列資料（如時間序列、音訊或文本）時最核心的技術。它透過一個固定長度的「窗口」在序列上移動，擷取局部連續的子集。
   - 邏輯： 定義窗口大小 $k$ 與步長 (Stride)。窗口內的元素會隨著移動而重複出現。
   - 應用場景： 計算股票的 5 日移動平均線、自然語言處理中的 $N$-grams（預測下一個字）。

   ```python
   def sliding_window(data, size):
       return [data[i : i + size] for i in range(len(data) - size + 1)]

   z = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6']
   print(sliding_window(z, 3))
   # 輸出: [['z1', 'z2', 'z3'], ['z2', 'z3', 'z4'], ['z3', 'z4', 'z5'], ['z4', 'z5', 'z6']]
   ```

2. **Hierarchy / Nested Grouping / 階層式組織**

   這是一種「樹狀結構」。資料不再是扁平的，而是具備父子、隸屬的層級關係。
   - 邏輯： 將元素按等級劃分，每一層級包含下一層級的引用。通常使用嵌套字典或樹 (Tree) 資料結構。
   - 應用場景： 檔案系統、組織架構圖、網頁的 DOM Tree、生物分類學。

   ```python
   # 模擬一個簡單的分類階層
   hierarchy = {
       'Electronics': {
           'Phone': ['iPhone', 'Pixel'],
           'Laptop': ['MacBook', 'ThinkPad']
       },
       'Books': ['Fiction', 'Science']
   }

   print(hierarchy['Electronics']['Phone']) # 輸出: ['iPhone', 'Pixel']
   ```

3. **Random Binning / Sampling / 隨機分箱**

   當資料量龐大或需要進行實驗對照時，將元素「隨機」且「均勻」地分配到不同的籃子（Bins）中。
   - 邏輯： 使用隨機數生成器，確保每個元素進入某個組別的機率是相等的。通常分為「放回抽樣」與「不放回抽樣」。
   - 應用場景： 機器學習中的訓練/測試集切分 (Train-Test Split)、A/B Testing 實驗分組。

   ```python
   import random

   z = ['z1', 'z2', 'z3', 'z4', 'z5', 'z6']
   random.shuffle(z) # 隨機打亂

   # 分成兩組 (Bin A, Bin B)
   bin_a = z[:3]
   bin_b = z[3:]

   print(f"Group A: {bin_a}, Group B: {bin_b}")
   ```

4. **Combinations / 組合**

   這是數學上的窮舉，從集合中取出所有可能的不重複子集。
   - 邏輯： 考慮從 $n$ 個元素中取出 $r$ 個。在「組合」中，順序不重要（$[z1, z2]$ 與 $[z2, z1]$ 被視為同一個）。
   - 應用場景： 密碼窮舉、找出所有可能的投資組合、排班系統。

   ```python
   from itertools import combinations

   z = ['z1', 'z2', 'z3', 'z4']

   # 從 4 個元素中選出 2 個的所有組合
   res = list(combinations(z, 2))

   print(res)
   # 輸出: [('z1', 'z2'), ('z1', 'z3'), ('z1', 'z4'), ('z2', 'z3'), ('z2', 'z4'), ('z3', 'z4')]
   ```

| Model          | 核心原則       | 元素重複性       | 輸出結構         |
| -------------- | -------------- | ---------------- | ---------------- |
| Sliding Window | 順序性與連續性 | 元素會重疊出現   | 固定長度的子序列 |
| Hierarchy      | 隸屬關係       | 元素具備父子級別 | 樹狀/嵌套字典    |
| Random Binning | 機率與隨機性   | 元素通常不重疊   | 隨機子集         |
| Combinations   | 數學窮舉       | 元素位置的排列   | 所有的子集可能性 |
