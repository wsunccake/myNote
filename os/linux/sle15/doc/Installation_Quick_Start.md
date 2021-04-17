# Installation Quick Start


##  Installation on AMD64 and Intel 64

### Copying the Installation Media Image to a Removable Flash Disk

```bash
sle:~ # dd if=<IMAGE> of=<FLASH_DISK> bs=4M && sync

sle:~ # grep -Ff <(hwinfo --disk --short) <(hwinfo --usb --short)
sle:~ # fdisk -l /dev/sdc | grep -e "^/dev"
sle:~ # dd if=SLE-15-SP2-Full-ARCH-GM-media1.iso of=/dev/sdc1 bs=4M && sync
```


### Hardware Requirements

`CPU Requirement`

max: 8192


`Memory Requirement`

min: 1024 MB

when two cpu, 512 MB/CPU


`Hard Disk Requirement`

| Installation Scope                         | Minimum Hard Disk Requirements |
| ------------------------------------------ | ------------------------------ |
| Text Mode                                  | 1.5 GB                         |
| Minimal System                             | 2.5 GB                         |
| GNOME Desktop                              | 3 GB                           |
| All patterns                               | 4 GB                           |
| Recommended Minimum (no Btrfs snapshots)   | 10 GB                          |
| Required Minimum (with Btrfs snapshots)    | 16 GB                          |
| Recommended Minimum (with Btrfs snapshots) | 32 GB                          |


---

## Boot Parameters

### Boot Parameters

```
setparams 'Installation'

   set gfxpayload=keep
   echo 'Loading kernel ...'
   linuxefi /boot/x86_64/loader/linux splash=silent
   echo 'Loading initial ramdisk ...'
   initrdefi /boot/x86_64/loader/initrd
```


### General Boot Parameters

autoyast=<URL>

manual=<0|1>

Info=<URL>

upgrade=<0|1>

dud=<URL>

language=<LANGUAGE>

```
cs_CZ, de_DE, es_ES, fr_FR, ja_JP, pt_BR, pt_PT, ru_RU, zh_CN, zh_TW
```

acpi=off

noapic

nomodeset

textmode=1

console=SERIAL_DEVICE[,MODE]


### Configuring the Network Interface

netsetup=<VALUE>

ie: netsetup=-dhcp, netsetup=hostip,netmask,gateway,nameserver

ifcfg=<INTERFACE>[.<VLAN>]=[.try,]<SETTINGS>

```
ifcfg=*="10.0.0.10/24,10.0.0.1,10.0.0.1 10.0.0.2,example.com"

ifcfg=eth0=dhcp,MTU=1500
```

hostname=host.example.com

domain=example.com

hostip=192.168.1.2[/24]

gateway=192.168.1.3

nameserver=192.168.1.4

domain=example.com


### Specifying the Installation Source

install=<SOURCE>

```
install=ftp://USER:PASSWORD@SERVER/DIRECTORY/DVD1/

install=smb://WORKDOMAIN;USER:PASSWORD@SERVER/DIRECTORY/DVD1/

install=cd:/
install=hd:/?device=sda/PATH_TO_ISO
install=slp:/
```


### Specifying Remote Access

display_ip=<IP_ADDRESS>

vnc=1

vncpassword=<PASSWORD>

ssh=1

ssh.password=<PASSWORD>


### Advanced Setups

regurl

```
regurl=https://smt.example.com/center/regsvc/
```

regcert

```
regcert=http://rmt.example.com/smt-ca.crt

regcert=/data/inst/smt/smt-ca.cert

regcert=ask

regcert=done
```


### Using IPv6 for the Installation


`Accept IPv4 and IPv6`

```
ipv6=1
```


`Accept IPv6 only`

```
ipv6only=1
```


### Using a Proxy for the Installation

```
proxy=http://USER:PASSWORD@proxy.example.com:POR

http://proxy.example.com:PORT
```


---

## Expert Partitioner

### Using the Expert Partitioner

```bash
sle15:~ # parted <DEVICE> set <PARTITION_NUMBER> msftdata off
```


### Expert Options

`swap`

```bash
sle:~ # mkdir -p /var/lib/swap
sle:~ # dd if=/dev/zero of=/var/lib/swap/swapfile bs=1M count=128
sle:~ # mkswap /var/lib/swap/swapfile

sle:~ # swapon /var/lib/swap/swapfile
sle:~ # swapoff /var/lib/swap/swapfile

sle:~ # cat /proc/swaps

sle:~ # vi /etc/fstab
/var/lib/swap/swapfile swap swap defaults 0 0
...
```
