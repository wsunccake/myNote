# deboostrap to rootfs on arm

## toolchain

```bash
# install
debian:~ # apt install crossbuild-essential-arm64   # for arm64
debian:~ # apt install crossbuild-essential-armel   # for arm32
debian:~ # apt install crossbuild-essential-armhf

debian:~ # arm-linux-gnueabihf-gcc -v

# test
debian:~ # cat << EOF >> hello.c
#include <stdio.h>

int main() {
  printf("hello\n");
}
EOF

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

## sd card

```bash
# package
debian:~ # apt install kpartx

debian:~ # SD_IMG=sd.img
debian:~ # LOOP=loop0
debian:~ # SD1=sd1
debian:~ # SD2=sd2
debian:~ # ZIMG=zImage
debian:~ # DTB=vexpress-v2p-ca9.dtb

# create virtual sd card
debian:~ # dd if=/dev/zero of=$SD_IMG bs=1G count=1
debian:~ # file $SD_IMG
debian:~ # hexdump $SD_IMG

# partition device
debian:~ # parted -s $SD_IMG mklabel msdos
debian:~ # parted -s $SD_IMG mkpart primary fat32 1MiB 81MiB
debian:~ # parted -s $SD_IMG set 1 lba off
debian:~ # parted -s $SD_IMG mkpart primary ext4 81MiB 100%
debian:~ # parted -s $SD_IMG print
debian:~ # fdisk -l $SD_IMG

# attach
debian:~ # losetup /dev/$LOOP $SD_IMG
debian:~ # losetup
debian:~ # kpart -av /dev/$LOOP
debian:~ # kpart -lv /dev/$LOOP

# format
debian:~ # mkfs -t msdos /dev/mapper/${LOOP}p1
debian:~ # mkfs -t ext4 -F /dev/mapper/${LOOP}p2

# mount
debian:~ # mkdir -p $SD1
debian:~ # mkdir -p $SD2
debian:~ # mount /dev/mapper/${LOOP}p1 $SD1
debian:~ # mount /dev/mapper/${LOOP}p2 $SD2
debian:~ # lsblk

# umount
debian:~ # umount $SD1
debian:~ # umount $SD2

# detach
debian:~ # kpart -dv /dev/$LOOP
debian:~ # losetup -d /dev/$LOOP
```

---

## rootfs - debootstrap

```bash
# package
debian:~ # apt install debootstrap

# debootstrap --arch <ARCH> <DISTRO> <DIRECTORY>  <MIRROR>
# debootstrap --second-stage

debian:~ # debootstrap \
  --arch armhf \
  --foreign \
  --keyring=/usr/share/keyrings/debian-archive-keyring.gpg \
  --verbose \
  bullseye \
  $SD2 \
  http://ftp.tw.debian.org/debian

debian:~ # cp /usr/bin/qemu-arm-static $SD2/usr/bin/

# chroot
debian:~ # chroot $SD2 /bin/bash
~ # /debootstrap/debootstrap --second-stage
~ # password


```

```bash
# setup chroot
debian:~ # chroot $SD2 /bin/bash

```

---

## kernel

```bash
debian:~ # apt-get install u-boot-tools

debian:~ # wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.172.tar.xz

debian:~ # tar Jxf linux-5.10.172.tar.xz
debian:~ # cd linux-5.10.172

debian:~/linux-5.10.172 # ls arch/arm/configs/
debian:~/linux-5.10.172 # ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make vexpress_defconfig
debian:~/linux-5.10.172 # ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make menuconfig
System Type  --->
  [ ] Enable the L2x0 outer cache controller

debian:~/linux-5.10.172 # grep CONFIG_MIGHT_HAVE_CACHE_L2X0=n .config
debian:~/linux-5.10.172 # ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make [-j <cpu number>]
debian:~/linux-5.10.172 # ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make [-j <cpu number>] uImage LOADADDR=0x60000000
debian:~/linux-5.10.172 # cp arch/arm/boot/zImage $ZIMG
debian:~/linux-5.10.172 # cp arch/arm/boot/dts/vexpress-v2p-ca9.dtb $DTB

