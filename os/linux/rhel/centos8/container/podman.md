# podman

## install

```bash
[centos:~] # dnf module install container-tools
[centos:~] # dnf install podman-docker
[centos:~] # touch /etc/containers/nodocker
```

/var/lib/containers

$HOME/.local/share/containers

---

## info

```bash
[centos:~] # podman version
[centos:~] # podman info [--debug]
[centos:~] # podman help
```

---

## rootless

```bash
centos:~ # dnf install slirp4netns podman
centos:~ # echo "user.max_user_namespaces=28633" > /etc/sysctl.d/userns.conf
centos:~ # sysctl -p /etc/sysctl.d/userns.conf

centos:~ # podman info
centos:~ # cat /etc/subuid
centos:~ # cat /etc/subgid
```

---

## image

```bash
[centos:~] # podman search <image>
[centos:~] # podman iamges
[centos:~] # podman pull <image>
[centos:~] # podman tag <old image> <new iamge>
[centos:~] # podman rmi <image>
```

image: host/repository/image:tag

/etc/containers/registries.conf

$HOME/.config/containers/registries.conf

---

## container

```bash
[centos:~] # podman run -td [-p <host port>:<container port>] [-v <host path>:<container path>] --name <container name> <image>
[centos:~] # podman ps -a
[centos:~] # podman inspect <container>
[centos:~] # podman rm <container>

[centos:~] # podman start <container>
[centos:~] # podman stop <container>
[centos:~] # podman restart <container>
[centos:~] # podman exec -it <container> <command>

[centos:~] # podman top <container>
[centos:~] # podman stats <container>
```

---

## pod

```bash
[centos:~] # podman pod create -p <host port>:<pod port> --name <pod name>
[centos:~] # podman pod ps
[centos:~] # podman pod inspect <pod>
[centos:~] # podman pod rm <pod>

[centos:~] # podman [pod] start <pod>
[centos:~] # podman [pod] stop <pod>
[centos:~] # podman [pod] restart <pod>

[centos:~] # podman run -td --pod <pod> --name <container name> <image>
[centos:~] # podman ps -a --pod
[centos:~] # podman rm <container>

[centos:~] # podman pod top <pod>
[centos:~] # podman pod stats <pod>
```

---

## build

```bash
[centos:~] # vi main.go
package main

import (
        "fmt"
        "net/http"
)

func handler(writer http.ResponseWriter, request *http.Request) {
        fmt.Fprint(writer, "Hello Go")
}

func main() {
        http.HandleFunc("/", handler)
        http.ListenAndServe(":8080", nil)
}


[centos:~] # vi dockerfile
# multi-stage
# build
FROM  golang:alpine  AS build-env

ADD  main.go /src/main.go
RUN  cd /src && go build -o /app/app main.go


# run
FROM alpine:latest

WORKDIR /app/
COPY --from=build-env /app/app /app/

EXPOSE 8080
ENTRYPOINT ./app


[centos:~] # podman build -t go-app -f dockerfile

# only container
[centos:~] # podman run -itd -p 8080:8080 --name hello go-app
[centos:~] # curl 127.0.0.1:8080

# container on pod
[centos:~] # podman pod create -p 8080:8080 --name web
[centos:~] # podman run -itd --name hello --pod web go-app

# test
[centos:~] # curl http://127.0.0.1:8080
```

---

## service

```bash
[centos:~] # podman generate kube <pod>|<container> > <service>.yaml
[centos:~] # podman play kube <pod>|<container>
```

```bash
[centos:~] # podman generate systemd <pod>|<container> > <service>.service

# for system
[centos:~] # cp <service>.service /etc/systemd/system
[centos:~] # systemctl enable <service>.service

# for user
[centos:~] # cp <service>.service $HOME/.config/systemd/user
[centos:~] # systemctl enable <service>.service --user
```

---

## network

```bash
[centos:~] # podman network ls
[centos:~] # podman network inspect <network>
[centos:~] # podman network create <network>
[centos:~] # podman network rm <network>

[centos:~] # podman port -a
[centos:~] # podman port -l
[centos:~] # podman port <container>
```

---

## volume

```bash
[centos:~] # podman volume ls
[centos:~] # podman volume inspect <volume>
[centos:~] # podman volume create <volume>
[centos:~] # podman volume rm <volume>
```

---

## podman-compose

```bash
[centos:~] # curl -o /usr/local/bin/podman-compose https://raw.githubusercontent.com/containers/podman-compose/devel/podman_compose.py
[centos:~] # chmod +x /usr/local/bin/podman-compose
```
