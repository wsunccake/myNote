# C


## hello

```c
#include <stdio.h>

int main() {
   /* my first program in C */
   printf("Hello, World! \n");
   
   return 0;
}
```

```bash
linux:~ # gcc hello.c -o hello
linux:~ # ./hello
```


---

## data type

```c
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <float.h>

int main(int argc, char** argv) {
    printf("CHAR_BIT    :   %d\n", CHAR_BIT);
    printf("CHAR_MAX    :   %d\n", CHAR_MAX);
    printf("CHAR_MIN    :   %d\n", CHAR_MIN);
    printf("INT_MAX     :   %d\n", INT_MAX);
    printf("INT_MIN     :   %d\n", INT_MIN);
    printf("LONG_MAX    :   %ld\n", (long) LONG_MAX);
    printf("LONG_MIN    :   %ld\n", (long) LONG_MIN);
    printf("SCHAR_MAX   :   %d\n", SCHAR_MAX);
    printf("SCHAR_MIN   :   %d\n", SCHAR_MIN);
    printf("SHRT_MAX    :   %d\n", SHRT_MAX);
    printf("SHRT_MIN    :   %d\n", SHRT_MIN);
    printf("UCHAR_MAX   :   %d\n", UCHAR_MAX);
    printf("UINT_MAX    :   %u\n", (unsigned int) UINT_MAX);
    printf("ULONG_MAX   :   %lu\n", (unsigned long) ULONG_MAX);
    printf("USHRT_MAX   :   %d\n", (unsigned short) USHRT_MAX);

    printf("Storage size for float : %d \n", sizeof(float));
    printf("FLT_MAX     :   %g\n", (float) FLT_MAX);
    printf("FLT_MIN     :   %g\n", (float) FLT_MIN);
    printf("-FLT_MAX    :   %g\n", (float) -FLT_MAX);
    printf("-FLT_MIN    :   %g\n", (float) -FLT_MIN);
    printf("DBL_MAX     :   %g\n", (double) DBL_MAX);
    printf("DBL_MIN     :   %g\n", (double) DBL_MIN);
    printf("-DBL_MAX     :  %g\n", (double) -DBL_MAX);
    printf("Precision value: %d\n", FLT_DIG );
    return 0;
}
```

```c
#include <stdio.h>

int main () {
   char c1;
   c1 = 'c';
   char c2 = 'C';
   char c3 = c2;
//   char c4 = "Z";
   printf("char c1: %c, c2: %c, c3: %c \n", c1, c2, c3);

   int i1 = 1;
   int i2 = 10;
   int i3 = i2 - i1;
   printf("int i1: %d, i2: %d, i3: %d\n", i1, i2, i3);

   int i4 = 16.9;
   int i5 = 016;
   int i6 = 0x16;
   printf("int i4: %d, i5: %d, i6: %d\n", i4, i5, i6);
   
   int i7 = 2567;
   printf("dec: %d, occ: %o, hex: %x\n", i7, i7, i7);

   return 0;
}
```

```c
#include <stdio.h>
 
int main () {
    int i, j;
    
    i = 1, j = 0;
    printf("i: %d, j: %d\n", i, j);
    j = i++;
    printf("i: %d, j: %d\n", i, j);

    i = 1, j = 0;
    printf("i: %d, j: %d\n", i, j);
    j = ++i;
    printf("i: %d, j: %d\n", i, j);    
    return 0;
}
```


---

## condition


### if

```c
#include <stdio.h>

int main () {
    char sex;
    printf("input m/f:");
    scanf("%c",&sex);
    printf("your input: %c\n", sex);

    if (sex == 'm') {
        printf("male\n");
    } else if (sex == 'f') {
        printf("female\n");
    } else {
        printf("unknown\n");
    }
    
    int i = (sex == 'm' ? 1 : 0);
    printf("%d\n", i);
    return 0;
}
```


### switch

```c
#include <stdio.h>

int main () {
    char sex;
    printf("input m/f:");
    scanf("%c",&sex);
    printf("your input: %c\n", sex);

    switch(sex) {
    case 'm':
    case 'M':
        printf("male\n");
        break;
    case 'f':
    case 'F':
        printf("female\n");
        break;
    default:
        printf("unknown\n");
        break;
    }

    return 0;
}
```


---

## loop

### for

```c
#include <stdio.h>
 
int main () {
   const int MAX = 5;

   for (int i = 0; i < MAX; i++ ) {
      printf("%d\n", i);
   }

   return 0;
}
```

```c
#include <stdio.h>
 
int main () {
   const int MAX = 5;
   
   int i = 0
   for ( ; ; ) {
        printf("%d\n", i);
        if (i > MAX) {
            break;
        }
        i++;
   }

   return 0;
}
```


