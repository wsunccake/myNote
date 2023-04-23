# kernel

```bash
linux:~ # apt install build-essential kmod
linux:~ # lsmod
linux:~ # cat /proc/modules

linux:~ # apt install linux-headers-`uname -r`
```

---

## hello

```makefile
# Makefile
obj-m += hello.o

PWD := $(CURDIR)

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

```bash
linux:~/hello $ tree
tree
.
├── hello.c
└── Makefile

0 directories, 2 files

linux:~/hello $ make

linux:~/hello # modinfo hello.ko
linux:~/hello # insmod hello.ko
linux:~/hello # lsmode | grep hello
linux:~/hello # rmmod hello
linux:~/hello # journalctl --since "1 hour ago" | grep kernel
```

### example 1

```c
// hello.c
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

// kernel module "start" (initialization) function
int init_module(void)
{
    pr_info("Hello world.\n");

    return 0;
}

// kernel module "end" (cleanup) function
void cleanup_module(void)
{
    pr_info("Goodbye world.\n");
}

MODULE_LICENSE("GPL");
```

### example 2

```c
// hello.c
#include <linux/init.h> /* Needed for the macros */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

static int __init hello_init(void)
{
    pr_info("Hello, world\n");
    return 0;
}

static void __exit hello_exit(void)
{
    pr_info("Goodbye, world\n");
}

module_init(hello_init); // kernel module "start" (initialization) function
module_exit(hello_exit); // kernel module "end" (cleanup) function

MODULE_LICENSE("GPL");
```

### example 3

```c
#include <linux/init.h> /* Needed for the macros */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

static int hello_data __initdata = 3;

static int __init hello_init(void)
{
    pr_info("Hello, world %d\n", hello_data);
    return 0;
}

static void __exit hello_exit(void)
{
    pr_info("Goodbye, world\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
```

### example 4

```c
#include <linux/init.h> /* Needed for the macros */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

MODULE_LICENSE("GPL");
MODULE_AUTHOR("LKMPG");
MODULE_DESCRIPTION("A sample driver");

static int __init init_hello(void)
{
    pr_info("Hello, world\n");
    return 0;
}

static void __exit cleanup_hello(void)
{
    pr_info("Goodbye, world\n");
}

module_init(init_hello);
module_exit(cleanup_hello);
```

### example 5

---

## ref

[The Linux Kernel Module Programming Guide](https://sysprog21.github.io/lkmpg/)
