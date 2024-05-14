# kernel 5.x

```bash
# for debian / ubuntu
linux:~ # apt install build-essential
linux:~ # apt install kmod
linux:~ # apt install linux-headers-`uname -r`

# for rhel / fedora
linux:~ # yum groupinstall 'Development Tools'
linux:~ # yum install kmod
linux:~ # yum install kernel-devel-`uname -r`

linux:~ # lsmod
linux:~ # cat /proc/modules

# kernel source
linux:~ # ls /lib/modules/`uname -r`/source/include/linux           # debian
linux:~ # ls /lib/modules/`uname -r`/build/include/linux            # ubuntu
```

---

## hello

### example 1

```c
// hello-1.c - simple kernel module
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

int init_module(void)
{
    pr_info("Hello world 1.\n"); // kernel module "start" (initialization) function
    return 0;
}

void cleanup_module(void)
{
    pr_info("Goodbye world 1.\n"); // kernel module "end" (cleanup) function
}

MODULE_LICENSE("GPL");
```

### example 2

```c
// hello-2.c - demonstrating the module_init() and module_exit() macro
#include <linux/init.h>   /* Needed for the macros */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

static int __init hello_2_init(void)
{
    pr_info("Hello, world 2\n");
    return 0;
}

static void __exit hello_2_exit(void)
{
    pr_info("Goodbye, world 2\n");
}

module_init(hello_2_init); // kernel module "start" (initialization) function
module_exit(hello_2_exit); // kernel module "end" (cleanup) function

MODULE_LICENSE("GPL");
```

### example 3

```c
// hello-3.c - illustrating the __init, __initdata and __exit macro
#include <linux/init.h> /* Needed for the macros */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

static int hello3_data __initdata = 3;

static int __init hello_3_init(void)
{
    pr_info("Hello, world %d\n", hello3_data);
    return 0;
}

static void __exit hello_3_exit(void)
{
    pr_info("Goodbye, world 3\n");
}

module_init(hello_3_init);
module_exit(hello_3_exit);

MODULE_LICENSE("GPL");
```

### example 4

```c
// hello-4.c - demonstrates module documentation
#include <linux/init.h>   /* Needed for the macros */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h> /* Needed for pr_info() */

MODULE_LICENSE("GPL");
MODULE_AUTHOR("LKMPG");
MODULE_DESCRIPTION("A sample driver");

static int __init init_hello_4(void)
{
    pr_info("Hello, world 4\n");
    return 0;
}

static void __exit cleanup_hello_4(void)
{
    pr_info("Goodbye, world 4\n");
}

module_init(init_hello_4);
module_exit(cleanup_hello_4);
```

### example 5

```c
// hello-5.c - demonstrates command line argument passing to a module
#include <linux/init.h>
#include <linux/kernel.h> /* for ARRAY_SIZE() */
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/printk.h>
#include <linux/stat.h>

MODULE_LICENSE("GPL");

static short int myshort = 1;
static int myint = 420;
static long int mylong = 9999;
static char *mystring = "blah";
static int myintarray[2] = {420, 420};
static int arr_argc = 0;

module_param(myshort, short, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
MODULE_PARM_DESC(myshort, "A short integer");

module_param(myint, int, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
MODULE_PARM_DESC(myint, "An integer");

module_param(mylong, long, S_IRUSR);
MODULE_PARM_DESC(mylong, "A long integer");

module_param(mystring, charp, 0000);
MODULE_PARM_DESC(mystring, "A character string");

module_param_array(myintarray, int, &arr_argc, 0000);
MODULE_PARM_DESC(myintarray, "An array of integers");

static int __init hello_5_init(void)
{
    int i;

    pr_info("Hello, world 5\n=============\n");
    pr_info("myshort is a short integer: %hd\n", myshort);
    pr_info("myint is an integer: %d\n", myint);
    pr_info("mylong is a long integer: %ld\n", mylong);
    pr_info("mystring is a string: %s\n", mystring);

    for (i = 0; i < ARRAY_SIZE(myintarray); i++)
        pr_info("myintarray[%d] = %d\n", i, myintarray[i]);

    pr_info("got %d arguments for myintarray.\n", arr_argc);
    return 0;
}

static void __exit hello_5_exit(void)
{
    pr_info("Goodbye, world 5\n");
}

module_init(hello_5_init);
module_exit(hello_5_exit);
```

### example startstop

```c
// start.c - illustration of multi filed module
#include <linux/kernel.h>
#include <linux/module.h>

int init_module(void)
{
    pr_info("Hello, world - this is the kernel speaking\n");
    return 0;
}

MODULE_LICENSE("GPL");
```

```c
// stop.c - illustration of multi filed module
#include <linux/kernel.h> /* We are doing kernel work */
#include <linux/module.h> /* Specifically, a module  */

void cleanup_module(void)
{
    pr_info("Short is the life of a kernel module\n");
}

MODULE_LICENSE("GPL");
```

### makefile

