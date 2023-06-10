# toolchain

## concept

```
build   host    target
x       x       x       native
x       x       y       cross
x       y       z       canadian
```

## package

```bash
# test
debian:~ # apt install crossbuild-essential-arm64   # for arm64
debian:~ # apt install crossbuild-essential-armel   # for arm
debian:~ # apt install crossbuild-essential-armhf
```

```c
// hello.c
#include <stdio.h>

int main() {
  printf("hello\n");
  return 0;
}
```

---

## arm

```bash
debian:~ # arm-linux-gnueabihf-gcc -v

debian:~ # arm-linux-gnueabihf-gcc -c hello.c -o hello.armhf
debian:~ # file hello.armhf

# run
debian:~ # dpkg --add-architecture armhf
debian:~ # dpkg --print-foreign-architectures
debian:~ # apt update
debian:~ # apt install qemu-system:armhf qemu-user:armhf qemu-user-static
debian:~ # hello.armhf
```

---

## arm64
