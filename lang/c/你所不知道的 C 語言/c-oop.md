# c-oop

## data encapsulation

```c
#include <stdio.h>
#include <stdlib.h>

/* forward declaration */
typedef struct object Object;
typedef int (*func_t)(Object *);

struct object {
    int a, b;
    func_t add, sub;
};

static int add_impl(Object *self) { // method
    return self->a + self->b;
}
static int sub_impl(Object *self) { // method
    return self->a - self->b;
}

// & : address of
// * : value of // indirect access
int init_object(Object **self) { // call-by-value
    if (NULL == (*self = malloc(sizeof(Object)))) return -1;
    (*self)->a = 0; (*self)->b = 0;
    (*self)->add = add_impl; (*self)->sub = sub_impl;
    return 0;
}

int main(int argc, char *argv[])
{
    Object *o = NULL;
    init_object(&o);
    o->a = 9922; o->b = 5566;
    printf("add = %d, sub = %d\n", o->add(o), o->sub(o));
    return 0;
}
```