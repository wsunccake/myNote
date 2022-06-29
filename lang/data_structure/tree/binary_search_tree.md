# binary search tree

## traversal

### BFS / Breadth First Search

    use queue

    level-order

### DFS / Depth First Search

    use recursive or stack

    pre-order:  root → left → right

    in-order:   left → root → right

    post-order: left → right → root


```
      A
    /   \
   B     C
  / \   / \
 D   E  F  G

level-order: ABCDEFG
pre-order:   ABDECFG
in-order:    DBEAFCG
post-order:  DEBFGCA
```


---

## add / insert

[3, 1, 2, 4, -1]

```
3

---

    3
  /
1

---

    3
  /
1
  \
    2

---

    3
  /   \
1      4
  \
    2

---

       3
     /   \
    1      4
  /   \
-1     2
```


---

## delete / remove

[3, 1, 2, 4, -1] - 4 - 1


```
       3
     /   \
    1      4
  /   \
-1     2

---

       3
     /
    1
  /   \
-1     2

---
            or
       3           3
     /           /
    2         -1
  /              \
-1                 2
```
