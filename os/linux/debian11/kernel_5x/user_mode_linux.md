# user-mode linux

## build user-mode linux

```bash
debian:~ # apt install build-essential libncurses-dev flex bison
debian:~ # apt install xz-utils wget curl ca-certificates bc
debian:~ # apt install fakeroot

debian:~ # KERNEL_URL=https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.107.tar.xz
debian:~ # KERNEL_XZ=${KERNEL_URL##*/}
debian:~ # KERNEL_DIR=${KERNEL_XZ%.tar.xz}
# download kernel
debian:~ # uname -a
debian:~ # wget $KERNEL_URL
debian:~ # tar Jxf $KERNEL_XZ
debian:~ # cd $KERNEL_DIR
debian:~ # ln -s $KERNEL_DIR linux

# compile user-mode linux
debian:~/linux # vi .config
debian:~/linux # make mrproper
debian:~/linux # make defconfig ARCH=um SUBARCH=x86_64
debian:~/linux # make menuconfig ARCH=um SUBARCH=x86_64
debian:~/linux # make linux ARCH=um SUBARCH=x86_64 -j `nproc`
debian:~/linux # file linux
debian:~/linux # ./linux --help
```

---

## setup alpine rootfs

```bash
# build alpine rootfs
debian:~/linux # REPO=http://dl-cdn.alpinelinux.org/alpine/v3.17/main
debian:~/linux # mkdir -p rootfs
debian:~/linux # curl $REPO/x86_64/APKINDEX.tar.gz | tar -xz -C /tmp/
debian:~/linux # APK_TOOL=`grep -A1 apk-tools-static /tmp/APKINDEX | cut -c3- | xargs printf "%s-%s.apk"`
debian:~/linux # curl $REPO/x86_64/$APK_TOOL | fakeroot tar -xz -C rootfs
debian:~/linux # fakeroot rootfs/sbin/apk.static \
  --repository $REPO --update-cache \
  --allow-untrusted \
  --root $PWD/rootfs --initdb add alpine-base
debian:~/linux # echo $REPO > rootfs/etc/apk/repositories
debian:~/linux # echo "LABEL=ALPINE_ROOT / auto defaults 1 1" >> rootfs/etc/fstab
```

```bash
# run user-mode linux
debian:~/linux # ./linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=./rootfs \
  rw mem=64M init=/bin/sh ubd0=/dev/null quiet

uml # stty sane
uml # /bin/busybox --install
uml # mount -t proc none /proc
uml # cat /proc/cpuinfo
```

---

## setup virtual network

```bash
debian:~ # TAP=tap0
debian:~ # IP=192.168.100.100
debian:~ # ip tuntap add $TAP mode tap
debian:~ # ip link set $TAP up
debian:~ # ip address add $IP/24 dev $TAP

debian:~/linux # ./linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=./rootfs \
  rw mem=64M init=/bin/sh quiet ubd0=/dev/null hostname=uml eth0=tuntap,tap0

uml # IP=192.168.100.101
uml # ip link set eth0 up
uml # ip address add $IP/24 dev eth0
uml # ping -c 3 192.168.100.100
```

---

## startup uml by script

```bash
#!/bin/bash
./linux umid=uml0 \
  root=/dev/root rootfstype=hostfs hostfs=./rootfs \
  rw mem=64M mem=64M init=/init.sh \
  ubd0=/dev/null hostname=uml eth0=tuntap,tap0 \
  quiet

stty sane; echo
```

```bash
debian:~/linux # chmod +x run_uml.sh

# startup uml
debian:~/linux # ./run_uml.sh
```

---

## customized environment

```bash
debian:~/linux # wget -O rootfs/sbin/tini https://github.com/krallin/tini/releases/download/v0.19.0/tini-static
debian:~/linux # chmod +x rootfs/sbin/tini

debian:~/linux # cat << EOF > rootfs/init.sh
#!/bin/sh

mount -t proc proc /proc
mount -t sysfs sys /sys

exec /sbin/tini /bin/sh +m
EOF
debian:~/linux # chmod +x rootfs/init.sh

# build module
debian:~/linux # make ARCH=um SUBARCH=x86_64 modules -j `nproc`
debian:~/linux # make ARCH=um MODLIB=../rootfs/lib/modules/VER modules_install

debian:~/linux # ./run_uml.sh

# setup kernel module
uml # mv /lib/modules/VER /lib/modules/`uname -r`
uml # depmod -ae `uname -r`

# test kernel module
uml # modprobe isofs
uml # lsmod

uml # export PS1='\[\033[01;32muml:\w\033[00m \# '
```

---

## hello

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
debian:~/linux # mkdir -p tests
debian:~/linux # cat tests/hello.c
debian:~/linux # cat tests/Makefile

debian:~/linux # make -C test
debian:~/linux # find tests -name "*.ko"
debian:~/linux # cp hello.ko rootfs/.

debian:~/linux # ./run_uml.sh

uml # insmod hello.ko
uml # lsmod
```

---

## ticks

```c
// tests/ticks/ticks.c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/sysfs.h>
#include <linux/kobject.h>
#include <linux/kernel.h>

