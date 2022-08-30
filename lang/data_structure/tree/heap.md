# min heap

binary heap or binary tree


## insert

是從 leaf insert

[2, 1, 3, 4]

```
             2          1            1                1
  2  ->     /     ->   /    ->     /   \    ->      /   \
           1         2            2     3          2     3
                                                  /
                                                 4
    insert       sort      insert
                           no sort
```


---

## delete

[2, 1, 5, 4, 6, 3] - min

```
      1                  5               5              3              2
    /   \              /   \           /   \          /   \          /   \
   2     3    ->      2     3   ->    2     3   ->   2     5   ->   3     5
  / \   /            / \   /         / \            / \            / \
 4   6  5           4   6  1        4   6          4   6          4   6
            change             delete          sort           sort
```


## max heap


---

## min - max heap

1. binary tree

2. tree level 為 min level 和 max level

3. root 為 min

```
               2            min level
         /          \
        60           50     max level
     /      \       /  \
    15      20     10   8   min level
   /  \    /  \
 45   55  30   38           max level
```


---

## max - min heap
