# user-mode linux

---

## content

- [environment](#environment)
- [build rootfs from debootstrap](#build-rootfs-from-debootstrap)
  - [manual run](#manual-run)
  - [setup network](#setup-network)
  - [boot script](#boot-script)
- [build user-mode linux from kernel](#build-user-mode-linux-from-kernel)
- [startup user-mode linux](#startup-user-mode-linux)
- [develop kernel module](#develop-kernel-module)
  - [hello](#hello)
- [debug / trace module](#debug--trace-module)

---

## environment

```text
Host:
  OS: Ubuntu 22.04.2 LTS

Target:
  User-Mode Linux: Ubuntu 22
```

---

## build rootfs from debootstrap

```bash
host:~ # ROOTFS=/root/amd64-jammy

host:~ # debootstrap \
  --arch amd64 \
  jammy \
  $ROOTFS \
  https://ftp.ubuntu-tw.org/mirror/ubuntu/
```

---

## startup user-mode linux

### manual run

```bash
host:~ # ./linux/linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=$ROOTFS \
  rw mem=64M init=/bin/sh ubd0=/dev/null hostname=uml \
  quiet

target:~ # stty sane
target:~ # mount -t proc none /proc
target:~ # cat /proc/cpuinfo
```

### setup network

```bash
# setup tap
host:~ # TAP=tap0
host:~ # IP=192.168.100.100
host:~ # ip tuntap add $TAP mode tap
host:~ # ip link set $TAP up
host:~ # ip address add $IP/24 dev $TAP

# setup nat
host:~ # echo 1 > /proc/sys/net/ipv4/ip_forward
host:~ # iptables -t nat -A POSTROUTING -j MASQUERADE
host:~ # iptables -t nat -L -nv

host:~/linux # ./linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=$ROOTFS \
  rw mem=64M init=/bin/sh quiet ubd0=/dev/null hostname=uml \
  eth0=tuntap,tap0

target:~ # IP=192.168.100.101
target:~ # ip link set eth0 up
target:~ # ip address add $IP/24 dev eth0
target:~ # ip route add default via $IP dev eth0
target:~ # ping -c 3 $IP
```

### boot script

```bash
# user-mode linux init script
host:~ # cat << EOF > $ROOTFS/init.sh
#!/bin/sh

mount -t proc proc /proc
mount -t sysfs sys /sys

IP=192.168.100.101
ip link set eth0 up
ip address add $IP/24 dev eth0

/bin/bash
EOF
host:~ # chmod +x $ROOTFS/init.sh

# user-mode linux startip script
host:~ # cat << EOF > run_uml.sh
ROOTFS=/root/amd64-jammy

/root/linux/linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=$ROOTFS \
  rw mem=64M init=/bin/sh quiet ubd0=/dev/null hostname=uml \
  eth0=tuntap,tap0
EOF
host:~ # chmod +x run_uml.sh
```

---

## build user-mode linux from kernel

```bash
# package
host:~ # apt install build-essential flex bison bc dwarves
host:~ # apt install libncurses-dev libssl-dev ca-certificates
host:~ # apt install xz-utils wget curl fakeroot

# download kernel
host:~ # KERNEL_URL=https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.42.tar.xz
host:~ # KERNEL_XZ=${KERNEL_URL##*/}
host:~ # KERNEL_DIR=${KERNEL_XZ%.tar.xz}

# un-compress tarball
host:~ # uname -a
host:~ # wget $KERNEL_URL
host:~ # tar Jxf $KERNEL_XZ
host:~ # cd $KERNEL_DIR
host:~ # ln -s $KERNEL_DIR linux

# compile user-mode linux
host:~ # cd linux
host:~/linux # make mrproper
host:~/linux # make defconfig ARCH=um SUBARCH=x86_64
host:~/linux # make menuconfig ARCH=um SUBARCH=x86_64

# build user-mode linux
host:~/linux # make linux ARCH=um SUBARCH=x86_64 -j `nproc`
host:~/linux # file linux
host:~/linux # ./linux --help

# build module
host:~/linux # make ARCH=um SUBARCH=x86_64 modules -j `nproc`
host:~/linux # make ARCH=um MODLIB=$ROOTFS/lib/modules/VER modules_install

# user-mode linux
host:~ # ./run_uml.sh
target:~ # mv /lib/modules/VER /lib/modules/`uname -r`
target:~ # depmod -ae `uname -r`

# test kernel module
target:~ # modprobe isofs
target:~ # lsmod
```

---

## develop kernel module

### hello

```c
// tests/hello.c
#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("GPL");

static int hello_init(void)
{
    printk(KERN_ALERT "Hello World! - init\n");
    return 0;
}

static void hello_exit(void)
{
    printk(KERN_ALERT "Hello World! - exit\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

```makefile
# tests/Makefile
obj-m += hello.o

PWD := $(shell pwd)
KDIR := $(PWD)/..

default:
    $(MAKE) -C $(KDIR) M=$(PWD) modules ARCH=um

clean:
    $(MAKE) -C $(KDIR) M=$(PWD) clean ARCH=um
```

```bash
host:~ # mkdir -p linux/tests
host:~ # cat linux/tests/hello.c
host:~ # cat linux/tests/Makefile

host:~ # make -C linux/test
host:~ # find linux/tests -name "*.ko"
host:~ # cp linux/tests/hello.ko $ROOTFS/.

host:~ # ./run_uml.sh

target # insmod hello.ko
target # lsmod
```

---

## debug / trace module
