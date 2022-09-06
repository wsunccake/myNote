# make

## install

```bash
centos:~ # dnf install make

ubuntu:~ # apt install make
```


---

## hello

```bash
linux:~/proj # cat << EOF > main.c
#include <stdio.h>

int main ()
{
    printf ("hello make");
    return 1;
}
EOF

linux:~/proj # cat << EOF > makefile
main.exe : main.c
    @echo "compile..."
    gcc -o main.exe main.c
EOF
linux:~/proj # sed -i 's/    /\t/g' makefile
```


### with command

```bash
linux:~/proj # gcc -o main.exe main.c
linux:~/proj # ./main.exe
```


### with make

```bash
linux:~/proj # make
linux:~/proj # ./main.exe
```


---

## macro

```bash
linux:~/proj # cat << EOF > main.c
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
EOF

linux:~/proj # cat << EOF > makefile
ARCH=x86_64

main.exe : main.c
    @echo "compile..."
    gcc -E -D${ARCH} main.c > _main.c
    gcc -o main.exe _main.c

.PHONY: clean
clean:
    @echo "clean..."
    -rm main.exe
EOF
linux:~/proj # sed -i 's/    /\t/g' makefile

linux:~/proj # make -DARCH=ia32
linux:~/proj # ./main.exe

linux:~/proj # make clean

linux:~/proj # make -DARCH=x86_64
linux:~/proj # ./main.exe
```


---

## include

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


### explicit

```makefile
# makefile
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


### implicit

```makefile
# makefile
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
# makefile
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
# makefile
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


### static link

```makefile
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


### shared link

```makefile
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
linux:~ # echo $LD_LIBRARY_PATH
linux:~ # ldconfig -v
linux:~ # cat /etc/ld.so.conf
linux:~ # ldconfig
```


---

[Makefile 語法簡介](https://sites.google.com/site/mymakefile/makefile-yu-fa-jian-jie)

[Learn Makefiles With the tastiest examples](https://makefiletutorial.com/)

[GNU make](https://www.gnu.org/software/make/manual/make.html)

