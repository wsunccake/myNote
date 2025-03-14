# dnf

BaseOS

AppStream

## alias

| command   | alias |
| --------- | ----- |
| list      | ls    |
| info      | if    |
| search    | se    |
| install   | in    |
| remove    | rm    |
| makecache | mc    |
| repoquery | rq    |
| group     | grp   |
| history   | hist  |

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

rocky:~ # dnf group list [--hidden|--available|--installed]
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

rocky:~ # dnf repolist -v
```

### add dvd media

```bash
rocky:~ # cat /etc/yum.repo.d/media.repo
[Media-BaseOS]
name=media-baseos
baseurl=file:///media/rocky9/BaseOS
enabled=1
gpgcheck=0
priority=1
# gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7

[Media-AppStream]
name=meedia-appstream
baseurl=file:///media/rocky9/AppStream
enabled=1
gpgcheck=0
priority=2

rocky:~ # dnf clean all
rocky:~ # dnf repolist -v
rocky:~ # dnf makecache
```

## other

```bash
# curl error (60) - SSL certificate problem: self-signed certificate in certificate chain
# method 1. stop ssl certificate
rocky:~ # dnf --setopt=sslverify=false makecache

# method 2. update ssl certificate
```
