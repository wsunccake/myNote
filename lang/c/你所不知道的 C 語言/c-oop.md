# c-oop

## content

- [encapsulation](#encapsulation)
- [inheritance](#inheritance)
- [polymorphism](#polymorphism)
- [example](#example)

---

## encapsulation

```c
#include <stdio.h>

struct Circle
{
    // member
    float r;

    // method
    void (*new)(struct Circle *, float);
    float (*area)(struct Circle *);
};

// method
float CircleAreaImp(struct Circle *obj) { return 3.14 * obj->r * obj->r; }

void CircleNewImp(struct Circle *obj, float r)
{
    obj->r = r;
}

void CircleNew(struct Circle *obj, float r)
{
    // method, function
    obj->new = CircleNewImp;
    obj->area = CircleAreaImp;

    // member, variable
    obj->r = r;
}

int main()
{
    struct Circle c;
    CircleNew(&c, 3.0);
    printf("area() = %G\n", c.area(&c));
}
```

---

## inheritance

inheritance, mixin, composition

```c
#include <stdio.h>

#define ShapeMembers(TYPE)      \
    void (*new)(struct TYPE *); \
    float (*area)(struct TYPE *)

typedef struct _Shape
{
    ShapeMembers(_Shape);
} Shape;

float ShapeArea(Shape *obj) { return 0; }

void ShapeNew(Shape *obj)
{
    obj->new = ShapeNew;
    obj->area = ShapeArea;
}

typedef struct _Circle
{
    ShapeMembers(_Circle);
    float r;
} Circle;

float CircleArea(Circle *obj) { return 3.14 * obj->r * obj->r; }

void CircleNew(Circle *obj)
{
    obj->new = CircleNew;
    obj->area = CircleArea;
}

int main()
{
    Shape s;
    ShapeNew(&s);
    printf("s.area()=%G\n", s.area(&s));

    Circle c;
    CircleNew(&c);
    c.r = 3.0;
    printf("c.area()=%G\n", c.area(&c));
}
```

---

## polymorphism

```c
#include <stdio.h>

#define ShapeText(TYPE)         \
    void (*new)(struct TYPE *); \
    float (*area)(struct TYPE *)

typedef struct _Shape
{
    ShapeText(_Shape);
} Shape;

float ShapeArea(Shape *obj) { return 0; }

void ShapeNew(Shape *obj)
{
    obj->new = ShapeNew;
    obj->area = ShapeArea;
}

typedef struct _Circle
{
    ShapeText(_Circle);
    float r;
} Circle;

float CircleArea(Circle *obj) { return 3.14 * obj->r * obj->r; }

void CircleNew(Circle *obj)
{
    obj->new = CircleNew;
    obj->area = CircleArea;
}

int main()
{
    Shape s;
    ShapeNew(&s);
    Circle c;
    CircleNew(&c);
    c.r = 3.0;
    Shape *list[] = {&s, (Shape *)&c}; // type convert
    int i;
    for (i = 0; i < 2; i++)
    {
        Shape *o = list[i];
        printf("s.area()=%G\n", o->area(o)); // run method
    }
}
```

---

## example

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
    // initial
    (*self)->a = 0;(*self)->b = 0;

    // bind method
    (*self)->add = add_impl; (*self)->sub = sub_impl;
    return 0;
}

int main(int argc, char *argv[])
{
    Object *o = NULL;
    init_object(&o);
    o->a = 9527; o->b = 5566;
    printf("add = %d, sub = %d\n", o->add(o), o->sub(o));
    free(o);

    return 0;
}
```

---

## ref

- [OOC-Design-Pattern](https://github.com/QMonkey/OOC-Design-Pattern)