### while

```c
#include <stdio.h>
 
int main () {
   const int MAX = 5;
   
   int i = 0
   while (i < MAX) {
      printf("%d\n", i);
      i++;
   }

   return 0;
}
```

```c
#include <stdio.h>
 
int main () {
   const int MAX = 5;
   
   int i = 0;
   do {
      printf("%d\n", i);
      i++;
   } while (i < MAX);

   return 0;
}
```


### goto

```c
#include <stdio.h>
 
int main () {
   const int MAX = 5;

   int i = 0;
   LOOP:
   printf("%d\n", i);
   i++;
   if (i < MAX) {
      goto LOOP;
   }

   return 0;
}
```


---

## function

```c
#include <stdio.h>

int max(int num1, int num2);
 
int main () {
   printf("max: %d\n", max(5, 10)); 
   return 0;
}
 
int max(int num1, int num2) {
   int result;
 
   if (num1 > num2)
      result = num1;
   else
      result = num2;
 
   return result; 
}
```

```c
#include <stdio.h>

// call by value
void swap1(int x, int y) {
   int temp;
   temp = x;
   x = y;
   y = temp;
   return;
}

// call by reference
void swap2(int *x, int *y) {
   int temp;
   temp = *x;
   *x = *y;
   *y = temp;
   return;
}

int main () {
   int a = 100;
   int b = 200;
 
   printf("before swap, a : %d, b: %d\n", a, b);
   swap1(a, b);
   printf("after swap, a : %d, b: %d\n", a, b);
 
   printf("before swap, a : %d, b: %d\n", a, b);
   swap2(&a, &b);
   printf("after swap, a : %d, b: %d\n", a, b);
}
```


---

## array

```c
#include <stdio.h>

int main () {
   int arr1[3]={1, 2, 3};
   int arr2[]={1, 2, 3};
   int arr3[3];
   arr3[0]=1, arr3[1]=2, arr3[2]=3;

   printf("arr1[0]: %d, len: %d\n", arr1[0], sizeof(arr1) / sizeof(arr1[0]));
   int i = 0;
   for (i; i < 3; i++) {
      printf("arr2[%d]: %d\n", i, arr2[i]);
   }

   return 0;
}
```


### function

```c
#include <stdio.h>

void showArray(int array[], int size) {
   int i = 0;
   for (i; i < size; i++)
      printf("array[%d]: %d\n", i, array[i]);
}

int main () {
   int arr1[]={1, 2, 3};   
   showArray(arr1, 3);
   return 0;
}
```


### 2d

```c
#include <stdio.h>

int main () {
   int arr2d[2][3] = {{1, 2, 3}, {7, 8, 9}};
   printf("arr2d[0][2]: %d\n", arr2d[0][2]);
   return 0;
}
```


---

## pointer

```c
#include <stdio.h>

int main () {
   int var = 20;
   int *ptr1 = &var;
   int *ptr2;
   ptr2 = &var;
   // int *ptr3;
   // *ptr3 = var;
   printf("&var: %x, ptr1: %x, ptr2: %x\n", &var, ptr1, ptr2);
   printf("var: %d, *ptr1: %d, *ptr2: %d\n", var, *ptr1, ptr2);
   *ptr = 1;
   printf("var: %d, *ptr1: %d, *ptr2: %d\n", var, *ptr1, ptr2);

   return 0;
}
```

```c
// array of pointer
char *ptr[3];
char *(ptr[3]);

// pointer to array
int (* ptr)[5] = NULL;

// pointer to pointer
int **ptr;


```


### array

```c
#include <stdio.h>

int main () {
  int *ptr = NULL;
  int arr[] = {1, 2, 3};
  int *ptr1 = arr;
  int *ptr2;
  ptr2 = arr;
  int *ptr3;
  ptr3 = &arr[0];

  int i;
  for (i = 0; i < 3; i++) {
      printf("&arr[%d]: %d, ptr1: %d, ptr2: %d, ptr3: %d\n", i, &arr[i], ptr1, ptr2, ptr3);
      printf("arr[%d]: %d, *ptr1: %d, *ptr2: %d, *ptr3: %d\n", i, arr[i], *ptr1, *ptr2, *ptr3);
      ptr1++, ptr2++, ptr3++;
  }

  return 0;
}
```


### function

