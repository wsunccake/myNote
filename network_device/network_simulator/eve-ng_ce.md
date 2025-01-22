# EVE-NG CE 6.x

Emulated Virtual Environment Next Generation Community Edition

## package

### eve-ng ce

- Free EVE Community Edition
- Widnwos Client Side / Apple OSX Clinet Side / Linux Client Side

- [Download Links and info for EVE-NG](https://www.eve-ng.net/index.php/download/)

### hypervisor

- VMWare Workstation (for windows, linux)
- VMWare Fusion (for mac)

- [Desktop Hypervisor](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion)

### image

IOL (Cisco IOS on Linux)

- i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20190423.bin (cisco L2 swtich)
- i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin (cisco L3 router)
- vios-adventerprisek9-m.SPA.159-3.M6
- viosl2-adventerprisek9-m.SSA.high_iron_20200929

- [Cisco-Images-for-GNS3-and-EVE-NG Public](https://github.com/hegdepavankumar/Cisco-Images-for-GNS3-and-EVE-NG)

### other

- CiscoIOUKeygen.py

```python
#!/usr/bin/python
print("*********************************************************************")
print("Cisco IOU License Generator - Kal 2011, python port of 2006 C version")
print("Modified to work with python3 by c_d 2014")
import os
import socket
import hashlib
import struct

# get the host id and host name to calculate the hostkey
hostid=os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey=int(hostid,16)
for x in hostname:
 ioukey = ioukey + ord(x)
print("hostid=" + hostid +", hostname="+ hostname + ", ioukey=" + hex(ioukey)[2:])

# create the license using md5sum
iouPad1 = b'\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
iouPad2 = b'\x80' + 39*b'\0'
md5input=iouPad1 + iouPad2 + struct.pack('!L', ioukey) + iouPad1
iouLicense=hashlib.md5(md5input).hexdigest()[:16]

print("\nAdd the following text to ~/.iourc:")
print("[license]\n" + hostname + " = " + iouLicense + ";\n")
print("You can disable the phone home feature with something like:")
print(" echo '127.0.0.127 xml.cisco.com' >> /etc/hosts\n")
```

- [EVE-NG Collection](https://drive.google.com/drive/folders/1Y-C4p8PK3BjMt5x7-0LkF0Xb-GFRWGYa)

---

## install

### install hypervisor

install vmware workstation / fusion

### create vm

create guest vm

Guest OS -> Ubuntu
Version -> 64-bit
Processor -> set Virtualize Intel VT-x/EPT or AMD-V/RVI and set Virtualize IOMMU

### configure eve

CLI login: root/eve
GUI login: admin/eve

```bash
eve-ng:~ # apt update
eve-ng:~ # apt upgrade
eve-ng:~ # dpkg -l eve-ng
```

### client - mac

```bash
osx:~ # curl -OL http://<eve-ng ip>/files/osx.zip
osx:~ # unzip osx.zip
osx:~ # cp OSX/telnet /usr/local/bin
osx:~ # cp OSX/ftp /usr/local/bin
```

### test

add new lab -> Virtual PC (VPCS)

---

## addon image

### iou / iol

```bash
client:~ # scp CiscoIOUKeygen.py root@<eve-ng ip>:/opt/unetlab/addons/iol/bin/.
client:~ # scp i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20190423.bin root@<eve-ng ip>:/opt/unetlab/addons/iol/bin/.
client:~ # scp i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin root@<eve-ng ip>:/opt/unetlab/addons/iol/bin/.
```

```bash
eve-ng:/opt/unetlab/addons/iol/bin # python3 CiscoIOUKeygen.py > iourc

# file permission
eve-ng:/opt/unetlab/addons/iol/bin # chmod 755 i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20190423.bin
eve-ng:/opt/unetlab/addons/iol/bin # chmod 755 i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin

# file permission
eve-ng:/opt/unetlab/addons/iol/bin # /opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```

### vios

```bash
client:~ # scp vios-adventerprisek9-m.SPA.159-3.M6.tgz root@<eve-ng ip>:/opt/unetlab/addons/qemu/.
client:~ # scp viosl2-adventerprisek9-m.ssa.high_iron_20200929.tgz root@<eve-ng ip>:/opt/unetlab/addons/qemu/.
```

```bash
eve-ng:/opt/unetlab/addons/qemu # tar xvf vios-adventerprisek9-m.SPA.159-3.M6.tgz
eve-ng:/opt/unetlab/addons/qemu # chmod 755 vios-adventerprisek9-m.SPA.159-3.M6/virtioa.qcow2
eve-ng:/opt/unetlab/addons/qemu # tar xvf viosl2-adventerprisek9-m.ssa.high_iron_20200929.tgz
eve-ng:/opt/unetlab/addons/qemu # chmod 755 viosl2-adventerprisek9-m.ssa.high_iron_20200929/virtioa.qcow2
```

---

## ref

- [eve-ng](https://www.eve-ng.net/)
