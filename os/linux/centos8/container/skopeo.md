# skopeo

## install

```bash
[centos:~] # dnf install skopeo

[centos:~] # skopeo --version
[centos:~] # skopeo --help
```


---

## usage

```bash
[centos:~] # skopeo inspect docker://registry.access.redhat.com/ubi8-minimal

[centos:~] # TMP_DIRmktemp -d
[centos:~] # skopeo copy docker://registry.access.redhat.com/ubi8-minimal:latest dir:${TMP_DIR}
[centos:~] # skopeo delete docker://<registry>/<repo>/<image>
```
