# rocky linux 10

## cli

```bash
rocky:~ # dnf makecache
# --nogpgcheck              停用 GPG 簽名檢查
# --setopt=sslverify=false  停用 SSL 憑證驗證
# --assumeyes               自動將所有的詢問都回答為 "yes"

# repo
rocky:~ # dnf install epel-release
rocky:~ # dnf repolist --all
rocky:~ # dnf config-manager --set-enabled epel-testing
rocky:~ # dnf config-manager --set-enabled crb

# cli
rocky:~ # dnf install bash-completion bash-color-prompt
rocky:~ # dnf install vim-common vim-enhanced
```

---

## system

### cockpit

```bash
rocky:~ # dnf install cockpit

rocky:~ # curl http://127.0.0.1:9090
```

---

## scheduling system

### slurm

- [SchedMD](https://www.schedmd.com/)

`require`

```bash
rocky:~ # dnf install munge munge-devel                 # repo: appstream, crb
rocky:~ # dnf install readline-devel mariadb-devel      # repo: appstream
rocky:~ # dnf install perl perl-devel
rocky:~ # dnf install pam-devel rpm-build rpmdevtools
rocky:~ # dnf group install development
```

`build`

```bash
rocky:~ $ curl -LO https://download.schedmd.com/slurm/slurm-25.11.1.tar.bz2
rocky:~ $ rpmbuild -ta slurm-25.11.1.tar.bz2

rocky:~ $ ls rpmbuild/RPMS/x86_64/
```
