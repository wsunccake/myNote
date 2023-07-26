# bitwise hack

## set a bit

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

---

## unset / clear a bit

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

---

## toggle a bit

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

---

## check a bit

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

---

## invert every bit for 1's complement

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

---

## invert every bit for 2's complement

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

---

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

## divide by 2

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

---

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
