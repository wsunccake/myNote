# bitwise

左移: x << y : x 左移 y 位元, 左移出的位元會被丟棄, 右側會補上 0
右移: x >> y : x 右移 y 位元, 右移出的位元會被丟棄

---

## bitwise hack

[bitwise_hack](./bitwise_hack.md)

```c
// right / left bit, if 1 byte
unsigned char value = 0x5a;
printf("value: %u, %x ...\n", value, value);
unsigned char right = value & 0xf;
printf("right: %u, %x ...\n", right, right);
unsigned char left = (value >> 4) & 0xf;
printf("left: %u, %x ...\n", left, left);
```

```text
by order / endianness

value = 0x12345678

mem addr:           low -> high
                    a       a+1     a+2     a+3
little endian:      0x78    0x56    0x34    0x12
big endian:         0x12    0x34    0x56    0x78
```

```
bit manipluation
bit mask

hex = bin
5 = 101
55 = 1010101
33 = 110011
333 = 1100110011
aa =
0f0f =
```

---

## ref

[你所不知道的 C 語言: bitwise 操作](https://hackmd.io/@sysprog/c-bitwise)
