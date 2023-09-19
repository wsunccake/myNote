# kernel tip

---

## content

- [macro](#macro)
  - [offsetof](#offsetof)
  - [container_of](#container_of)
- [data](#data)

---

## macro

### offsetof

```c
// for stddef.h from linux6.1, c11 support
#define offsetof(TYPE, MEMBER)  __builtin_offsetof(TYPE, MEMBER)

// for traditional compiler
#define offsetof(TYPE, MEMBER) ((size_t) &((TYPE*)0)->MEMBER)
```

將 TYPE 為 struct st 帶入,

```c
// TYPE: struct st => (TYPE*)0
(struct st*)0 // struct pointer 指到 null
```

```c
#include <stdio.h>

#define p_offsetof(TYPE, MEMBER) ((size_t) &((TYPE*)0)->MEMBER)

struct st{
    int a;
    int b;
    char c1;
    char c2;
};

int main()
{
    printf("%p\n",&((struct st*)0)->a);
    printf("%p\n",&((struct st*)0)->b);
    printf("%p\n",&((struct st*)0)->c1);
    printf("%p\n",&((struct st*)0)->c2);
// (nil)
// 0x4
// 0x8
// 0x9

    printf("%ld\n",p_offsetof(struct st , a));
    printf("%ld\n",p_offsetof(struct st , b));
    printf("%ld\n",p_offsetof(struct st , c1));
    printf("%ld\n",p_offsetof(struct st , c2));
// 0
// 4
// 8
// 9

    return 0;
}
```

### container_of

```c
// container_of.h from linux6.1
#define container_of(ptr, type, member) ({                              \
        void *__mptr = (void *)(ptr);                                   \
        static_assert(
            (*(ptr), ((type *)0)->member) ||       \
                      __same_type(*(ptr), void),                        \
                      "pointer type mismatch in container_of()");       \
        ((type *)(__mptr - offsetof(type, member))); })

// for traditional compiler
#define container_of(ptr, type, member) ({          \
        const typeof( ((type *)0)->member ) *__mptr = (const typeof( ((type *)0)->member ) *)(ptr); \
        (type *)( (char *)__mptr - offsetof(type,member) );})
```

```c
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>

#define p_offsetof(TYPE, MEMBER) ((size_t) & ((TYPE *)0)->MEMBER)
#define container_of(ptr, type, member) ({          \
       const typeof( ((type *)0)->member ) *__mptr = (const typeof( ((type *)0)->member ) *)(ptr); \
       (type *)( (char *)__mptr - p_offsetof(type,member) ); })

struct student
{
    int age;
    char name[10];
    int id;
    unsigned long phone_num;
};

void print_all(void *p_str)
{

    struct student *stu = NULL;

    stu = container_of(p_str, struct student, age);
    // stu = container_of(p_str, struct student, id);

    printf("age:%d\n", stu->age);
    printf("name:%s\n", stu->name);
    printf("id:%d\n", stu->id);
    printf("phone_num:%ld\n", stu->phone_num);
}

int main()
{
    struct student *stu = (struct student *)malloc(sizeof(struct student));

    stu->age = 25;
    stu->id = 1;
    stu->name[0] = 'j';
    stu->name[1] = 'o';
    stu->name[2] = 'h';
    stu->name[3] = 'n';
    stu->name[4] = '\0';
    stu->phone_num = 12345;

    print_all(&stu->age);

    printf("main end\n");

    if (stu != NULL)
        free(stu);

    return 0;
}
```

---

## data

### endian

```text
0x01234567

address         0x100   0x101   0x102   0x104
                |       |       |       |
big endian      01      23      45      67
little endian   67      45      23      01
```

```c
#include <stdio.h>

int main()
{
    int a = 0x11223344;
    char b;
    b = a;

    if (b == 0x44)
        printf("little endian\n");
    else
        printf("big endian\n");

    return 0;
}
```

```c
#include <stdio.h>

union u
{
    int a;
    char b;
};

int main()
{
    union u c;
    c.a = 0x11223344;

    if (c.b == 0x44)
        printf("little endian\n");
    else
        printf("big endian\n");

    return 0;
}
```

```c
#define swap_endian_u16(A) \
    ((A & 0xFF00 > c > 8) | (A & 0x00FF << 8))
```

### signed and unsigned

```c
#include <stdio.h>

int main()
{
    signed int a = -1;
    printf("signed int -> d: %d\n", a);
    printf("signed int -> u: %u\n", a);

    unsigned int b = 0xffffffff;
    printf("unsigned int -> d: %d\n", b);
    printf("unsigned int -> u: %u\n", b);

    return 0;
}
```

### overflow

```c
#include <stdio.h>

int main()
{
    // infinite loop
    char i;
    for (i = 0; i < 130; i++)
        printf("i: %d\n", i);

    signed char c1 = 127;
    printf("signed char: %d, signed char+1: %d\n", c1, c1 + 1);
    c1++;
    printf("signed char: %d, signed char+1: %d\n", c1, c1 + 1);

    unsigned char c2 = 255;
    printf("unsigned char: %u, unsigned char+1: %u\n", c2, c2 + 1);
    c2++;
    printf("unsigned char: %u, unsigned char+1: %u\n", c2, c2 + 1);

    return 0;
}
```

```c
#include <stdio.h>
#include <limits.h>

#define isSignAddOver(a, b, c) (c) < 0 ? 1 : 0
#define isUnsignAddOver(a, b, c) ((c) < (a) || (c) < (b)) ? 1 : 0
#define isAddOver(a, b, c, d) ((a) > (d) - (b)) ? 1 : 0

#define isAddOverflow(a, x, max_value) (((x) > 0) && ((a) > (max_value) - (x))) ? 1 : 0
#define isSubOverflow(a, x, max_value) (((x) < 0) && ((a) > (max_value) + (x))) ? 1 : 0
#define isMulOverflow(a, x, max_value) ((a) > (max_value) / (x)) ? 1 : 0
#define isDivOverflow(a, x, max_value, min_value) (((x) == (max_value) + 1) && ((a) == (min_value))) ? 1 : 0

int main()
{
    signed char a1 = 127;
    signed char b1 = 30;
    signed char c1 = a1 + b1;
    if (isSignAddOver(a1, b1, c1))
        printf("overflow: %d + %d = %d (isSignAddOver)\n", a1, b1, c1);
    if (isUnsignAddOver(a1, b1, c1))
        printf("overflow: %d + %d = %d (isUnsignAddOver)\n", a1, b1, c1);
    if (isAddOver(a1, b1, c1, CHAR_MAX))
        printf("overflow: %d + %d = %d (isAddOver)\n", a1, b1, c1);

    unsigned char a2 = 255;
    unsigned char b2 = 30;
    unsigned char c2 = a2 + b2;
    if (isSignAddOver(a2, b2, c2))
        printf("overflow: %u + %u = %u (isSignAddOver)\n", a2, b2, c2);
    if (isUnsignAddOver(a2, b2, c2))
        printf("overflow: %u + %u = %u (isUnsignAddOver)\n", a2, b2, c2);
    if (isAddOver(a2, b2, c2, UCHAR_MAX))
        printf("overflow: %u + %u = %u (isAddOver)\n", a2, b2, c2);

    return 0;
}
```
