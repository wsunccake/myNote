# red-black tree

## rule

0. root is black / 根是黑色

1. every node is either red or black / 節點是紅色或黑色

2. all NIL nodes are considered black / 所有葉子都是黑色

3. red node does not have a red child / 每個紅色節點必須有兩個黑色的子節點

4. every path from a given node to any of its descendant NIL nodes goes through the same number of black nodes / 從任一節點到其每個葉子的所有簡單路徑都包含相同數目的黑色節點


---

## insert

[1, 2, 3, 4, 5, 6, 7, 8]

*: red

no *: black

insert mus be red

```
+ 1

1*   ->  1

1* recolor -> 1
---
[1] + 2

1
 \
  2*

---
[1, 2] + 3

1                  2*             2
 \                /  \          /   \
  2*      ->     1    3*  ->   1*    3*
   \
    3*

2*, 3* not match r3
2* is diff with 1 -> NIL color => rotate

2* -> 2, 1 -> 1*

---
[1, 2, 3] + 4

   2               2
 /   \           /   \
1*    3*    ->  1     3
       \               \
        4*              4*

1* -> 1, 3* -> 3

---
[1, 2, 3, 4] + 10

   2               2                   2
 /   \           /   \               /   \
1     3     ->  1     3*       ->   1     4
       \               \                 /  \
        4*              4               3*   10*
         \               \
          10*             10*

4*, 10* not match r3
3 -> 3*, 4* -> 4

---
[1, 2, 3, 4, 10] + 14

   2                   2
 /   \               /   \
1     4       ->    1     4*
     /  \                /  \
    3*   10*            3    10
          \                    \
          14*                   14*

---
[1, 2, 3, 4, 10, 14] + 7

   2
 /   \
1     4*
     /  \
    3    10
        /  \
       7*   14*
```

