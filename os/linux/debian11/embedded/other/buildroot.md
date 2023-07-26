# buildroot

## package

```bash
debian:~ # apt install rsync

debian:~ $ tar zxf buildroot-2023.02.tar.gz
debian:~ $ cd buildroot-2023.02
debian:~/buildroot-2023.02 $ ls configs/qemu_*
```

---

## qemu

```bash
# arch
debian:~/buildroot-2023.02 $ make qemu_arm_vexpress_defconfig		# for arm
debian:~/buildroot-2023.02 $ make qemu_aarch64_virt_defconfig		# for arm64
debian:~/buildroot-2023.02 $ make qemu_x86_64_defconfig				# for x86_64

# package config
debian:~/buildroot-2023.02 $ make menuconfig

# kernel config
debian:~/buildroot-2023.02 $ make linux-menuconfig
Kernel hacking  --->
  Compile-time checks and compiler options  --->
    [*] Compile the kernel with debug info

# enable kernel debug
debian:~/buildroot-2023.02 $ grep CONFIG_DEBUG_KERNEL=y output/build/linux-5.15.18/.config
debian:~/buildroot-2023.02 $ grep CONFIG_DEBUG_INFO=y output/build/linux-5.15.18/.config

# build
debian:~/buildroot-2023.02 $ make [-j <cpu number>]

# exec
debian:~/buildroot-2023.02 $ ./output/images/start-qemu.sh
```

---

## custome package

```c
// hello/hello.c
#include <stdio.h>

int main()
{
  printf("hello world!\n");
  return 0;
}
```

```makefile
# hello/Makefile
# CFLAGS_EXTRA = \$(shell \$(PKG_CONFIG) --cflags libdrm)
# LIBS = \$(shell \$(PKG_CONFIG) --libs libdrm)

.PHONY: clean

hello: hello.c
	\$(CC) \$(CFLAGS) \$(CFLAGS_EXTRA) -o '\$@' '\$<' \$(LIBS)

clean:
	rm hello
```

```conf
# hello/Config.in
config BR2_PACKAGE_HELLO
	bool "hello"
#	depends on BR2_PACKAGE_LIBDRM
	help
	  Hello world package.

	  http://example.com
```

```makefile
# hello/hello.mk
################################################################################
#
# hello
#
################################################################################

HELLO_VERSION = 1.0
HELLO_SITE = ./package/hello
HELLO_SITE_METHOD = local
# HELLO_DEPENDENCIES += libdrm

define HELLO_BUILD_CMDS
    \$(MAKE) -C \$(@D) \$(TARGET_CONFIGURE_OPTS)
endef

define HELLO_INSTALL_TARGET_CMDS
	\$(INSTALL) -D -m 0755 \$(@D)/hello \$(TARGET_DIR)/usr/bin
endef

\$(eval \$(generic-package))
```

```bash
debian:~ $ tree hello
hello
├── Config.in
├── hello.mk
├── main.c
└── Makefile

0 directories, 4 files

debian:~ $ make -C hello
debian:~ $ make -C hello clean
```

```bash
debian:~/buildroot-2023.02 $ cp -r ~/hello package/.

debian:~/buildroot-2023.02 $ vi package/Config.in
...
menu "Text editors and viewers"
	source "package/bat/Config.in"
	source "package/ed/Config.in"
	source "package/joe/Config.in"
	source "package/less/Config.in"
	source "package/mc/Config.in"
	source "package/mg/Config.in"
	source "package/most/Config.in"
	source "package/nano/Config.in"
	source "package/uemacs/Config.in"
	source "package/vim/Config.in"
endmenu

### begin
menu "User provided"
	source "package/hello/Config.in"
endmenu
### end

endmenu
```
