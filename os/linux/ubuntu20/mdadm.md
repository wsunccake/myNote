# mdadm

## install

```bash
[ubuntu:~ ] # apt install mdadm
[ubuntu:~ ] # apt list mdadm
```

---

## raid

```bash
# list / show
[ubuntu:~ ] # mdadm -D /dev/md0
[ubuntu:~ ] # mdadm -Db /dev/md0
[ubuntu:~ ] # mdadm -Q /dev/md0
[ubuntu:~ ] # mdadm -E /dev/md0
[ubuntu:~ ] # mdadm -Dsv
# -D, --detail
# -Q, --query
# -E, --examine
# -s, --scan
# -v, --verbose

# create
[ubuntu:~ ] # mdadm -Cv /dev/md0 --level=0 --raid-devices=2 /dev/vd[b-c]                # raid 0
[ubuntu:~ ] # mdadm -Cv /dev/md0 --level=1 --raid-devices=2 --spare=0 /dev/vd[b-c]      # raid 1
[ubuntu:~ ] # mdadm -Cv /dev/md0 --level=5 --raid-devices=3 /dev/vd[b-d]                # raid 5
[ubuntu:~ ] # mdadm -Cv /dev/md0 --level=6 --raid-devices=4 /dev/vd[b-e]                # raid 6
[ubuntu:~ ] # mdadm -Cv /dev/md0 --level=10 --raid-devices=4 /dev/vd[b-e]               # raid 10
# -C, --create

# config
[ubuntu:~ ] # cat /dev/mdstat
[ubuntu:~ ] # mdadm -Ds [/dev/md0] >> /etc/mdadm/mdadm.conf
[ubuntu:~ ] # update-initramfs -u

# fomat and mount
[ubuntu:~ ] # fdisk /dev/md0
[ubuntu:~ ] # mkfs.xfs /dev/md0
[ubuntu:~ ] # mount /dev/md0p1 /data
[ubuntu:~ ] # vi /etc/fstab
/dev/md0p1 /data xfs defaults 0 0

# stop
[ubuntu:~ ] # mdadm -S /dev/md0
# -S, --stop
[ubuntu:~ ] # mdadm --zero-superblock /dev/vdb

# change disk
[ubuntu:~ ] # mdadm --manage /dev/md0 --fail /dev/vdb
[ubuntu:~ ] # mdadm --manage /dev/md0 --remove /dev/vdb
[ubuntu:~ ] # mdadm --manage /dev/md0 --add /dev/vdd
```

---

## format disk to softraid

```bash
[ubuntu:~ ] # lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda                  252:0    0  100G  0 disk
├─vda1               252:1    0    1M  0 part
├─vda2               252:2    0    1G  0 part /boot
└─vda3               252:3    0   99G  0 part
  └─ubuntu--vg-lv--0 253:0    0   99G  0 lvm  /
vdb                  252:16   0  100G  0 disk
vdc                  252:32   0  100G  0 disk
vdd                  252:16   0  100G  0 disk
vde                  252:32   0  100G  0 disk

[ubuntu:~ ] # parted /dev/vdb
(parted) mklabel gpt
(parted) mkpart primary 0% 100%
(parted) set 1 raid on
(parted) align-check
alignment type(min/opt)  [optimal]/minimal? optimal
Partition number? 1
1 aligned
(parted) print
Model: Virtio Block Device (virtblk)
Disk /dev/vdb: 107GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End    Size   File system  Name     Flags
 1      1049kB  107GB  107GB               primary  raid

(parted) quit
[ubuntu:~ ] # fdisk -l /dev/vdb
Disk /dev/vdb: 100 GiB, 107374182400 bytes, 209715200 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 58767C03-41DC-49A3-99D1-43F8B7406D44

Device     Start       End   Sectors  Size Type
/dev/vdb1   2048 209713151 209711104  100G Linux RAID

[ubuntu:~ ] # parted -s /dev/vdc mklabel gpt
[ubuntu:~ ] # parted -s /dev/vdc mkpart primary 0% 100%
[ubuntu:~ ] # parted -s /dev/vdc set 1 raid on
[ubuntu:~ ] # parted -s /dev/vdc align-check optimal 1
[ubuntu:~ ] # parted -s /dev/vdc print
```
