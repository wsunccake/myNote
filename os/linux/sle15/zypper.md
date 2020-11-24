# zypper


## repository

```bash
# add repo
suse:~ # zypper ar "dir:///<path>/<folder>" <repo>
suse:~ # zypper ar "iso:/?iso=/<path>/<img>.iso" <repo>

# list repo
suse:~ # zypper lr

# remove repo
suse:~ # zypper rr <repo>

# repo config
suse:~ # ls /etc/zypp/repos.d
```


---

## package

```bash
# search package
suse:~ # zypper se <pkg>
suse:~ # zypper pt

# install package
suse:~ # zypper in <pkg>
suse:~ # zypper in -t pattern <pattern>

# remove package
suse:~ # zypper rm <pkg>
```

---

## SUSE Package Hub

[How to use](https://packagehub.suse.com/how-to-use/)

[SUSE Package Hub](https://packagehub.suse.com/)