debian:~/linux-5.10.172 # ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make [-j <cpu number>] modules
debian:~/linux-5.10.172 # ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make [-j <cpu number>] modules_install INSTALL_MOD_PATH=../modules/

debian:~/linux-5.10.172 # cd ../modules
debian:~/modules # tar caf ../modules-5.10.172.tar.xz lib

# sd card
debian:~ # cp $ZIMG $SD1
debian:~ # cp $DTB $SD1
```

DTS / Device Tree Source

DTC / Device Tree Compiler

DTB / Device Tree Blob

---

## uboot

```bash
debian:~ # wget https://ftp.denx.de/pub/u-boot/u-boot-2023.01.tar.bz2

debian:~ # tar jxf u-boot-2023.01.tar.bz2
debian:~ # cd u-boot-2023.01

debian:~/u-boot-2023.01 # ls configs/
debian:~/u-boot-2023.01 # CROSS_COMPILE=arm-linux-gnueabihf- make vexpress_ca9x4_defconfig
debian:~/u-boot-2023.01 # CROSS_COMPILE=arm-linux-gnueabihf- make menuconfig
debian:~/u-boot-2023.01 # CROSS_COMPILE=arm-linux-gnueabihf- make [-j <cpu number>]

debian:~/u-boot-2023.01 # cp u-boot $SD1
debian:~/u-boot-2023.01 # cp u-boot.bin $SD1
```

```bash
u-boot ==> help
u-boot ==> version

u-boot ==> bdinfo
u-boot ==> mmcinfo
u-boot ==> printenv

u-boot ==> mmc info
u-boot ==> mmc list
u-boot ==> mmc part

u-boot ==> ls mmc 0:2
u-boot ==> fatls mmc 0:1
u-boot ==> ext4ls mmc 0:2
```

```bash
# u-boot ==> bdinfo
boot_params = 0x60002000
DRAM bank   = 0x00000000
-> start    = 0x60000000  # kernel boot LOADADDR
-> size     = 0x20000000  # (hex) -> 536,870,912 (dec) Byte -> 524,288 KiB -> 512 MiB
DRAM bank   = 0x00000001
-> start    = 0x80000000
-> size     = 0x20000000
flashstart  = 0x40000000
flashsize   = 0x04000000
flashoffset = 0x00000000
baudrate    = 38400 bps
relocaddr   = 0x7ff67000
reloc off   = 0x1f767000
Build       = 32-bit
current eth = ethernet@3,02000000
ethaddr     = 52:54:00:12:34:56
IP addr     = <NULL>
fdt_blob    = 0x60878cd0
new_fdt     = 0x00000000
fdt_size    = 0x00000000
lmb_dump_all:
 memory.cnt  = 0x1
 memory[0]	[0x60000000-0x9fffffff], 0x40000000 bytes flags: 0
 reserved.cnt  = 0x3
 reserved[0]	[0x4c000000-0x4c7fffff], 0x00800000 bytes flags: 4
 reserved[1]	[0x7eb23000-0x9fffffff], 0x214dd000 bytes flags: 0
 reserved[2]	[0x7fb22c68-0x7fffffff], 0x004dd398 bytes flags: 0
