# docker

## install

```bash
# package
sle:~ # zypper in docker

# service
sle:~ # systemctl enable docker --now

# add user
sle:~ # usermod -aG docker <user>
```

[Red Hat](https://hub.docker.com/u/redhat)
[SUSE Container Images & Applications](https://registry.suse.com/repositories)
[opensuse/leap](https://hub.docker.com/r/opensuse/leap)

Red Hat Universal Base Image (UBI)
SUSE Linux Enterprise Base Container Images (SLE BCI)

```bash
sle:~ # docker pull redhat/ubi10
sle:~ # docker pull registry.suse.com/bci/bci-base:15.7
sle:~ # docker pull opensuse/leap
```
