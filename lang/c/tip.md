## point declare

```c
int *ptr, val   // ptr 是 pointer to int, val 是 int
int* ptr, val   // 同上, 但是 val 會讓人誤解成 pointer to int
```


## implicit data convert

```c
#include <stdio.h>

int main() { puts("-0.5" + 1); }

// 0.5
```

"-0.5" 是 char *, 然後往後一個 index


```c
#include <stdio.h>

int main() { printf("%d\n" 50 ** "2"); }

// 2500
```

"2" 在 ascii 為 50, (void *)  50 被轉成 int 50. 最後在 50 * 50
