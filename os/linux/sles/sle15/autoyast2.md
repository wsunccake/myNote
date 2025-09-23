# autoyast2

## install

```bash
sle:~ # zypper in autoyast2
sle:~ # zypper in autoyast2-installation
```

## usage

```bash
# collect current system all setting to generate autoinst.xml
sle:~ # yast clone_system

# modify autoinst.xml
sle:~ # yast autoyast

# check syntax
sle:~ # xmllint autoinst.xml

# check
sle:~ # yast autoyast check-profile filename=autoinst.xml output=result.xml
sle:~ # yast autoyast check-profile filename=autoinst.xml output=result.xml
sle:~ # yast autoyast check-profile filename=autoinst.xml output=result.xml run-scripts=true
sle:~ # yast autoyast check-profile filename=autoinst.xml output=result.xml import-all=false
# filename=autoinst.xml
# filename=http://192.168.0.1/autoinst.xml
```

## pxe

```conf
# /srv/tftpboot/pxelinux.cfg/default
DEFAULT linux
PROMPT 0
TIMEOUT 100
MENU TITLE SUSE Linux Enterprise Server 15

LABEL linux
    MENU LABEL SLES 15 Installation
    KERNEL sle15sp7/linux
    APPEND initrd=sle15sp7/initrd install=http://192.168.0.1/sle15/ autoyast=http://192.168.0.1/autoinst.xml
```
