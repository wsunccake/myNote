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
sle:~ # zypper -v in --download-only -f <pkg>
```

---

## SUSE Package Hub

[How to use](https://packagehub.suse.com/how-to-use/)

[SUSE Package Hub](https://packagehub.suse.com/)
