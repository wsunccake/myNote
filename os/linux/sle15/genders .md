# genders

## install

```bash
sle:~ # zypper install genders
```

---

## config

```ini
# /etc/genders
node001         login,cpus=4,rack=1
node002         login,cpus=8,rack=1
node003         mgmt,cpus=4,rack=2
node00[4-9]     compute,cpus=4,rack=2
```

---

## run

```bash
sle:~ # nodeattr -k
sle:~ # nodeattr -l

sle:~ # nodeattr -c login
sle:~ # nodeattr -q login               # for pdsh format
sle:~ # nodeattr -c "login||mgmt"
sle:~ # nodeattr -c "login&&cpus=4"
sle:~ # nodeattr -c "~(login||mgmt)"
```
