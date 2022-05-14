# function

## function prototype

```c
#include <stdio.h>

int factorial(int n);   // function prototype

int main(void) {
    printf("%d\n", factorial());
    return 0;
}

int factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```


---

iso C 並不支援 nest function


---

malloc: (overcommit) 儘可能之前記憶體空間, 拿到的空間可能會比要求的小, OS 發現開始不夠用時就開始殺東殺西把空間滕出來, 直到砍到沒東西能砍了 OOM

calloc: 儘可能用沒使用過記憶體空間, 不需做 memset, 但需要的空間較多

calloc != malloc + memset

```c
unsigned n, m;
scanf("%u %u", &n, &m);

long arr[n + 1];                                // 使用 stack
for (size_t i = 1; i <= n; ++i)
    arr[i] = 0;
```

```c
unsigned n, m;
scanf("%u %u", &n, &m);

long *arr = malloc((n + 1) * sizeof(*arr));     // 使用 heap
for (size_t i = 1; i <= n; ++i)
    arr[i] = 0;
```

```c
unsigned n, m;
scanf("%u %u", &n, &m);

long *arr = calloc((n + 1) * sizeof(*arr));
```

malloc or calloc 都是在 heap 裡面操作

stack


---

## function notation

```c
void foo(int x) {}
             ^
        parameter

foo(4)
    ^
argument
```

---

## heap allocator


---

## stack


---

## ref

[你所不知道的 C 語言：函式呼叫篇](https://hackmd.io/@sysprog/c-function)
