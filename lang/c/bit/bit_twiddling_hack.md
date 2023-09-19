# bit twiddling hack

---

## content

- [compute sign](#compute-sign)
- [opposite sign](#opposite-sign)
- [compute integer absolute value](#compute-integer-absolute-value)
- [max and min](#max-and-min)

---

## compute sign

```c
#include <stdio.h>
#include <limits.h>

void compute_sign_zero_or_minus(int v)
{
    int sign;

    sign = (v < 0 ? -1 : 0);
    printf("%d\n", sign);

    sign = -(v < 0);
    printf("%d\n", sign);

    // CHAR_BIT is the number of bits per byte (normally 8)
    sign = -(int)((unsigned int)((int)v) >> (sizeof(int) * CHAR_BIT - 1));
    printf("%d\n", sign);

    // one less instruction (but not portable)
    sign = v >> (sizeof(int) * CHAR_BIT - 1);
    printf("%d\n", sign);
}

void compute_sign_plus_or_minus(int v)
{
    int sign;

    sign = (v < 0 ? -1 : 1);
    printf("%d\n", sign);

    sign = +1 | (v >> (sizeof(int) * CHAR_BIT - 1));
    printf("%d\n", sign);
}

void compute_sign_plus_or_zero_or_minus(int v)
{
    int sign;
    if (v == 0)
    {
        sign = 0;
    }
    else if (v > 0)
    {
        sign = 1;
    }
    else
    {
        sign = -1;
    }
    printf("%d\n", sign);

    sign = (v != 0) | -(int)((unsigned int)((int)v) >> (sizeof(int) * CHAR_BIT - 1));
    printf("%d\n", sign);

    // more speed but less portability
    sign = (v != 0) | (v >> (sizeof(int) * CHAR_BIT - 1)); // -1, 0, or +1
    printf("%d\n", sign);

    // portability, brevity, and (perhaps) speed:
    sign = (v > 0) - (v < 0); // -1, 0, or +1
    printf("%d\n", sign);
}

void compute_sign_plus_or_zero(int v)
{
    int sign;

    sign = v < 0 ? 0 : 1;
    printf("%d\n", sign);

    sign = 1 ^ ((unsigned int)v >> (sizeof(int) * CHAR_BIT - 1));
    printf("%d\n", sign);
}

int main()
{
    int v1 = 0;
    int v2 = 1;
    int v3 = -1;

    compute_sign_zero_or_minus(v1);
    compute_sign_zero_or_minus(v2);
    compute_sign_zero_or_minus(v3);

    compute_sign_plus_or_minus(v1);
    compute_sign_plus_or_minus(v2);
    compute_sign_plus_or_minus(v3);

    compute_sign_plus_or_zero_or_minus(v1);
    compute_sign_plus_or_zero_or_minus(v2);
    compute_sign_plus_or_zero_or_minus(v3);

    compute_sign_plus_or_zero(v1);
    compute_sign_plus_or_zero(v2);
    compute_sign_plus_or_zero(v3);

    return 0;
}
```

---

## opposite sign

```c
#include <stdio.h>
#include <stdbool.h>

// before c89
// #define BOOL int
// #define TRUE 1
// #define FALSE 0
// BOOL flag = TRUE;

// typedef enum
// {
//     TRUE = 1,
//     FALSE = 0
// } BOOL;
// BOOL flag = TRUE;

bool opposite_sign(int x, int y)
{
    bool f;

    // branch predictor
    if (x * y == 0)
    {
        if (x > 0 || y > 0)
        {
            f = false;
        }
        else
        {
            f = true;
        }
    }
    else if (x * y > 0)
    {
        f = false;
    }
    else
    {
        f = true;
    }
    printf("%s \n", f ? "true" : "false");

    f = ((x ^ y) < 0);
    printf("%s \n", f ? "true" : "false");

    return f;
}

int main()
{
    opposite_sign(1, 2);
    opposite_sign(1, 0);
    opposite_sign(1, -1);
    opposite_sign(-1, 0);
    return 0;
}
```

---

## compute integer absolute value

```c
#include <stdio.h>
#include <limits.h>

unsigned int compute_abs(int v)
{
    unsigned int r;

    r = v < 0 ? -v : v;
    printf("%d\n", r);

    // 用 sign bit + right shift 做 mask, 0 or -1
    // int const mask = v >> (sizeof(int) * CHAR_BIT - 1);
    int const mask = v >> sizeof(int) * CHAR_BIT - 1;

    r = (v + mask) ^ mask;
    printf("%d\n", r);

    r = (v ^ mask) - mask;
    printf("%d\n", r);

    return r;
}

int main()
{
    int v1 = 0;
    int v2 = 1;
    int v3 = -1;

    compute_abs(v1);
    compute_abs(v2);
    compute_abs(v3);

    return 0;
}
```

$$
\begin{aligned}
abs(x)=\left\{
                \begin{array}{ll}
                  x, & \text{if $x >= 0$} \\
                  -x, & \text{if $x < 0$} \\
                \end{array}
              \right.
=>
abs(x)=\left\{
                \begin{array}{ll}
                  x, & \text{if $x >= 0$} \\
                  \char`\~x+1, & \text{if $x < 0$} \\
                \end{array}
              \right.
\end{aligned}
$$

---

## max and min

```c
#include <stdio.h>
#include <limits.h>

int compute_max(int x, int y)
{
    int r;

    r = x > y ? x : y;
    printf("max: %d\n", r);

    r = x ^ ((x ^ y) & -(x < y));
    printf("max: %d\n", r);

    //  INT_MIN <= x - y <= INT_MAX
    r = x - ((x - y) & ((x - y) >> (sizeof(int) * CHAR_BIT - 1)));
    printf("max: %d\n", r);

    return r;
}

int compute_min(int x, int y)
{
    int r;

    r = x > y ? y : x;
    printf("min: %d\n", r);

    r = y ^ ((x ^ y) & -(x < y));
    printf("min: %d\n", r);

    //  INT_MIN <= x - y <= INT_MAX
    r = y + ((x - y) & ((x - y) >> (sizeof(int) * CHAR_BIT - 1)));
    printf("min: %d\n", r);

    return r;
}

int main()
{
    int x = 1;
    int y = -1;

    compute_max(x, y);
    compute_min(x, y);

    return 0;
}
```
