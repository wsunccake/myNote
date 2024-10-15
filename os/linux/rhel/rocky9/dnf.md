# dnf

BaseOS

AppStream

## module

```bash
rocky:~ # dnf module list [<module>]
rocky:~ # dnf module info <module>[:<stream>[/<profile>]]
rocky:~ # dnf module info --profile <module>[:<stream>]
rocky:~ # dnf module install <module>
rocky:~ # dnf module provides <package>
```

---

## configure

```bash
rocky:~ # dnf config-manager --dump
rocky:~ # vi /etc/dnf/dnf.conf
```

---

## search

```bash
rocky:~ # dnf search [--all] <package>
rocky:~ # dnf list [--all]

rocky:~ # dnf repoquery [-l] [<package>]
rocky:~ # dnf repoinfo <repo>

rocky:~ # dnf provides <file>
rocky:~ # dnf info <package>
rocky:~ # dnf repoquery --info <package>

rocky:~ # dnf group list
rocky:~ # dnf group info "<group>"
rocky:~ # dnf group summary
```

---

## install

```bash
rocky:~ # dnf install <package1> <package2> ...
rocky:~ # dnf install <package>.<arch>
rocky:~ # dnf install <path_to_file>
rocky:~ # dnf install <rpm>
```

---

## update

```bash
rocky:~ # dnf check-update
rocky:~ # dnf upgrade
rocky:~ # dnf upgrade <package>
rocky:~ # dnf group upgrade <group>

rocky:~ # dnf upgrade --security
rocky:~ # dnf upgrade-minimal --security
```

---

## remove

```bash
rocky:~ # dnf remove <package1> <package2> ...
rocky:~ # dnf group remove <group>
rocky:~ # dnf module remove <module-name:stream/profile>
```

---

## history

```bash
rocky:~ # dnf history
rocky:~ # dnf history list <package_name>
rocky:~ # dnf history info <transaction_id>
rocky:~ # dnf history undo <transaction_id>
rocky:~ # dnf history rollback <transaction_id>
```

---

## repository

```bash
rocky:~ # dnf config-manager --add-repo <repository_URL>
rocky:~ # cat /etc/yum.repos.d/<repository_URL>.repo
rocky:~ # dnf config-manager --enable <repository_id>
rocky:~ # dnf config-manager --disable <repository_id>
```
