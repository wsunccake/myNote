# docker

## install

```bash
# remove podman
alma:~ # dnf -y remove podman runc

# add repo
alma:~ # curl https://download.docker.com/linux/centos/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
alma:~ # sed -i -e "s/enabled=1/enabled=0/g" /etc/yum.repos.d/docker-ce.repo
alma:~ # dnf --enablerepo=docker-ce-stable -y install docker-ce

# service
alma:~ # systemctl enable --now docker

# add group
alma:~ # usermod -aG docker <user>

# testing
alma:~ # docker version
```
