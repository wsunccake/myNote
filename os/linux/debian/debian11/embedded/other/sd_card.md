# sd card

## image / virtual

```bash
# package
debian:~ # apt install kpartx

debian:~ # SD_IMG=sd.img
debian:~ # LOOP=loop0
debian:~ # SD1=sd1
debian:~ # SD2=sd2
debian:~ # PAT_SIZE=81

# create virtual sd card
debian:~ # dd if=/dev/zero of=$SD_IMG bs=1G count=1
debian:~ # file $SD_IMG
debian:~ # hexdump $SD_IMG

# partition device
debian:~ # parted -s $SD_IMG mklabel msdos
debian:~ # parted -s $SD_IMG mkpart primary fat32 1MiB ${PAT_SIZE}MiB
debian:~ # parted -s $SD_IMG set 1 lba off
debian:~ # parted -s $SD_IMG mkpart primary ext4 ${PAT_SIZE}MiB 100%
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

```bash
#!/bin/bash

###
### var
###

SD_IMG=sd.img
LOOP=loop0
PAT_SIZE=81
SD1=sd1
SD2=sd2


###
### func
###

create_sd() {
  dd if=/dev/zero of=$SD_IMG bs=1G count=1
  file $SD_IMG
  hexdump $SD_IMG
}

partition_sd() {
  parted -s $SD_IMG mklabel msdos
  parted -s $SD_IMG mkpart primary fat32 1MiB ${PAT_SIZE}MiB
  parted -s $SD_IMG set 1 lba off
  parted -s $SD_IMG mkpart primary ext4 ${PAT_SIZE}MiB 100%
  parted -s $SD_IMG print
  fdisk -l $SD_IMG
}

attach_sd() {
  losetup /dev/$LOOP $SD_IMG
  losetup
  kpartx -av /dev/$LOOP
  kpartx -lv /dev/$LOOP
}

format_sd() {
  mkfs -t msdos /dev/mapper/${LOOP}p1
  mkfs -t ext4 -F /dev/mapper/${LOOP}p2
}

mount_sd() {
  mkdir -p $SD1
  mkdir -p $SD2
  mount /dev/mapper/${LOOP}p1 $SD1
  mount /dev/mapper/${LOOP}p2 $SD2
  lsblk
}

umount_sd() {
  umount $SD1
  umount $SD2
  lsblk
}

detach_sd() {
  kpartx -dv /dev/$LOOP
  kpartx -lv /dev/$LOOP
  losetup -d /dev/$LOOP
  losetup
}


###
### main
###

$1
```
