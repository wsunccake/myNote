# docker

## install

```bash
fedora:~ # dnf remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-selinux \
    docker-engine-selinux \
    docker-engine
fedora:~ # dnf config-manager addrepo --from-repofile="https://download.docker.com/linux/fedora/docker-ce.repo"
fedora:~ # dnf list docker-ce --showduplicates | sort -r
fedora:~ # dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## uninstall

```bash
fedora:~ # dnf remove docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    docker-ce-rootless-extras

fedora:~ # rm -rf /var/lib/{docker,containerd}
```

## service

```bash
fedora:~ # systemctl enable --now docker
fedora:~ # systemctl status docker
fedora:~ # systemctl start docker
fedora:~ # systemctl enable docker
fedora:~ # systemctl disable docker
fedora:~ # systemctl stop docker

fedora:~ # usermod -aG docker <user>
```

## test

```bash
fedora:~ $ docker run hello-world
```

## ssl/tls

```bash
fedora:~ $ cat /etc/docker/daemon.json
{
    "insecure-registries": ["<registry_host>"]
}
```
