# bitwise hack

---

## content

- [basic](#basic)
  - [set a bit](#set-a-bit)
  - [unset / clear a bit](#unset--clear-a-bit)
  - [toggle a bit](#toggle-a-bit)
  - [check a bit](#check-a-bit)
  - [strip off last set bit](#strip-off-last-set-bit)
  - [get lowest set bit](#get-lowest-set-bit)
- [complement](#complement)
  - [invert every bit for 1's complement](#invert-every-bit-for-1s-complement)
  - [invert every bit for 2's complement](#invert-every-bit-for-2s-complement)
- [application](#application)
  - [divide by 2](#divide-by-2)
  - [divide by power of 2 n](#divide-by-power-of-2-n)
  - [modulo](#modulo)
  - [swap](#swap)
  - [combine two number to one](#combine-two-number-to-one)
- [n-byte align](#n-byte-align)

---

## basic

### set a bit

```c
unsigned char a = 0x80;
a |= (1 << n);
printf("a: %u ...\n", a);

a               1 0 0 0 0 0 0 0
a |= (1 << 1) = 1 0 0 0 0 0 1 0
a |= (1 << 3) = 1 0 0 0 1 0 0 0
a |= (1 << 5) = 1 0 1 0 0 0 0 0
```

```python
def set (num, pos):
  print(f"before num: {num}\t{bin(num)}")
  num |= (1 << pos)
  print(f"after  num: {num}\t{bin(num)}")

num, pos = 4, 1
set(num, pos)
```

### unset / clear a bit

```c
unsigned char b = 0xff;
b &= ~(1 << n);
printf("b: %u ...\n", b);

b                1 1 1 1 1 1 1 1
b &= ~(1 << 1) = 1 1 1 1 1 1 0 1
b &= ~(1 << 3) = 1 1 1 1 0 1 1 1
b &= ~(1 << 5) = 1 1 0 1 1 1 1 1
```

```python
def unset(num, pos):
    print(f"before num: {num}\t{bin(num)}")
    num &= (~(1 << pos))
    print(f"after  num: {num}\t{bin(num)}")

num, pos = 7, 1
unset(num, pos)
```

### toggle a bit

```c
unsigned char c = 0x9b;
c ^= (1 << n);
printf("c: %u ...\n", c);

c               1 0 0 1 1 0 1 1
c ^= (1 << 1) = 1 0 0 1 1 0 0 1
c ^= (1 << 3) = 1 0 0 1 0 0 1 1
c ^= (1 << 5) = 1 0 1 1 1 0 1 1

// 大小寫互換
char a = 'a'; // 0101 0001
char A = 'A'; // 0100 0001
printf("a: %c, %u\n", a, a);
printf("A: %c, %u\n", A, A);
a ^= (1 << 5);
A ^= (1 << 5);
printf("a: %c, %u\n", a, a);
printf("A: %c, %u\n", A, A);
```

```python
def toggle(num, pos):
    print(f"before num: {num}\t{bin(num)}")
    num ^= (1 << pos)
    print(f"after  num: {num}\t{bin(num)}")

num, pos = 7, 1
toggle(num, pos)
```

### check a bit

```c
unsigned char e = d & (1 << n);
```

```python
def at_position(num, pos):
    print(f"before num: {num}\t{bin(num)}")
    bit = num & (1<<pos)
    print(f"after  num: {num}\t{bin(num)}")
    print(f'then   bit: {bit}\t{bin(bit)}')
    return bit

num, pos = 7, 2
bit = at_position(num, pos)
```

## strip off last set bit

```c
num = num & (num-1);
```

```python
def strip_last_set_bit(num):
    print(f"before num: {num}\t{bin(num)}")
    num &= (num - 1)
    print(f"after  num: {num}\t{bin(num)}")

num = 6
strip_last_set_bit(num)
```

## get lowest set bit

```c
ret = num & (-num);
```

```python
def lowest_set_bit(num):
    print(f"before num: {num}\t{bin(num)}")
    num &= (-num)
    print(f"after  num: {num}\t{bin(num)}")

num = 10
lowest_set_bit(num)
```

---

## complement

### invert every bit for 1's complement

```c
int num = 4;
~num
```

```python
def invert_1(num):
    print(f"before num: {num}\t{bin(num)}")
    print(f"after  num: {~num}\t{bin(~num)}")

num = 4
invert_1(num)
```

### invert every bit for 2's complement

```c
int num = 4;
-num;
(~num+1);
```

```python
def invert_2(num):
    print(f"before num: {num}\t{bin(num)}")
    print(f"after  num: {-num}\t{bin(-num)}")
    print(f"after  num: {~num+1}\t{bin(~num+1)}")

num = 4
invert_2(num)
```

---

---

## application

### divide by 2

```c
int num = 12;
num >> 1;
```

```python
def divide_by_2(num):
    print(f"before num: {num}\t{bin(num)}")
    print(f"after  num: {num >> 1}\t{bin(num >> 1)}")

num = 6
divide_by_2(num)
```

### divide by power of 2 n

```c
int num = 12;
num << 1;
```

```python
def multiply_by_2(num):
    print(f"before num: {num}\t{bin(num)}")
    print(f"after  num: {num << 1}\t{bin(num << 1)}")

num = 6
multiply_by_2(num)
```

### modulo by power of 2 n

```c
int num = 12;
num % 2 == num & 1
num % 4 == num & 3
num % 8 == num & 7
// num % 2^i = num & (2^i - 1) = num & (1 << i - 1)
```

### swap

```c
int a = 1, b = 3;
a = a ^ b;
b = a ^ b;
a = a ^ b;
```

### combine two number to one

```c
#include <stdio.h>
#include <limits.h>
#include <stdlib.h>

#define MINORBITS (sizeof(unsigned char) * 8 + 1)
#define MINORMASK ((1U << MINORBITS) - 1)
#define MAJOR(dev) ((unsigned int)((dev) >> MINORBITS))
#define MINOR(dev) ((unsigned int)((dev)&MINORMASK))
#define MKDEV(ma, mi) (((ma) << MINORBITS) | (mi))

char *decimal_to_binary(int n)
{
    int c, d, t;
    char *p;
    int total = (MINORBITS - 1) * 2;
    t = 0;
    p = (char *)malloc(total + 1);

    if (p == NULL)
        exit(EXIT_FAILURE);

    for (c = total - 1; c >= 0; c--)
    {
        d = n >> c;

        if (d & 1)
            *(p + t) = 1 + '0';
        else
            *(p + t) = 0 + '0';

        t++;
    }
    *(p + t) = '\0';

    return p;
}
int main()
{
    printf("unsigned char: %lu byte\n", sizeof(unsigned char));
    printf("unsigned short: %lu byte\n", sizeof(unsigned short));
    // printf("unsigned int: %lu byte\n", sizeof(unsigned int));
    printf("MINORBITS: %3d, %s\n", MINORBITS, decimal_to_binary(MINORBITS));
    printf("MINORMASK: %3d, %s\n", MINORMASK, decimal_to_binary(MINORMASK));
    printf("-----------------------------\n");

    unsigned char ma = 123;
    unsigned char mi = 5;
    printf("ma   : %7d, %s\n", ma, decimal_to_binary(ma));
    printf("mi   : %7d, %s\n", mi, decimal_to_binary(mi));
    unsigned short ma1 = ma << (sizeof(unsigned char) * 8 + 1);
    printf("ma   : %7d, %s ma <<\n", ma1, decimal_to_binary(ma1));
    unsigned short dev = ma1 | mi;
    printf("ma   : %7d, %s (ma <<) | mi\n", dev, decimal_to_binary(dev));
    printf("-----------------------------\n");

    printf("dev  : %7d, %s\n", dev, decimal_to_binary(dev));
    unsigned short ma2 = (dev >> MINORBITS);
    printf("MAJOR: %7d, %s dev >>\n", ma2, decimal_to_binary(ma2));
    unsigned short mi2 = (dev & MINORMASK);
    printf("MINOR: %7d, %s dev &\n", mi2, decimal_to_binary(mi2));
    printf("-----------------------------\n");

    printf("dev  : %7d, %s\n", MKDEV(ma, mi), decimal_to_binary(MKDEV(ma, mi)));
    printf("MAJOR: %7d, %s\n", MAJOR(dev), decimal_to_binary(MAJOR(dev)));
    printf("MINOR: %7d, %s\n", MINOR(dev), decimal_to_binary(MINOR(dev)));

    return 0;
}
```

---

## n-byte align

```c
#include <stdio.h>

#define nbyte 4
#define align_byte(x) ((x) & (nbyte - 1)) ? ((((x) >> (nbyte / 2)) + 1) << (nbyte / 2)) : (x)
#define align_byte_up(x) (x + (nbyte - 1)) & (~(nbyte - 1))
#define align_byte_down(x) (x) & (~(nbyte - 1))

int main()
{
    for (int i = 0; i < 20; i++) {
        printf("%d -> %d\n", i, align_byte(i));
        printf("%d -> %d up\n", i, align_byte_up(i));
        printf("%d -> %d down\n", i, align_byte_down(i));
    }

    return 0;
}
```

---

## ref

- [Bit Twiddling Hacks](https://graphics.stanford.edu/~seander/bithacks.html)
