# Data Expand Strategy

「原子組合 (Atomic)」 與 「結構組合 (Structural)」

expand_cross (全組合)
expand_cycle (全局循環)
expand_zip (一對一對齊)
expand_chunk_inner_cycle (組內重置循環)
expand_fixed (固定填補)
expand_balanced_chunk (負載均衡分組)
expand_pair (一對多固定分配)
expand_random (隨機抽樣)
expand_unique_combination (唯一無序組合)

1. expand_cross (全組合 / 笛卡爾積)

將所有輸入列表的元素進行交叉乘積。如果 A 列表有 2 個元素，B 列表有 3 個，最終會生成 $2 \times 3 = 6$ 組結果。

- 場景：窮舉測試（Brute-force）、多維度參數組合。
- 範例：[A, B] 與 [1, 2] $\rightarrow$ (A,1), (A,2), (B,1), (B,2)。



2. expand_cycle (全局循環)

當兩個列表長度不一時，以最長列表為基準，短列表從頭開始循環，直到填滿長度。

- 場景：資源分配，例如將 10 個任務分配給 3 台機器。
- 範例：[A, B, C, D] 與 [1, 2] $\rightarrow$ (A,1), (B,2), (C,1), (D,2)。


3. expand_zip (一對一對齊)

嚴格按照索引位置配對。通常以最短列表為準（或在長度不符時拋錯/停止）。

- 場景：並行參數，如用戶名對應其專屬的 ID。
- 範例：[A, B, C] 與 [1, 2] $\rightarrow$ (A,1), (B,2)。

4. expand_chunk_inner_cycle (組內重置循環)

這通常涉及「分組」概念。在每一組（Chunk）內部進行循環對齊，當進入下一個分組時，對齊邏輯會重置。

- 場景：多機房部署中，每個機房（Chunk）內的節點都要對應一組相同的配置。

5. expand_fixed (固定填補)

以長列表為準，短列表不足的部分使用最後一個元素或預設值進行填充，不再循環。

- 場景：當後續操作需要固定佔位符時。
- 範例：[A, B, C] 與 [1] $\rightarrow$ (A,1), (B,1), (C,1)。

6. expand_balanced_chunk (負載均衡分組)

將元素盡可能均勻地分配到指定數量的組（Chunks）中，確保各組之間的數量差異最小化。

- 場景：分散式計算、任務分片（Sharding）。
- 邏輯：10 個任務分給 3 個節點 $\rightarrow$ 組大小分別為 4, 3, 3。

7. expand_pair (一對多固定分配)

將主列表的「一個」元素固定分配給子列表的「多個」元素。這與 Cross 類似，但更強調層級結構。

- 場景：一個 Master 節點對應多個 Worker 節點的拓撲結構定義。

8. expand_random (隨機抽樣)

不按順序，從組合空間中隨機抽取指定數量的樣本。

- 場景：模糊測試（Fuzz Testing）、在大數據集上進行壓力測試抽樣。

9. expand_unique_combination (唯一無序組合)

從單一集合中選取所有可能的組合，但不考慮順序（即 $C(n, k)$），且不重複選取相同元素。

- 場景：節點兩兩對接測試（P2P 測試）。
- 範例：[A, B, C] 取 2 個 $\rightarrow$ (A,B), (A,C), (B,C)（排除 (B,A) 等重覆）。
