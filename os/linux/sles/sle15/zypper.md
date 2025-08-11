# zypper

## repository

```bash
# add repo
sle:~ # zypper ar "dir:///<path>/<folder>" <repo>
sle:~ # zypper ar "iso:/?iso=/<path>/<img>.iso" <repo>

# list repo
sle:~ # zypper lr

# remove repo
sle:~ # zypper rr <repo>

# repo config
sle:~ # ls /etc/zypp/repos.d
```

---

## package

```bash
# search package
sle:~ # zypper se <pkg>
sle:~ # zypper pt

# install package
sle:~ # zypper in <pkg>
sle:~ # zypper in -t pattern <pattern>

# remove package
sle:~ # zypper rm <pkg>

# download package
sle:~ # zypper -v in -d -f <pkg>
# download to /var/cache/zypp/packages
```

---

## SUSE Package Hub

[How to use](https://packagehub.suse.com/how-to-use/)

[SUSE Package Hub](https://packagehub.suse.com/)

```bash
# /usr/sbin/SUSEConnect -> /usr/bin/suseconnect
sle:~ # SUSEConnect -p PackageHub/$SLEVER.$SPNUM/$ARCH
# $SLEVER = Major version of the SUSE Linux Enterprise Product (12 or 15)
# $SPNUM = The service pack number (i.e. 1, 2, 3, 4...)
# $ARCH = The platform architecture (aarch64, ppc64le, s390x, or x86_64)

# activation
sle:~ # SUSEConnect -p PackageHub/15.7/x86_64
# de-register
sle:~ # SUSEConnect -d -p PackageHub/15.7/x86_64

# register
sle:~ # SUSEConnect -r <REGISTRATION_CODE> -e <EMAIL_ADDRESS>

sle:~ # SUSEConnect -i          # show information
sle:~ # SUSEConnect -s          # current system registration status
sle:~ # SUSEConnect -l          # list all extension and module
```
