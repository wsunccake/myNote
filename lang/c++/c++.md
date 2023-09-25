# C++

---

## content

- [simple](#simple)
  - [hello](#hello)
  - [example](#example)
- [operator](#operator)
  - [arithmetic operator](#arithmetic-operator)
  - [relational operator](#relational-operator)
  - [logical operator](#logical-operator)
  - [++]
- [data type](#data-type)
  - [primitive built-in type](#primitive-built-in-type)
  - [typedef](#typedef)
  - [enum](#enum)
  - [data convert / casting](#data-convert--casting)
- [decision](#decision)
  - [if](#if)
  - [switch](#switch)
  - [goto](#goto)
- [loop]($loop)
  - [for](#for)
  - [while](#while)
  - [do while](#do-while)
- [function](#function)
  - [scope](#scope)
  - [call by value / address / reference](#call-by-value--address--reference)
- [class](#class)
  - [explicit casting](#explicit-casting)
  - [implicit casting](#implicit-casting)

---

## simple

### hello

```cpp
// hello.cpp
#include <iostream>
using namespace std;

int main()
{
    cout << "hello";
    return 0;
}
```

```text
#include <iostream>
    iostream header

using namespace std;
    namespace

int main()

cout << "hello"
    console out
    stream insertion operator

return 0;
    0 exit code
```

```cpp
// hi.cpp
#include <iostream>

int main()
{
    std::cout << "hi";
    return 0;
}
```

```text
    std::cout << "hi";
```

```bash
linux:~ $ g++ -o hello hello.cpp
```

### example

```cpp
#include <iostream>

int main()
{
    int number1;
    int number2;
    int sum = 0; // initialize
    // int sum{0};

    std::cout << "first number: ";
    std::cin >> number1;

    std::cout << "second number:";
    std::cin >> number2;

    sum = number1 + number2;
    std::cout << "sum: " << sum << std::endl;

    return 0;
}
```

```makefile
CPP=/usr/bin/g++
CPPFLAGS=-g

.SUFFIX : .cpp .o

my ?= main
my_objs =

.cpp .o :
	@echo "compile ..."
	$(CPP) $(CPPFLAGS) -c $<

${my}.exe: ${my}.o
	@echo "build ..."
	$(CPP) $(CPPFLAGS) -o ${my}.exe ${my}.o

.PHONY: run
run: ${my}.exe
	./${my}.exe

.PHONY: run_all
run_all:
	-@for n in $(my_objs); do \
		echo $$n;\
		make my=$$n run;\
	done

.PHONY: clean
clean:
	-rm *.o
	-rm *.exe
	-rm *.so
```

```text
>>
    stream extraction operator

<<
    stream insertion operator

expression

statement

```

## operator

### arithmetic operator

```text
()
*, /, %
+, -
```

### relational operator

```text
>, <, >=, <=
==, !=
```

### logical operator

```text
&&
||
!
```

[C++ Operator Precedence](https://en.cppreference.com/w/cpp/language/operator_precedence)

### ++

```cpp
#include <iostream>
using namespace std;

int main()
{
int c;

    // c++
    c = 0;
    cout << "c: " << c << endl;
    cout << "c++: " << c++ << endl;
    cout << "c: " << c << endl;

    // ++c
    c = 0;
    cout << "c: " << c << endl;
    cout << "++c: " << ++c << endl;
    cout << "c: " << c << endl;

    // c+c++
    c = 0;
    cout << "c: " << c << endl;
    cout << "c+c++: " << c + c++ << endl;
    cout << "c: " << c << endl;

    // c+++c
    c = 0;
    cout << "c: " << c << endl;
    cout << "c+++c: " << c++ + c << endl;
    cout << "c: " << c << endl;

    // c+++c++
    c = 0;
    cout << "c: " << c << endl;
    cout << "c+++c++: " << c++ + c++ << endl;
    cout << "c: " << c << endl;

    // c+++c+c+c++;
    c = 0;
    cout << "c: " << c << endl;
    cout << "c+++c+c+c++: " << c++ + c + c + c++ << endl;
    cout << "c: " << c << endl;

    return 0;
}
```

---

## data type

### primitive built-in type

```text
char	                1byte	        -127 to 127 or 0 to 255
unsigned char	        1byte	        0 to 255
signed char	            1byte	        -127 to 127
int	                    4bytes	        -2147483648 to 2147483647
unsigned int	        4bytes	        0 to 4294967295
signed int	            4bytes	        -2147483648 to 2147483647
short int	            2bytes	        -32768 to 32767
unsigned short int	    2bytes	        0 to 65,535
signed short int	    2bytes	        -32768 to 32767
long int	            8bytes	        -9223372036854775808 to 9223372036854775807
signed long int	        8bytes	        same as long int
unsigned long int	    8bytes	        0 to 18446744073709551615
long long int	        8bytes	        -(2^63) to (2^63)-1
unsigned long long int	8bytes	        0 to 18,446,744,073,709,551,615
float	                4bytes
double	                8bytes
long double	            12bytes
wchar_t	                2 or 4 bytes    1 wide character
```

```cpp
#include <iostream>
#include <limits>

using namespace std;

int main()
{
   cout << "Size of char : " << sizeof(char) << endl;
   cout << "Size of int : " << sizeof(int) << endl;
   cout << "Size of short int : " << sizeof(short int) << endl;
   cout << "Size of long int : " << sizeof(long int) << endl;
   cout << "Size of float : " << sizeof(float) << endl;
   cout << "Size of double : " << sizeof(double) << endl;
   cout << "Size of wchar_t : " << sizeof(wchar_t) << endl;

   cout << "Int Min " << numeric_limits<int>::min() << endl;
   cout << "Int Max " << numeric_limits<int>::max() << endl;
   cout << "Unsigned Int  Min " << numeric_limits<unsigned int>::min() << endl;
   cout << "Unsigned Int Max " << numeric_limits<unsigned int>::max() << endl;
   cout << "Long Int Min " << numeric_limits<long int>::min() << endl;
   cout << "Long Int Max " << numeric_limits<long int>::max() << endl;

   cout << "Unsigned Long Int Min " << numeric_limits<unsigned long int>::min() << endl;
   cout << "Unsigned Long Int Max " << numeric_limits<unsigned long int>::max() << endl;

   return 0;
}
```

### typedef

```cpp
   typedef int feet;
   feet length = 3;
   feet width = 1;
   cout << "area: " << length * width << endl;
```

### enum

```cpp
   enum color { red=1, green, blue };
   color c = blue;
   cout << c << endl;
```

### data convert / casting

```cpp
#include <iostream>
using namespace std;

int main()
{
    float x = 33767.6;

    // implicit convert
    int i1 = x + 1;
    cout << "i1: " << i1 << endl;

    // explicit convert
    int i2 = (int)x + 1;
    cout << "i2: " << i2 << endl;

    // cast operator
    int i3 = static_cast<int>(x) + 1;
    cout << "i3: " << i3 << endl;

    short s1 = x + 1;
    cout << "s1: " << s1 << endl;

    short s2 = (short)x + 1;
    cout << "s2: " << s2 << endl;

    short s3 = static_cast<short>(x) + 1;
    cout << "s3: " << s3 << endl;
    return 0;
}
```

---

## decision

### if

```cpp
#include <iostream>
using namespace std;

int main()
{
    char sex;
    cout << "input m/f:";
    cin >> sex;
    cout << "your input: " << sex << endl;

    if (sex == 'm')
    {
        cout << "male\n";
    }
    else if (sex == 'f')
    {
        cout << "female\n";
    }
    else
    {
        cout << "unknown\n";
    }

    // single statemnet without block
    if (sex == 'm')
        cout << "male\n";
    else if (sex == 'f')
        cout << "female\n";
    else
        cout << "unknown\n";

    // ternary operator
    int i = (sex == 'm' ? 1 : 0);
    // int i;
    // if (sex == 'm')
    //     i = 1;
    // else
    //     i = 0;
    cout << i << endl;

    // default 0
    if (!0)
        printf("!0 is true\n");

    // default NULL
    if (!NULL)
        printf("!NULL is true\n");

    return 0;
}
```

### switch

```cpp
#include <iostream>

using namespace std;

int main()
{
    char sex;
    cout << "input m/f:";
    cin >> sex;
    cout << "your input: "<< sex << endl;

    switch (sex)
    {
    case 'm':
    case 'M':
        cout << "male\n";
        break;
    case 'f':
    case 'F':
        cout << "female\n";
        break;
    default:
        cout << "unknown\n";
        break;
    }

    return 0;
}
```

### goto

---

## loop

### for

```cpp
#include <iostream>
using namespace std;

int main()
{
    const int MAX = 5;

    for (int i = 0; i < MAX; i++)
    {
        cout << i << endl;
    }

    return 0;
}
```

```cpp
#include <iostream>
using namespace std;

int main()
{
    const int MAX = 5;

    int i = 0;
    // infinite loop
    for (;;)
    {
        if (i > MAX)
        {
            break;
        }
        i++;
        cout << i << endl;
    }

    return 0;
}
```

### while

```cpp
#include <iostream>
using namespace std;

int main()
{
    const int MAX = 5;

    int i = 0;
    while (i < MAX)
    {
        i++;
        cout << i << endl;
    }

    return 0;
}
```

### do while

```cpp
#include <iostream>
using namespace std;

int main()
{
    const int MAX = 5;

    int i = 0;
    do
    {
        i++;
        cout << i << endl;
    } while (i < MAX);

    return 0;
}
```

---

## function

```cpp
#include <iostream>
using namespace std;

// function declare
int max(int num1, int num2);

int main()
{
    cout << "max: " << max(5, 10) << endl;
    return 0;
}

int max(int num1, int num2)
{
    return (num1 > num2) ? num1 : num2;
}
```

### scope

```cpp
#include <iostream>
using namespace std;

// global variable declaration
int g = 200;
int G = 100;

int main()
{
    // local variable declaration
    int g = 10;
    int l = 9;
    int v = 9;
    cout << "main g :" << g << endl;
    cout << "main l :" << l << endl;
    cout << "main v :" << v << endl;

    // still global variable
    cout << "main G: " << G << endl;

    {
        int v = -1;
        cout << "{v} :" << v << endl;
        cout << "{l} :" << l << endl;
        cout << "{g} :" << g << endl;
        l = 0;
    }

    cout << "main l :" << l << endl;
    cout << "main v :" << v << endl;

    return 0;
}
```

### call by value / address / reference

```cpp
#include <iostream>
using namespace std;

// call by value
void swap1(int x, int y)
{
    int temp;
    temp = x;
    x = y;
    y = temp;
    return;
}

// call by address
void swap2(int *x, int *y)
{
    int temp;
    temp = *x;
    *x = *y;
    *y = temp;
    return;
}

// call by reference
void swap3(int &x, int &y)
{
    int temp;
    temp = x;
    x = y;
    y = temp;
    return;
}

int main()
{
    int a1 = 1, b1 = 9;
    cout << "before swap1 a: " << a1 << " b: " << b1 << endl;
    swap1(a1, b1);
    cout << "after  swap1 a: " << a1 << " b: " << b1 << endl;

    int a2 = 1, b2 = 9;
    cout << "before swap2 a: " << a2 << " b: " << b2 << endl;
    swap2(&a2, &b2);
    cout << "after  swap2 a: " << a2 << " b: " << b2 << endl;

    int a3 = 1, b3 = 9;
    cout << "before swap3 a: " << a3 << " b: " << b3 << endl;
    swap3(a3, b3);
    cout << "after  swap3 a: " << a3 << " b: " << b3 << endl;

    return 0;
}
```

### default value

```cpp
#include <iostream>
using namespace std;

void hello(string name = "c++")
{
    cout << "hello " << name << endl;
    return;
}

int main()
{
    string name = "world";
    hello(name);
    hello();

    return 0;
}
```

---

## class

### explicit casting

```cpp
#include <iostream>
using namespace std;

class Money
{
public:
    Money() : amount{0.0} {};
    Money(double _amount) : amount{_amount} {};

    // explicit casting operator
    explicit operator double() const { return amount; }

private:
    double amount;
};

void BuySomething(double amount)
{
    cout << "pay money: " << amount << endl;
}

int main()
{
    Money money(500.0);

    // not support implicit casting
    // BuySomething(money);

    // explicit casting
    BuySomething(static_cast<double>(money));
    BuySomething((double)money);
    BuySomething(double(money));
    BuySomething(double{money});

    // directly call operator
    BuySomething(money.operator double());
}
```

### implicit casting

```cpp
#include <iostream>
using namespace std;

class Cash
{
public:
    Cash() : amount{0.0} {};
    Cash(double _amount) : amount{_amount} {};

    // implicit casting operator
    operator double() const { return amount; }

private:
    double amount;
};

void BuySomething(double amount)
{
    cout << "pay: " << amount << endl;
}

int main()
{
    Cash cash(500.0);

    // implicit casting
    BuySomething(cash);

    // explicit casting
    BuySomething(static_cast<double>(cash));
    BuySomething((double)cash);
    BuySomething(double(cash));
    BuySomething(double{cash});

    // directly call operator
    BuySomething(cash.operator double());
}
```
