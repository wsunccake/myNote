# c-memory

```c
int *intptr = NULL;
void *dvoidptr = &intptr; /* 6.3.2.3 (1) */
*(void **) dvoidptr = malloc(sizeof *intptr);
```

*(void *) dvoidptr = malloc(sizeof *intptr); 沒問題
*(void **) dvoidptr = malloc(sizeof *intptr); 不保證


```c
void *p = ...;
void *p2 = p + 1; /* what exactly is the size of void? */

```

void *p2 = p + 1; 因為 void 不知道要一個單位要幾個 byte


memory allcateion (記憶體配置)為 overcommit


stack allocation

    alloca 是將記憶體配置到 stack, alloca 不需要執行 free

heap allocation

    malloc 是將記憶體配置到 heap

slab allocator


demand paging

    mlock() - lock/unlock memory

    madvise() - give adivce about use of memory


---

## ref

[你所不知道的 C 語言：記憶體管理、對齊及硬體特性](https://hackmd.io/@sysprog/c-memory)