```c
#include <stdio.h>

void showPointer(int *ptr, int size) {
   int i = 0;
   for (i; i < size; i++) {
      printf("i: %d, ptr: %d, *ptr: %d\n", i, ptr, *ptr);
      ptr++;
   }
}

int *addArray1(int arr1[], int arr2[], int size) {
    int i;
    int res[size];
    for (i = 0; i < size; i++) {
        res[i] = arr1[i] + arr2[i];
        printf("&arr1[%d]: %d, &arr2[%d]: %d, &res[%d]: %d\n", i, &arr1[i], i, &arr2[i], i, &res[i]);
        printf("arr1[%d]: %d, arr2[%d]: %d, res[%d]: %d\n", i, arr1[i], i, arr2[i], i, res[i]);
    }
    
    return res;
}

int *addArray2(int arr1[], int arr2[], int size) {
    int i;
    int *res = malloc(size);
    for (i = 0; i < size; i++) {
        res[i] = arr1[i] + arr2[i];
        printf("&arr1[%d]: %d, &arr2[%d]: %d, &res[%d]: %d\n", i, &arr1[i], i, &arr2[i], i, &res[i]);
        printf("arr1[%d]: %d, arr2[%d]: %d, res[%d]: %d\n", i, arr1[i], i, arr2[i], i, res[i]);
    }
    
    return res;
}

int main () {
   int arr1[]={1, 2, 3};
   int arr2[]={9, 8, 7};

   int *ptr1= addArray1(arr1, arr2, 3);
   printf("ptr1: %d\n", ptr1);
   showPointer(ptr1, 3);

   int *ptr2;
   ptr2 = addArray1(arr1, arr2, 3);
   printf("ptr2: %d\n", ptr2);
   showPointer(ptr2, 3);

   ptr2 = addArray2(arr1, arr2, 3);
   printf("ptr2: %d\n", ptr2);
   showPointer(ptr2, 3);

   return 0;
}
```


### array of pointer

```c
#include <stdio.h>

int main () {
   char *name1 = "LPJ";
   printf("%s\n", name1);
   name1 = &"JoJo";
   printf("%s\n", name1);

   char name2[] = "Fin";
   printf("%s\n", name2);
   name2[0] = 'A';
   name2[1] = 'l';
   name2[2] = 'i';
//   name2[3] = 'b';
   printf("%s\n", name2);

   char *names[] = {
      "Zara",
      "Sara",
      name1,
      name2
   };

   int i = 0;
   for ( i = 0; i < 4; i++) {
      printf("names[%d] = %s\n", i, names[i] );
   }

   return 0;
}
```


### pointer to array

```c
int main() 
{ 
  int arr[] = { 3, 5, 6, 7, 9 };
  int *p = arr;
  int (*ptr)[5] = &arr;

  printf("p = %p, ptr = %p\n", p, ptr);
  printf("*p = %d, *ptr = %p\n", *p, *ptr);
  printf("sizeof(p) = %lu, sizeof(*p) = %lu\n", sizeof(p), sizeof(*p)); 
  printf("sizeof(ptr) = %lu, sizeof(*ptr) = %lu\n", sizeof(ptr), sizeof(*ptr)); 

  return 0; 
} 
```


### pointer to pointer

```c
#include <stdio.h>

int g = 999;

void change1(int a) {
    a = 1;
}

void change2(int *p) {
    *p = 1;
}

void change3(int *p) {
    *p = g;
}

void change4(int *p) {
    p = &g;
}

void change5(int **ptp) {
    *ptp = &g;
}

int main () {
   int a1 = 100;
   printf("Before a1 : %d\n", a1);
   change1(a1);
   printf("After a1 : %d\n", a1);

   int v1 = 100;
   int *p1 = &v1;
   printf("Before v1: %d, p1: %d, *p1:%d\n", v1, p1, *p1);
   change1(*p1);
   printf("After v1: %d, p1: %d, *p1:%d\n", v1, p1, *p1);


   int a2 = 100;
   printf("Before a2 : %d\n", a2);
   change2(&a2);
   printf("After a2 : %d\n", a2);

   int v2 = 100;
   int *p2 = &v2;
   printf("Before v2: %d, p2: %d, *p2:%d\n", v2, p2, *p2);
   change2(p2);
   printf("After v2: %d, p2: %d, *p2:%d\n", v2, p2, *p2);


   int a3 = 100;
   printf("Before a3 : %d\n", a3);
   change3(&a3);
   printf("After a3 : %d\n", a3);

   int v3 = 100;
   int *p3 = &v3;
   printf("Before v3: %d, p3: %d, *p3:%d\n", v3, p3, *p3);
   change3(p3);
   printf("After v3: %d, p3: %d, *p3:%d\n", v3, p3, *p3);


   int a4 = 100;
   printf("Before a4 : %d\n", a4);
   change4(&a4);
   printf("After a4 : %d\n", a4);

   int v4 = 100;
   int *p4 = &v4;
   printf("Before v4: %d, p4: %d, *p4:%d\n", v4, p4, *p4);
   change4(p4);
   printf("After v4: %d, p4: %d, *p4:%d\n", v4, p4, *p4);


   printf("g: %d, &g: %d\n", g, &g);
   
   int v5 = 100;
   int *p5 = &v5;
   printf("Before v5: %d, p5: %d, *p5:%d\n", v5, p5, *p5);
   change5(&p5);
   printf("After v5: %d, p5: %d, *p5:%d\n", v5, p5, *p5);

   return 0;
}
```


