# cmake

---

## content

- [install](#install)
- [basic](#basic)
  - [set](#set)
  - [if](#if)
  - [foreach](#foreach)
  - [while](#while)
  - [macro](#macro)
  - [function](#function)
- [build](#build)
  - [in-place build](#in-place-build)
  - [out-place build](#out-place-build)
- [sample](#sample)
  - [hello](#hello)

---

## install

```bash
# for rhel / centos
centos:~ # dnf install cmake

# for debian / ubuntu
ubuntu:~ # apt install cmake
```

---

## basic

### set

```cmake
# CMakeLists.txt
set(xxx a b c d)
message("hello ${xxx}")
set(xxx e;f;g;h)
message("hi ${xxx}")
```

```bash
linux:~ $ cmake CMakeLists.txt
linux:~ $ cmake .
```

### if

```cmake
# CMakeLists.txt
if ( NOT DEFINED test)
    message("Use: cmake -Dtest:STRING=val to test")
elseif(${test} STREQUAL yes)
    message("if: ${test}")
elseif(${test} STREQUAL test1)
    message("else if: ${test}")
else()
    message("else: ${test}")
endif()
```

```bash
linux:~ $ cmake -Dtest:yes CMakeLists.txt
linux:~ $ cmake -Dtest:yes .
```

### foreach

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8)

set(xxx e;f;g;h)

foreach(i ${xxx})
    message(${i})
endforeach()
```

### while

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8)

set(i 0)
while(i LESS 10)
    message(${i})
    math(EXPR i "${i} + 1")
endwhile()
```

### macro

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 2.8)

macro(mac_print msg)
    set(mac "macro")
    message("${mac}: ${msg}")
endmacro(mac_print)

mac_print("test macro")
message("check var in macro: ${mac}")
```

### function

```cmake
# CMakeLists.txt
function(func_print msg)
    set (func "func")
    message("${func}: ${msg}")
endfunction(func_print)

func_print("test function")
message("check var in function: ${func}")
```

---

## build

### in-place build

```bash
linux:~/project $ ls CMakeLists.txt
linux:~/project $ cmake .
linux:~/project $ make
```

### out-place build

```bash
linux:~/project $ ls CMakeLists.txt
linux:~/project $ mkdir build
linux:~/project $ cd build
linux:~/project/build $ cmake ../
linux:~/project/build $ make
```

---

## sample

### hello

```cpp
// hello.cpp
#include <iostream>
using namespace std;

int main()
{
    cout << "hello\n";
    return 0;
}
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.12)
project(project)

# add_executable(hello.exe hello.cpp)

add_executable(hello.exe)
target_sources(hello.exe PRIVATE hello.cpp)
```

```bash
linux:~/project $ tree
.
├── CMakeLists.txt
└── hello.cpp

linux:~/project $ cmake .
linux:~/project $ make
linux:~/project $ ./hello.exe
```
