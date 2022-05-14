# bitwise

左移: x << y : x 左移 y 位元, 左移出的位元會被丟棄, 右側會補上 0
右移: x >> y : x 右移 y 位元, 右移出的位元會被丟棄


```c

// set a bit
unsigned char a |= (1 << n);

a               1 0 0 0 0 0 0 0
a |= (1 << 1) = 1 0 0 0 0 0 1 0
a |= (1 << 3) = 1 0 0 0 1 0 0 0
a |= (1 << 5) = 1 0 1 0 0 0 0 0

// clear a bit
unsigned char b &= ~(1 << n);

b                1 1 1 1 1 1 1 1
b &= ~(1 << 1) = 1 1 1 1 1 1 0 1
b &= ~(1 << 3) = 1 1 1 1 0 1 1 1
b &= ~(1 << 5) = 1 1 0 1 1 1 1 1

// toggle a bit
unsigned char c ^= (1 << n);

c               1 0 0 1 1 0 1 1
c ^= (1 << 1) = 1 0 0 1 1 0 0 1
c ^= (1 << 3) = 1 0 0 1 0 0 1 1
c ^= (1 << 5) = 1 0 1 1 1 0 1 1

//
unsigned char e = d & (1 << n);
```

---

## ref

[你所不知道的 C 語言: bitwise 操作](https://hackmd.io/@sysprog/c-bitwise)
