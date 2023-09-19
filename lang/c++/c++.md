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
- [data type](#data-type)
  - [primitive built-in type](#primitive-built-in-type)
  - [typedef](#typedef)
  - [enum](#enum)

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
    int sum;

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