devicetree  = embed
arch_number = 0x000008e0
TLB addr    = 0x7fff0000
irq_sp      = 0x7fb26eb0
sp start    = 0x7fb26ea0
Early malloc usage: 370 / 400
```

```bash
# => printenv
arch=arm
baudrate=38400
board=vexpress
board_name=vexpress
boot_a_script=load ${devtype} ${devnum}:${distro_bootpart} ${scriptaddr} ${prefix}${script}; source ${scriptaddr}
boot_efi_binary=load ${devtype} ${devnum}:${distro_bootpart} ${kernel_addr_r} efi/boot/bootarm.efi; if fdt addr -q ${fdt_addr_r}; then bootefi ${kernel_addr_r} ${fdt_addr_r};else bootefi ${kernel_addr_r} ${fdtcontroladdr};fi
boot_efi_bootmgr=if fdt addr -q ${fdt_addr_r}; then bootefi bootmgr ${fdt_addr_r};else bootefi bootmgr;fi
boot_extlinux=sysboot ${devtype} ${devnum}:${distro_bootpart} any ${scriptaddr} ${prefix}${boot_syslinux_conf}
boot_prefixes=/ /boot/
boot_script_dhcp=boot.scr.uimg
boot_scripts=boot.scr.uimg boot.scr  # boot script
boot_syslinux_conf=extlinux/extlinux.conf
boot_targets=mmc1 mmc0 pxe dhcp
bootargs=console=tty0 console=ttyAMA0,38400n8
bootcmd=run distro_bootcmd; run bootflash
bootcmd_dhcp=devtype=dhcp; if dhcp ${scriptaddr} ${boot_script_dhcp}; then source ${scriptaddr}; fi;setenv efi_fdtfile ${fdtfile}; if test -z "${fdtfile}" -a -n "${soc}"; then setenv efi_fdtfile ${soc}-${board}${boardver}.dtb; fi; setenv efi_old_vci ${bootp_vci};setenv efi_old_arch ${bootp_arch};setenv bootp_vci PXEClient:Arch:00010:UNDI:003000;setenv bootp_arch 0xa;if dhcp ${kernel_addr_r}; then tftpboot ${fdt_addr_r} dtb/${efi_fdtfile};if fdt addr -q ${fdt_addr_r}; then bootefi ${kernel_addr_r} ${fdt_addr_r}; else bootefi ${kernel_addr_r} ${fdtcontroladdr};fi;fi;setenv bootp_vci ${efi_old_vci};setenv bootp_arch ${efi_old_arch};setenv efi_fdtfile;setenv efi_old_arch;setenv efi_old_vci;
bootcmd_mmc0=devnum=0; run mmc_boot
bootcmd_mmc1=devnum=1; run mmc_boot
bootcmd_pxe=dhcp; if pxe get; then pxe boot; fi
bootdelay=2
bootflash=run flashargs; cp ${ramdisk_addr} ${ramdisk_addr_r} ${maxramdisk}; bootm ${kernel_addr} ${ramdisk_addr_r}
console=ttyAMA0,38400n8
cpu=armv7
distro_bootcmd=for target in ${boot_targets}; do run bootcmd_${target}; done
dram=1024M
efi_dtb_prefixes=/ /dtb/ /dtb/current/
ethaddr=52:54:00:12:34:56
fdt_addr_r=0x60000000
fdtcontroladdr=60878cd0
fdtfile=vexpress-v2p-ca9.dtb
flashargs=setenv bootargs root=${root} console=${console} mem=${dram} mtdparts=${mtd} mmci.fmax=190000 devtmpfs.mount=0  vmalloc=256M
kernel_addr_r=0x60100000
load_efi_dtb=load ${devtype} ${devnum}:${distro_bootpart} ${fdt_addr_r} ${prefix}${efi_fdtfile}
loadaddr=0x60100000
mmc_boot=if mmc dev ${devnum}; then devtype=mmc; run scan_dev_for_boot_part; fi
mtd=armflash:1M@0x800000(uboot),7M@0x1000000(kernel),24M@0x2000000(initrd)
root=/dev/sda1 rw
scan_dev_for_boot=echo Scanning ${devtype} ${devnum}:${distro_bootpart}...; for prefix in ${boot_prefixes}; do run scan_dev_for_extlinux; run scan_dev_for_scripts; done;run scan_dev_for_efi;
scan_dev_for_boot_part=part list ${devtype} ${devnum} -bootable devplist; env exists devplist || setenv devplist 1; for distro_bootpart in ${devplist}; do if fstype ${devtype} ${devnum}:${distro_bootpart} bootfstype; then run scan_dev_for_boot; fi; done; setenv devplist
scan_dev_for_efi=setenv efi_fdtfile ${fdtfile}; if test -z "${fdtfile}" -a -n "${soc}"; then setenv efi_fdtfile ${soc}-${board}${boardver}.dtb; fi; for prefix in ${efi_dtb_prefixes}; do if test -e ${devtype} ${devnum}:${distro_bootpart} ${prefix}${efi_fdtfile}; then run load_efi_dtb; fi;done;run boot_efi_bootmgr;if test -e ${devtype} ${devnum}:${distro_bootpart} efi/boot/bootarm.efi; then echo Found EFI removable media binary efi/boot/bootarm.efi; run boot_efi_binary; echo EFI LOAD FAILED: continuing...; fi; setenv efi_fdtfile
scan_dev_for_extlinux=if test -e ${devtype} ${devnum}:${distro_bootpart} ${prefix}${boot_syslinux_conf}; then echo Found ${prefix}${boot_syslinux_conf}; run boot_extlinux; echo EXTLINUX FAILED: continuing...; fi
scan_dev_for_scripts=for script in ${boot_scripts}; do if test -e ${devtype} ${devnum}:${distro_bootpart} ${prefix}${script}; then echo Found U-Boot script ${prefix}${script}; run boot_a_script; echo SCRIPT FAILED: continuing...; fi; done
stderr=serial
stdin=serial
stdout=serial
ubifs_boot=if ubi part ${bootubipart} ${bootubioff} && ubifsmount ubi0:${bootubivol}; then devtype=ubi; devnum=ubi0; bootfstype=ubifs; distro_bootpart=${bootubivol}; run scan_dev_for_boot; ubifsumount; fi
vendor=armltd

