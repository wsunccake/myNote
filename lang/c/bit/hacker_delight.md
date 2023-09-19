# hacker delight

---

## content

- [basic](#basic)
  - [n complement](#n-complement)
  - [manipulating rightmost bit](#manipulating-rightmost-bit)
  - [De Morgan’s Laws](#de-morgans-laws)
  - [De Morgan’s Laws Extended](#de-morgans-laws-extended)
  - [addition combined with logical operation](#addition-combined-with-logical-operation)
  - [inequalities among logical and arithmetic expression](#inequalities-among-logical-and-arithmetic-expression)

---

## basic

### n complement

```c
-x = ~x + (n - 1)
```

### manipulating rightmost bit

```c
// unsigned int, 2^n
x & (x - 1)     1 => 0, 0 => 0
x               0101 1000
x - 1           0101 0111
x&(x - 1)       0101 0000
                     ^

x & (x + 1)     1 => 0, 0 => 0
x               1010 0111
(x + 1)         1010 1000
x & (x + 1)     1010 0000
                      ^^^

x | (x - 1)     0 => 1, 1 => 1
x               1010 1000
(x - 1)         1010 0111
x | (x - 1)     1010 1111
                 ^^^

x | (x + 1)     0 => 1, 1 => 1
x               1010 0111
(x + 1)         1010 1000
x | (x + 1)     1010 1111
                     ^

~x | (x - 1)
x               1010 1000
~x              0101 0111
(x - 1)         1010 0111
~x | (x - 1)    1111 0111
                ^ ^

~x | (x + 1)
x               1010 0111
~x              0101 1000
(x + 1)         1010 1000
~x | (x + 1)    1111 1000
                ^ ^

~x & (x - 1) = ~(x | -x) = (x & -x) - 1
x               1010 1000
~x              0101 0111
(x - 1)         1010 0111
~x | (x - 1)    0000 0111
                 ^ ^

~x & (x + 1)
x               1010 0111
~x              0101 1000
(x + 1)         1010 1000
~x & (x + 1)    0000 1000
                 ^ ^

x & (-x)
x               0101 1000
-x              1010 1000
x & (-x)        0000 1000
                 ^ ^

x ^ (x - 1)
x               0101 1000
x - 1           0101 0111
x ^ (x - 1)     0000 1111
                 ^ ^  ^^^

x ^ (x + 1)
x               0101 0111
x + 1           0101 1000
x ^ (x + 1)     0000 1111
                 ^ ^ ^
```

### De Morgan’s Laws

```c
// De Morgan’s Laws
~(x & y)  = ~x | ~y
~(x | y)  = ~x & ~y
```

### De Morgan’s Laws Extended

```c
~(x + 1)  = ~x - 1
~(x - 1)  = ~x + 1
~-x       = ~(~x + 1)  = x-1
~(x ^ y)  = ~x ^ y
```

```c
# example
x =                               xxx0 1111 0000
smallest = x & -x;                0000 0001 0000
ripple = x + smallest;            xxx1 0000 0000
ones = x ^ ripple;                0001 1111 0000
ones >> 2                         0000 0111 1100
ones = (ones >> 2) / smallest;    0000 0000 0111
ripple | ones;                    xxx1 0000 0111
```

### addition combined with logical operation

```c
-x    = ~x + 1
      = ~(x - 1)
~x    = -x - 1
-~x   = x + 1
-~-~x = x + 2
~-x   = x - 1
~-~-x = x - 2
x + y = x - ~y - 1
      = (x ^ y) + 2(x & y)
      = (x | y) + (x & y)
      = 2(x | y) - (x ^ y)
x - y = x + ~y + 1
      = (x ^ y) - 2(~x & y)
      = (x & ~y) - (~x & y)
      = 2(x & ~y) - (x ^ y)
x ^ y   = (x | y) - (x & y)
        = (x & ~y) | (~x & y)
x & ~y  = (x | y) - y
        = x - (x & y)
~(x-y)  = y - x -1
        = ~x + y
~(x ^ y)  = (x & y) - (x | y) - 1
          = (x & y) + ~(x | y)
x | y   = (x & ~y) + y
x & y   = (~x | y) - ~x
```

### inequalities among logical and arithmetic expression

```c
x ^ y  <=  x | y
x & y  <=  ~(x ^ y)
x | y  >=  max(x, y)
x & y  <=  min(x, y)
x | y  <=  x + y (not overflow)
x | y  >=  x + y (overflow)
abs(x + y) <= ~(x ^ y)
```

```c
x     y     ~x    ~y    0     1
0     0     1     1     0     1
0     1     1     0     0     1
1     0     0     1     0     1
1     1     0     0     0     1

            x & y       x & ~y
x     y           ~x & y      ~(x & y)
0     0     0     0     0     1
0     1     0     1     0     1
1     0     0     0     1     1
1     1     1     0     0     0


            x | y       x | ~y
x     y           ~x | y      ~(x | y)
0     0     0     1     1     1
0     1     1     1     0     0
1     0     1     0     1     0
1     1     1     1     1     0


            x ^ y       x ^ ~y
x     y           ~x ^ y      ~(x ^ y)
0     0     0     1     1     1
0     1     1     0     0     0
1     0     1     0     0     0
1     1     0     1     1     1
```

### absolute value function

```c
abs                     nabs
(x ^ y) - y             y - (x ^ y)
(x + y) ^ y             (y - x) ^ y
x - (2x & y)            (2x & y) - x

2x = x << 1
y = x >> 31
((x >> 30) | 1 ) * x = +1|-1
```

### average of two integer

```c
// unsigned integer
(x & y) + ((x ^ y) >> 1)      // without casing overflow
(x | y) - (~(x ^ y) >> 1)     //
```

### sign extension

```c
((x+0x0000000080)&0x00000000FF)-0x0000000080
((x&0x0000000080)^0x00000000FF)-0x0000000080
(x&0x000000007F)-(x&0x0000000080)
```

### shift right signed from unsigned
