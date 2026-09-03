# docker ce

```bash
# repo
rocky:~ # dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo

# package
rocky:~ # dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# service
rocky:~ # systemctl --now enable docker

# permission
rocky:~ # usermod -aG docker <user>
```