### function pointer

```c
int sum (int num1, int num2)
{
   return num1+num2;
}

int main()
{
   int (*f2p) (int, int);
   f2p = sum;
   
   int op1 = f2p(10, 13);
   int op2 = sum(10, 13);
   
   printf("function pointer: %d\n",op1);
   printf("function: %d\n", op2);
   
   return 0;
}
```


---

## string

```c
#include <stdio.h>

int main () {
   char h1[6] = {'h', 'e', 'l', 'l', 'o', '\0'};
   char h2[] = "hello";
   printf("h1: %s, h2: %s\n", h1, h2);
   
   int i;
   for (i = 0; i < 6; i++) {
      if (h1[i] == h2[i]) {
         printf("h1: %x == h2: %x\n", h1[i], h2[i]);
      } else {
         printf("h1: %x != h2: %x\n", h1[i], h2[i]);    
      } 
   }

   return 0;
}
```

```c
#include <stdio.h>
#include <string.h>

int main () {
   char str1[12] = "Hello";
   char str2[12] = "World";
   char str3[12];
   int  len ;

   strcpy(str3, str1);
   printf("strcpy( str3, str1) :  %s\n", str3);

   strcat(str1, str2);
   printf("strcat( str1, str2):   %s\n", str1);

   len = strlen(str1);
   printf("strlen(str1) :  %d\n", len);

   return 0;
}
```


---

## struct

```c
#include <stdio.h>
#include <string.h>
 
struct Employee  
{
   char name[50];
   float salary;
};

struct Book
{
   int id;  
   char name[50];  
} b1, b2;


void adjustSalary1(struct Employee e) {
   e.salary = 1.1 * e.salary;
}

void adjustSalary2(struct Employee *e) {
   e->salary = 1.1 * e->salary;
}
 
int main( ) {
   b1.id = 1;
   strcpy(b1.name, "Learn C");
   printf("book id: %d, name: %s\n", b1.id, b1.name);
    
   struct Employee e1;
   strcpy(e1.name, "LPJ");
   e1.salary = 10;
   printf("name: %s, salary: %f\n", e1.name, e1.salary);
    
   adjustSalary1(e1);
   printf("name: %s, salary: %f\n", e1.name, e1.salary);

   adjustSalary2(&e1);
   printf("name: %s, salary: %f\n", e1.name, e1.salary);

   return 0;
}
```


---

## union

```c
#include <stdio.h>
#include <string.h>
 
union Data {
   int i;
   float f;
   char str[20];
};
 
int main( ) {
   union Data data;        

   data.i = 10;
   data.f = 220.5;
   strcpy( data.str, "C Programming");

   printf( "data.i : %d\n", data.i);
   printf( "data.f : %f\n", data.f);
   printf( "data.str : %s\n", data.str);

   data.i = 10;
   printf( "data.i : %d\n", data.i);
   
   data.f = 220.5;
   printf( "data.f : %f\n", data.f);
   
   strcpy( data.str, "C Programming");
   printf( "data.str : %s\n", data.str);
   return 0;
}
```

---

## file


---

## preprocessor

```c
#include <stdio.h>
#include <string.h>
 
#define PI 3.14  
#define MIN(a,b) ((a)<(b)?(a):(b))    

 
int main( ) {
   float r = 10.0;
   printf("circle area: %f\n", PI * r * r);
   printf("min(1, -1): %d\n", MIN(1, -1));
    
   printf("File :%s\n", __FILE__ );    
   printf("Date :%s\n", __DATE__ );    
   printf("Time :%s\n", __TIME__ );    
   printf("Line :%d\n", __LINE__ );    
   printf("STDC :%d\n", __STDC__ );  

   return 0;
}
```

```c
#include <stdio.h>

int main() {
#ifdef x86_64
  char Arch[]="x86_64";
#elif ia32
  char Arch[]="ia32";
#else
  char Arch[]="Unknown";
#endif

  printf("Architecture: %s\n", Arch);
  return 1;
}
```

```bash
# ia32
linux:~ # gcc -Dia32 -o ia32.exe test.c

# x86_64
linux:~ # gcc -Dx86_64 -E test.c > _test.c
linux:~ # gcc -o x86_64.exe _test.c
```


---

## header


---

## error


---

## memory
