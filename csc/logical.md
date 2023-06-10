# logical design

## complement

[解讀計算機編碼](https://hackmd.io/@sysprog/binary-representation)

```
binary  unsign  sing	1s complement	2s complement
0000    0       0     0	            0
0001	  1       1     1	            1
0010	  2       2     2	            2
0011	  3       3     3	            3
0100	  4       4     4	            4
0101	  5       5     5	            5
0110	  6       6     6	            6
0111	  7       7     7	            7
1000	  8       -0    -7	          -8
1001	  9       -1    -6	          -7
1010	  10      -2    -5	          -6
1011	  11      -3    -4	          -5
1100	  12      -4    -3	          -4
1101	  13      -5    -2	          -3
1110	  14      -6    -1	          -2
1111	  15      -7    -0	          -1
```

```
1 + 4 = (0001)u + (0100)u = (0101)u = 5
1 - 4 = (0001)s + (1100)s = (1101)u = -5 != -3
1 - 4 = (0001)1 + (1011)1 = (1100)1 = -3
1 - 4 = (0001)2 + (1100)2 = (1101)2 = -3
1 - 1 = (0001)1 + (1110)1 = (1111)1 = -0 = 0
1 - 1 = (0001)1 + (1111)1 = (0000)1 = 0
```

```
# decimal
10's complement      (10 - 1)'s complement
     1,000,000                   999,999
   -   012,398               -   012,398
   =   987,602               =   987,601
  總加為 0 / 10             總加為 9

# binary
2's complement      (2 - 1)'s comlement
      1,000,000                   111,111
    -   101,100               -   101,100
    =   010,100               =   010,011
  總加為 0                   總加為 1
```

```
# decimal
一般算法            10's comlement
    72,532            72,532
-    3,250         +  96,750  ->  96,750 為 3,250 補數 / complement
=   69,282           169,282  ->  在移除溢位, 就是答案, 用加法當減法

     3,250             3,250
-   72,532         +  27,468
=  -69,282         =  30,718  ->  取 30,718 補數 69,282 再加上負號
```

---

## cpu cache

```
x KiB       register    0.x ns
x00 KiB     cache       x ns
x MiB       memory      x00 ns
x GiB       SSD         0.x ms
x TiB       HD          x ms
```

```
CPU (Intel i7-8700k)
Size of L1 Cache: 384 KiB
Size of L2 Cache: 1.5 Mib
Size of L3 Cache: 12 Mib
Speed: L1 > L2 > L3
```

### cache component

$$
\begin{align*}
Cache &= [Cache Set]
\newline

Cache Set &= [Cache Line]
\newline

Cache Line &= [Valid Bit, Tag, Data]
\end{align*}
$$

### cache size

$$
\begin{align*}
C &= S \times E \times B
\end{align*}
$$

C: data bytes
S: sets
E: lines per set
B: bytes per cache block (data)

### cache layout

- Directed Mapped
- Set Associative
- Fully Associative

### cache miss

- compulsory miss / cold start miss
- capacity miss
- conflict miss / collision miss

### conflict misses strategy

- FIFO (first in first out)
- random
- LRU (least recently used)

$$
    F_e = \frac{1}{4 \pi \epsilon_0} \frac{q_1 q_2}{r^2}
$$
