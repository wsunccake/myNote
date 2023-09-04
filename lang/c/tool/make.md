# make

## install

```bash
# for rhel / centos
centos:~ # dnf install make

# for debian / ubuntu
ubuntu:~ # apt install make
```

---

## hello

```c
// main.c
#include <stdio.h>

int main ()
{
    printf ("hello make");
    return 1;
}
```

```makefile
# Makefile
main.exe : main.c
    @echo "compile..."
    gcc -o main.exe main.c
```

```bash
linux:~/proj # sed -i 's/    /\t/g' Makefile

# with command
linux:~/proj # gcc -o main.exe main.c
linux:~/proj # ./main.exe

# with make
linux:~/proj # make
linux:~/proj # ./main.exe
```

---

## macro

```c
// main.c
#include <stdio.h>

int main()
{

#ifdef x86_64
  char Arch[]="x86_64";
#elif ia32
  char Arch[]="ia32";
#else
  char Arch[]="Unknown";
#endif

  printf("architecture: %s\n", Arch);
  return 1;
}
```

```makefile
# Makefile.inc
ARCH=x86_64
```

```makefile
# Makefile
include Makefile.inc

main.exe : main.c
    @echo "compile..."
    gcc -E -D${ARCH} main.c > _main.c
    gcc -o main.exe _main.c

.PHONY: clean
clean:
    @echo "clean..."
    -rm main.exe
```

```bash
linux:~/proj # ARCH=ia32 make
linux:~/proj # ./main.exe

linux:~/proj # make clean

linux:~/proj # ARCH=x86_64 make
linux:~/proj # ./main.exe
```

---

## depend

```c
// main.c
#include "hi.h"

int main ()
{
    hi () ;
    return 1 ;
}
```

```c
// hi.h
#include "hi.c"

void hi () ;
```

```c
// hi.c
#include <stdio.h>

void hi () ;
{
    printf ("include method") ;
}
```

```makefile
# Makefile.exp
CC=gcc

.PHONY: all
all : main.o
    ${CC} -o main.exe main.o

# explicit
main.o : main.c
    $(CC) -o main.o -c main.c

.PHONY: clean
clean :
    -rm *.o *.exe
```

```makefile
# Makefile.imp
CC=gcc

.PHONY: all
all : main.o
    ${CC} -o main.exe main.o

# implicit
main.o : main.c

.PHONY: clean
clean :
    -rm *.o *.exe
```

### variable

```makefile
# Makefile
CC =/usr/bin/gcc

.SUFFIX : .c .o

.PHONY: all
all : main.o hi.o
    ${CC} -o main.exe $?
# $? all dependency file

.c.o :
    ${CC} -c $<
# $< first dependency file

.PHONY: clean
clean:
    -rm *.o *.exe
```

```makefile
# =
X = foo
Y = $(X) bar
X = xyz
# y = xyz bar

# :=
X := foo
Y := $(X) bar
X := xyz
# y = foo bar

# ?=
FOO ?= bar

# +=
CFLAGS = -Wall -g
CFLAGS += -O2
```

### wild card

```makefile
# Makefile
CC=/usr/bin/gcc

.SUFFIX : .c .o

.PHONY: all
all : main.o hi.o
    ${CC} -o main.exe $?

%.o : %.c
    ${CC} -c $<

.PHONY: clean
clean:
    -rm *.o *.exe
```

---

## libaray

```c
// main.c
int main ()
{
    hi () ;
    return 1 ;
}
```

```c
// hi.c
#include <stdio.h>

void hi ()
{
    printf ("library") ;
}
```

```makefile
# Makefile.static
CC=/usr/bin/gcc

.SUFFIX: .c .o

.PHONY: all
all: main.o libhi.a
    ${CC} -o main.exe main.o  -L. -lhi

.c.o:
    ${CC} -c $<

# make static library
libhi.a: hi.o
    ar rcv $@ $?
    ranlib $@

.PHONY: clean
clean:
    -rm *.o *.a *.exe
```

```makefile
# Makefile.symbolic
CC=/usr/bin/gcc

.SUFFIX: .c .o

.PHONY: all
all: main.o libhi.so
    ${CC} -o main.exe $?

.c .o:
    ${CC} -c $<

hi.o: hi.c
    ${CC} -fPIC -c $?

# make share library
libhi.so : hi.o
    ${CC} -shared -o $@ $?

.PHONY: clean
clean:
    -rm *.o *.so *.exe
```

```bash
# static link
linux:~ # make -f Makefile.static

# shared link
linux:~ # make -f Makefile.symbolic
linux:~ # echo $LD_LIBRARY_PATH
linux:~ # ldconfig -v
linux:~ # cat /etc/ld.so.conf
linux:~ # ldconfig
```

---

## work directory

```makefile
# Makefile
include Makefile.inc

try:
	@echo "change directory"; cd src; pwd
	@echo "current directory"; pwd

# make by change directory
all:
    cd src; make

# make by -C
hi:
    make -C src hi
```

```makefile
# Makefile.inc
export ARCH=x86_64
NAME=linux
```

```makefile
# src/Makefile
main.exe : main.c
    @echo "compile..."
    gcc -E -D${ARCH} main.c > _main.c
    gcc -o main.exe _main.c

hi:
    echo "hi $(ARCH)"
    echo "hi $(NAME)"
```

```c
// main.c
#include <stdio.h>

int main()
{

#ifdef x86_64
  char Arch[]="x86_64";
#elif ia32
  char Arch[]="ia32";
#else
  char Arch[]="Unknown";
#endif

  printf("architecture: %s\n", Arch);
  return 1;
}
```

```bash
linux:~/pro $ make try
linux:~/pro $ make all
linux:~/pro $ make hi
```

---

## ref

[Makefile 語法簡介](https://sites.google.com/site/mymakefile/makefile-yu-fa-jian-jie)
[跟我一起写 Makefile](https://seisman.github.io/how-to-write-makefile/overview.html)
[Makefile](http://tw.gitbook.net/makefile/index.html)
[Learn Makefiles With the tastiest examples](https://makefiletutorial.com/)
[GNU make](https://www.gnu.org/software/make/manual/make.html)
[Unix Makefile Tutorial](https://www.tutorialspoint.com/makefile/index.htm)