static ssize_t jiffies_show(struct kobject *kobj, struct kobj_attribute *attr,
                            char *buf) {
        return sprintf(buf, "%lu", jiffies);
}

static ssize_t hz_show(struct kobject *kobj, struct kobj_attribute *attr,
                       char *buf) {
        return sprintf(buf, "%u", HZ);
}

static struct kobj_attribute jiffies_attr =
        __ATTR(jiffies, 0444, jiffies_show, NULL);
static struct kobj_attribute hz_attr = __ATTR(hz, 0444, hz_show, NULL);

static struct attribute *ticks_attrs[] = { &jiffies_attr.attr, &hz_attr.attr,
                                           NULL };

static struct attribute_group ticks_grp = { .attrs = ticks_attrs };

static struct kobject *ticks;

static int __init ticks_init(void) {
        int retval;

        ticks = kobject_create_and_add("ticks", NULL);
        if (!ticks)
                return -EEXIST;

        retval = sysfs_create_group(ticks, &ticks_grp);
        if (retval)
                kobject_put(ticks);

        return retval;
}
module_init(ticks_init);

static void __exit ticks_exit(void) {
        sysfs_remove_group(ticks, &ticks_grp);

        kobject_put(ticks);
}
module_exit(ticks_exit);

MODULE_LICENSE("GPL");
```

```makefile
# tests/ticks/Makefile
obj-m := ticks.o

KDIR= ../../

all:
    $(MAKE) -C $(KDIR) M=$(PWD) modules ARCH=um
clean:
    $(MAKE) -C $(KDIR) M=$(PWD) clean ARCH=um
```

```bash
debian:~/linux # mkdir -p tests/ticks
debian:~/linux # cat tests/ticks/ticks.c
debian:~/linux # cat tests/ticks/Makefile

debian:~/linux/tests/ticks # make
debian:~/linux/tests/ticks # cp ticks.ko ../../rootfs/.

debian:~/linux # ./run_uml.sh

uml # insmod /ticks.ko
uml # lsmod
uml # cat /sys/ticks/jiffies
uml # cat /sys/ticks/hz
```

---

## gdb

```bash
debian:~/linux # gdb -q -ex "python print(sys.version_info.major,sys.version_info.minor)" -ex "quit"
debian:~/linux # echo "CONFIG_GDB_SCRIPTS=y" > .config-fragment
debian:~/linux # ARCH=um scripts/kconfig/merge_config.sh .config .config-fragment
debian:~/linux # make ARCH=um scripts_gdb
debian:~/linux # gdb -ex "add-auto-load-safe-path scripts/gdb/vmlinux-gdb.py" \
  -ex "file vmlinux" \
  -ex "lx-version" -q

(gdb) apropos lx
(gdb) exit

debian:~/linux # cat << EOF >> gdbinit
python gdb.COMPLETE_EXPRESSION = gdb.COMPLETE_SYMBOL
add-auto-load-safe-path scripts/gdb/vmlinux-gdb.py
file vmlinux
lx-version
set args umid=uml0 root=/dev/root rootfstype=hostfs rootflags=$HOME/linux/rootfs rw mem=64M init=/init.sh quiet
handle SIGSEGV nostop noprint
handle SIGUSR1 nopass stop print
EOF

debian:~/linux # gdb -q -x gdbinit
(gdb) run
# startup user-mode linux, other terminal send send SIGUSR1 to debug
(gdb) lx-mounts
(gdb) lx-cmdline
(gdb) lx-dmesg
(gdb) lx-lsmod

(gdb) lx-ps
      TASK          PID    COMM
0x6048cac0   0   swapper
0x60830040   1   tini
0x6083a080   2   kthreadd
0x6083c0c0   3   netns
0x60848100   4   kworker/0:0
0x6084e140   5   kworker/0:0H
0x60850180   6   kworker/u2:0
0x6085c1c0   7   mm_percpu_wq
0x60866200   8   ksoftirqd/0
0x60868240   9   kdevtmpfs
0x60882280  10   inet_frag_wq
0x608a42c0  11   oom_reaper
0x608ac300  12   writeback
0x608ae340  13   kblockd
0x608be380  14   blkcg_punt_bio
0x6091c3c0  15   hwrng
0x6091e400  16   kworker/0:1
0x60938440  17   kswapd0
0x609d4480  18   kworker/u2:1
0x60a5a500  21   sh
(gdb) p $container_of(init_task.tasks.next, "struct task_struct", "tasks")
$1 = (struct task_struct *) 0x60830040
(gdb) p *(struct task_struct *)0x60830040
(gdb) lx-list-check init_task.tasks

(gdb) break do_init_module
(gdb) command 1
> py if str(gdb.parse_and_eval("mod->name")).find("hello") != 1: gdb.execute("continue", False, False)
end
uml # insmod /hello.ko
(gdb) print $lx_module("hello") # must run "insmod /hello.ko" to show it
(gdb) list
```

```bash
# other terminal
debian:~ # pkill -SIGUSR1 -o vmlinux
```
