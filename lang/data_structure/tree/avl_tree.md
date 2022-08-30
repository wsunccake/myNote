# avl tree

Adelson-Velsky and Landis Tree

BF (balance factor) = left height - right height

## LL


```
        height    BF       after
    3   2         2           2
   /                        /   \
  2     1         1        1     3
 /
1       0         0
```


---

## RR

```
        height    BF       after
1       2         -2          2
 \                          /   \
  2     1         -1       1     3
   \
    3   0         0
```


---

## LR

```
      height    BF       after
  3   2         2           3           2
 /                         /           / \
1     1         -1        2      ->   1   3
 \                       /
  2   0         0       1
```


---

## RL

```
        height    BF       after
1       2         -2       1              2
 \                          \           /   \
  3     1         1          2    ->   1     3
 /                            \
2       0         0            3
```
