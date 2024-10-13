# dnf

## module

```bash
[centos:~ ] # dnf module list [<module>]
[centos:~ ] # dnf module info <module>[:<stream>]
[centos:~ ] # dnf module info --profile <module>[:<stream>]
[centos:~ ] # dnf module install <module>
```

---

## content

```bash
[centos:~ ] # dnf list
[centos:~ ] # dnf repoquery [-l] [<package>]
[centos:~ ] # dnf search <package>
[centos:~ ] # dnf info <package>
[centos:~ ] # dnf module provides <package>
```

---

## install

```bash
[centos:~ ] # dnf install <package>
[centos:~ ] # dnf module enable <module>:<stream>
[centos:~ ] # dnf module install <module>[:<stream>][/<profile>]
[centos:~ ] # dnf install @<module>[:<stream>][/<profile>]
```

---

## remove

```bash
[centos:~ ] # dnf remove <package>
[centos:~ ] # dnf module disable <module>:<stream>
[centos:~ ] # dnf module remove [--all] <module>[:<stream>][/<profile>]
```

---

## other

```bash
[centos:~ ] # dnf module reset <module>:<stream>
[centos:~ ] # dnf autoremove
[centos:~ ] # dnf clean all
```