Environment size: 4229/262140 bytes
```

---

## qemu

```bash
# for kernel
debian:~ # qemu-system-arm \
  -machine vexpress-a9 \
  -smp 1 \
  -m 1024M \
  -dtb $DTB \
  -kernel $ZIMG \
  -append "console=ttyAMA0" \
  -nographic

# for kernel + rootfs / sd card
debian:~ # qemu-system-arm \
  -machine vexpress-a9 \
  -smp 1 \
  -m 1024M \
  -dtb $DTB \
  -kernel $ZIMG \
  -append "root=/dev/mmcblk0p2 rw console=ttyAMA0" \
  -nographic -sd $SD_IMG

# for u-boot
debian:~ # qemu-system-arm \
  -machine vexpress-a9 \
  -smp 1 \
  -m 1024M \
  -kernel u-boot \
  -nographic \

# for u-boot + sd card + kernel
debian:~ # qemu-system-arm \
  -machine vexpress-a9 \
  -smp 1 \
  -m 1024M \
  -kernel u-boot \
  -drive file=$SD_IMG,if=sd,format=raw,index=0 \
  -nographic

u-boot ==> load mmc 0:1 0x60008000 zImage
u-boot ==> load mmc 0:1 0x61000000 vexpress-v2p-ca9.dtb
u-boot ==> setenv bootargs "root=/dev/mmcblk0p2 rw console=ttyAMA0"
u-boot ==> bootz 0x60008000 - 0x61000000

# for u-boot + sd card + kernel + boot script
debian:~ # cat << EOF >> boot.cmd
load mmc 0:1 0x60008000 zImage
load mmc 0:1 0x61000000 vexpress-v2p-ca9.dtb
setenv bootargs "root=/dev/mmcblk0p2 rw console=ttyAMA0"
bootz 0x60008000 - 0x61000000
EOF

debian:~ # mkimage -C none -A arm -T script -d boot.cmd boot.scr
debian:~ # cp boot.scr $SD1
debian:~ # qemu-system-arm \
  -machine vexpress-a9 \
  -smp 1 \
  -m 1024M \
  -kernel u-boot \
  -drive file=$SD_IMG,if=sd,format=raw,index=0 \
  -nographic

u-boot ==> load mmc 0:1 0x62000000 boot.scr
u-boot ==> source 0x62000000
```