```makefile
# Makefile
obj-m += hello-1.o
obj-m += hello-2.o
obj-m += hello-3.o
obj-m += hello-4.o
obj-m += hello-5.o
obj-m += startstop.o
startstop-objs := start.o stop.o

PWD := $(CURDIR)
KDIR := /lib/modules/$(shell uname -r)/build

all:
	make -C ${KDIR} M=$(PWD) modules

clean:
	make -C ${KDIR} M=$(PWD) clean
```

### usage

```bash
linux:~/hello $ tree
tree
.
├── hello-1.c
├── hello-2.c
├── hello-3.c
├── hello-4.c
├── hello-5.c
├── start.c
├── stop.c
└── Makefile

0 directories, 8 files

linux:~/hello $ make

# insert module
linux:~/hello # modinfo <module>.ko
linux:~/hello # insmod <module>.ko

# remove module
linux:~/hello # rmmod <module>

# list module
linux:~/hello # lsmod | grep <module>

# update module dependcy
linux:~/hello # ln -s `readfile -f <module>.ko` /lib/modules/`uname -r`/misc
linux:~/hello # depmod
linux:~/hello # cat /lib/modules/`uname -r`/modules.dep

# add / remove module
linux:~ # modprobe <moudle>
linux:~ # modprobe -r <moudle>

# log / message
linux:~/hello # dmesg
linux:~/hello # journalctl --since "1 hour ago" | grep kernel
```

---

User Space
Kernel Space
Name Space
/proc/kallsyms
Code space
Device Drivers
/dev

---

## character device driver

```c
// chardev.c : creates a read - only char device that says how many times
#include <linux/atomic.h>
#include <linux/cdev.h>
#include <linux/delay.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h> /* for sprintf() */
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/types.h>
#include <linux/uaccess.h> /* for get_user and put_user */

#include <asm/errno.h>

/*  Prototypes - this would normally go in a .h file */
static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char __user *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char __user *, size_t, loff_t *);

#define SUCCESS 0
#define DEVICE_NAME "chardev" // dev name appear /proc/devices
#define BUF_LEN 80            // max length of the message

static int major; // device driver major number
enum
{
    CDEV_NOT_USED = 0,
    CDEV_EXCLUSIVE_OPEN = 1,
};

// prevent multiple access to device
static atomic_t already_open = ATOMIC_INIT(CDEV_NOT_USED);
static char msg[BUF_LEN + 1];
static struct class *cls;
static struct file_operations chardev_fops = {
    .read = device_read,
    .write = device_write,
    .open = device_open,
    .release = device_release,
};

static int __init chardev_init(void)
{
    // register device
    major = register_chrdev(0, DEVICE_NAME, &chardev_fops);

    if (major < 0)
    {
        pr_alert("Registering char device failed with %d\n", major);
        return major;
    }
    pr_info("I was assigned major number %d.\n", major);

    cls = class_create(THIS_MODULE, DEVICE_NAME);
    device_create(cls, NULL, MKDEV(major, 0), NULL, DEVICE_NAME);
    // int register_chrdev_region(dev_t from, unsigned count, const char *name);
    // int alloc_chrdev_region(dev_t *dev, unsigned baseminor, unsigned count, const char *name);
    pr_info("Device created on /dev/%s\n", DEVICE_NAME);

    return SUCCESS;
}

static void __exit chardev_exit(void)
{
    device_destroy(cls, MKDEV(major, 0));
    class_destroy(cls);

    // unregister device
    unregister_chrdev(major, DEVICE_NAME);
}

/* method */
// cat /dev/chardev
static int device_open(struct inode *inode, struct file *file)
{
    static int counter = 0;

    if (atomic_cmpxchg(&already_open, CDEV_NOT_USED, CDEV_EXCLUSIVE_OPEN))
        return -EBUSY;

    sprintf(msg, "I already told you %d times Hello world!\n", counter++);
    try_module_get(THIS_MODULE);

    return SUCCESS;
}

static int device_release(struct inode *inode, struct file *file)
{
    atomic_set(&already_open, CDEV_NOT_USED);
    module_put(THIS_MODULE);

    return SUCCESS;
}

static ssize_t device_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset)
{
    int bytes_read = 0;
    const char *msg_ptr = msg;

    if (!*(msg_ptr + *offset))
    {
        *offset = 0; // reset the offset at the end of message
        return 0;
    }

    msg_ptr += *offset;
    while (length && *msg_ptr)
    {
        put_user(*(msg_ptr++), buffer++);
        length--;
        bytes_read++;
    }
    *offset += bytes_read;

    return bytes_read;
}

// echo "hi" > /dev/hello
static ssize_t device_write(struct file *filp, const char __user *buff, size_t len, loff_t *off)
{
    pr_alert("Sorry, this operation is not supported.\n");
    return -EINVAL;
}

module_init(chardev_init);
module_exit(chardev_exit);

MODULE_LICENSE("GPL");
```

```bash
# module
linux:~ # lsmod | grep
linux:~ # cat /proc/modules

# device
linux:~ # grep chardev /proc/devices
linux:~ # cat /dev/chardev
```

---

## ref

[The Linux Kernel Module Programming Guide](https://sysprog21.github.io/lkmpg/)
