# building running and managing container

## starting with container

podman - For directly managing pods and container images (run, stop, start, ps, attach, exec, and so on)
buildah - For building, pushing and signing container images
skopeo - For copying, inspecting, deleting, and signing images
runc - For providing container run and build features to podman and buildah

podman - Client tool for managing containers. Can replace most features of the docker command for working with individual containers and images.
buildah - Client tool for building OCI-compliant container images.
skopeo - Client tool for copying container images to and from container registries. Includes features for signing and authenticating images as well.
runc - Container runtime client for running and working with Open Container Initiative (OCI) format containers.


```bash
centos:~ # dnf module install container-tools
centos:~ # dnf install podman-docker
centos:~ # touch /etc/containers/nodocker
```

/var/lib/containers
$HOME/.local/share/containers


### set up for rootless container


```bash
centos:~ # dnf install slirp4netns podman
centos:~ # echo "user.max_user_namespaces=28633" > /etc/sysctl.d/userns.conf
centos:~ # sysctl -p /etc/sysctl.d/userns.conf

centos:~ # podman info
```

```bash
centos:~ $ podman search ubi
centos:~ $ podman pull registry.access.redhat.com/ubi8-minimal
centos:~ $ podman run registry.access.redhat.com/ubi8-minimal cat /etc/os-release

centos:~ # cat /etc/subuid
centos:~ # cat /etc/subgid
```


---

## working with container image

### pulling images from registry

```bash
centos:~ # podman pull registry.redhat.io/ubi8/ubi
centos:~ # podman tag registry.redhat.io/ubi8/ubi registry.example.com:5000/ubi8/ubi
centos:~ # podman push registry.example.com:5000/ubi8/ubi

centos:~ # grep -vE '^#' /etc/containers/registries.conf
centos:~ # podman search quay.io/
centos:~ # podman login quay.io
centos:~ # podman search postgresql-10
centos:~ # podman search registry.redhat.io/postgresql-10
```

/etc/containers/registries.conf
$HOME/.config/containers/registries.conf


### inspecting local image

```bash
centos:~ # podman pull <registry>[:<port>]/[<namespace>/]<name>:<tag>

centos:~ # podman images
centos:~ # podman inspect registry.redhat.io/ubi8/ubi
centos:~ # podman run -d registry.redhat.io/ubi8/ubi
centos:~ # podman ps

centos:~ # skopeo inspect docker://registry.redhat.io/ubi8/ubi-init

centos:~ # podman tag <image_id> <registry>[:<port>]/[<namespace>/]<name>:<tag>
```


### saving and loading image

```bash
centos:~ # podman save -o myrsyslog.tar registry.redhat.io/rhel8/rsyslog:latest
centos:~ # podman load -i myrsyslog.tar
```


### removing image

```bash
centos:~ # podman rmi ubi8-init
centos:~ # podman rmi -a
centos:~ # podman rmi -f <image_id>
```


---

## working with container and pod

### running container

```bash
centos:~ # podman run --rm registry.redhat.io/ubi8/ubi cat /etc/os-release

centos:~ # podman run --name=mybash -it registry.redhat.io/ubi8/ubi /bin/bash
centos:~ # podman ps -a
centos:~ # podman start -ai mybash

centos:~ # podman run --name="log_test" -v /dev/log:/dev/log --rm registry.redhat.io/ubi8/ubi logger "Testing logging to the host"
centos:~ # journalctl -b

centos:~ # podman run -d --name=mylog --ip=10.88.0.44 registry.access.redhat.com/rhel7/rsyslog
centos:~ # podman inspect mylog
centos:~ # podman inspect --format='{{.NetworkSettings.IPAddress}}' mylog
```


### investigating running and stopped container

```bash
centos:~ # podman exec -it 74b1da000a11 /bin/bash
centos:~ # podman start myrhel_httpd
centos:~ # podman start -a -i agitated_hopper
centos:~ # podman stop 74b1da000a11
centos:~ # podman kill --signal="SIGHUP" 74b1da000a11
```


### sharing files between two container

```bash
centos:~ # podman volume create hostvolume
centos:~ # podman volume inspect hostvolume

centos:~ # echo "Hello from host" >> $mntPoint/host.txt
centos:~ # ls $mntPoint/

centos:~ # podman run -it --name myubi1 -v $mntPoint:/containervolume1 registry.access.redhat.com/ubi8/ubi /bin/bash
centos:~ # podman run -it --name myubi2 -v $mntPoint:/containervolume2 registry.access.redhat.com/ubi8/ubi  /bin/bash

centos:~ # podman volume ls
centos:~ # podman volume rm hostvolume
```


### removing container

```bash
centos:~ # podman rm goofy_wozniak
centos:~ # podman rm clever_yonath furious_shockley drunk_newton
centos:~ # podman rm -a
```


### creating pod

```bash
centos:~ # podman pod create --name mypod
centos:~ # podman pod ps
centos:~ # podman ps -a --pod

centos:~ # podman run -dt --name myubi --pod mypod registry.access.redhat.com/ubi8/ubi  /bin/bash
centos:~ # podman pod ps
centos:~ # podman ps -a --pod
```


### displaying pod information

```bash
centos:~ # podman pod top mypod
centos:~ # podman pod stats -a --no-stream
centos:~ # podman pod inspect mypod
```


### stopping pod

```bash
centos:~ # podman pod stop mypod
centos:~ # podman ps -a --pod
```


### removing pod

```bash
centos:~ # podman pod rm mypod
centos:~ # podman ps
centos:~ # podman pod ps
```
