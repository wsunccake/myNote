# Docker


## Install

```bash
rhel:~ # cat /etc/yum.repo.d/docker.repo
[virt7-docker-common-testing]
name=virt7-docker-common-testing
baseurl=http://cbs.centos.org/repos/virt7-docker-common-testing/x86_64/os/ 
enabled=1
gpgcheck=0

rhel:~ # yum install docker

rhel:~ # vi /etc/sysconfig/docker                           # 啟動設定
OPTIONS='-G dockerroot --selinux-enabled --log-driver=journald --signature-verification=false --bip=10.253.42.1/16 --storage-opt dm.loopdatasize=200G --storage-opt dm.loopmetadatasize=10G --storage-opt dm.basesize=50G -g /home/docker'
...

rhel:~ # systemctl start docker.service                     # 啟動服務
rhel:~ # systemctl enable docker.service                    # 常駐服務
rhel:~ # docker run hello-world                             # 測試

rhel:~ # usermod -aG docker user                            # 將使用者加入 docker 群組, 確定 docker daemon -G docker
```


---

## PWD/

[http://labs.play-with-docker.com/](http://labs.play-with-docker.com/)


---

## Run

![docker_intro](https://smlsunxie.gitbooks.io/docker-book/content/basic/images/docker-stages.png)

```bash
rhel:~ # docker info
rhel:~ # docker run -it centos /bin/bash                    # 啟用 centos image 的 container, i: inter active mode, t: terminal
rhel:~ # docker run -it --name my_centos centos /bin/bash   # 指令 container name
rhel:~ # docker run -itdP centos /bin/bash                  # d: background mode, P: container port forwading (當 image 有先定義 EXPOSE 才會有效)

rhel:~ # docker exec <container_id> /bin/sh                 # 在 host 端送 command 到 container 端執行

# docker exec <container_id> /bin/sh then show below error
# rpc error: code = 2 desc = oci runtime error: exec failed: container_linux.go:247: starting container process caused "process_linux.go:75: starting setns process caused \"fork/exec /
rhel:~ # nsenter --target <container_id_pid>  --mount --uts --ipc --net --pid /bin/sh
rhel:~ # nsenter --target <container_id_pid>  --mount --uts --ipc --net --pid

rhel:~ # dock ps                                            # 顯示執行中的 container
rhel:~ # dock ps -l                                         # 顯示最後一個 container
rhel:~ # dock ps -a  [ -f status=exited]                    # 顯示所有的 container (包括未執行的)
rhel:~ # dock ps -aq                                        # 顯示所有的 container id (包括未執行的)

rhel:~ # docker rm <container_id>                           # 刪除 container

rhel:~ # docker start <container_id>                        # 啟動 container
rhel:~ # docker stop <container_id>                         # 停止 container
rhel:~ # docker restart <container_id>                      # 重啟 container
rhel:~ # docker kill <container_id>                         # 強制停止 container

rhel:~ # docker attch <container_id>                        # 進入 container, deattch 使用 ctrl^p ctrl^q
rhel:~ # docker exec -it  /bin/exec           # 進入 container
rhel:~ # docker exec -it <container_id> sh -c "echo \$DEBUG_LEVEL"  # 顯示環境變數
rhel:~ # docker show variable


rhel:~ # docker top <container_id>
rhel:~ # docker logs -ft <container_id>
rhel:~ # docker stats <container_id>
rhel:~ # docker inspect <container_id>
rhel:~ # docker inspect --format '{{.State.Pid}}' <container_id>
rhel:~ # docker inspect --format '{{.NetworkSettings.IPAddress}}' <container_id>
```


```bash
rhel:~ # docker run/update
--cpus 4.0
--cpu-shares 1024
--cpuset-cpus=4-7
# cpus 使用數量
# cpu-shares 使用比例, default 1024
# cpuset-cpus 限制使用

--memory 4g
--memory-swap
--memory-swappiness
--memory-reservation
# memory 使用數量, unit: b, k, m, g

--oom-kill-disable
--oom-score-adj

--device=/dev/sdc:/dev/xvdc
--device=/dev/sda
--device-read-bps /dev/sda:1mb
--device-write-bps
--device-read-iops /dev/sda:100
--device-write-iops
# device-read-bps, device-write-bps, unit: kb, mb, gb
```

docker cpu/mem/io info

```bash
rhel:~ # ls /sys/fs/cgroup/cpu/docker/<docker_id>
rhel:~ # ls /sys/fs/cgroup/memory/docker/<docker_id>
rhel:~ # ls /sys/fs/cgroup/blkio/docker/<docker_id>
```


---

## Docker Image 

```bash
rhel:~ # docker search archlinux                            # 搜尋 Docker Hub 上的 image
rhel:~ # curl https://registry.hub.docker.com/v2/repositories/library/archlinux/tags/ | jq -m python.tool                   # 顯示 tag
rhel:~ # curl https://registry.hub.docker.com/v2/repositories/library/archlinux/tags/ | jq '."results"[]["name"]' | sort    # 顯示 tag
rhel:~ # curl https://registry.hub.docker.com/v2/repositories/library/python/tags/ | jq '.results[].name'
rhel:~ # curl https://registry.hub.docker.com/v2/repositories/library/python/tags/ | jq '.results[] | {name: .name}'


rhel:~ # docker images                                      # 顯示本機上的 images

rhel:~ # docker pull base/archlinux                         # 從 Docker Hub 下載 image
rhel:~ # docker pull ubuntu:last                            # 下載 image 並指定 tag

rhel:~ # docker rmi hello-world                             # 刪除 image
rhel:~ # docker rmi -f hello-world                          # 強制刪除 image
```

`method 1`

已有的 image 上 create image

```bash
rhel:~ # docker commit -m -a <container_id> <image_name> [tag]
```

`method 2`

匯入 LXC template, 可到 [OpenVZ 下載](https://openvz.org/Download/template/precreated)

```bash
rhel:~ # docker import http://download.openvz.org/template/precreated/suse-13.1-x86_64-minimal.tar.gz <image_name[:tag]>

rhel:~ # wget http://download.openvz.org/template/precreated/suse-13.1-x86_64-minimal.tar.gz
rhel:~ # cat suse-13.1-x86_64-minimal.tar.gz | docker import - <image_name[:tag]>
```

`method 3`

從 dockerfile 產生

```bash
rhel:~ # mkdir test_img
rhel:~ # cd test_img/
rhel:~/test_img # cat Dockerfile
# FROM  image  指定 image
# FROM  image:tag
FROM  busybox

# MAINTAINER  指定維護者資訊
MAINTAINER  user@com

# RUN  cmd  指定建構 image 時執行動作
# RUN  ["cmd1", "cmd2", ...]
RUN  echo "Hello World"
RUN  date

# CMD  cmd param1 param2 ...  指定啟動 container 時的動作, param 可以省略.只能出現一次, 若多次, 以最後一次為主
# CMD  ["cmd", "param1", ...]
CMD /bin/sh

# ENTRYPOINT  cmd param1 param2 ...
# ENTRYPOINT  ["cmd", "param1", ...]

# EXPOSE 22 53/udp 80/tcp  指定 container 對外開放的 port
EXPOSE  22 80 9000

# ENV
# ADD
# COPY
# VOLUME
# USER
# WORKDIR
# ONBUILD

rhel:~/test_img # docker build -t test_image .
rhel:~/test_img # docker images test_image
```

`import / export, save / load`

```bash
rhel:~ # docker save <image_name[:tag]> > <image>.tar
rhel:~ # docker load <image_name[:tag]> < <image>.tar

rhel:~ # docker export <container_id> > image.tar
rhel:~ # docker import image.tar <image_name>
```


---

## Docker Volume ##

`container`

```bash
rhel:~ # docker run -it --name webser -v /opt/webapp centos /bin/bash # -v: 建立 /opt/webapp
rhel:~ # docker exec webser ls /opt
```

`host - container`

- folder

將 host 的目錄直接給 container 使用

```bash
rhel:~ # docker run -it --name webser -v /tmp/webapp:/opt/webapp centos /bin/bash
rhel:~ # touch /tmp/webapp/tmp_file
rhel:~ # docker exec webser ls /opt/webapp
rhel:~ # docker inspect --format '{{.Mounts}}' webser # 顯示 volume
```

預設在 /var/lib/docker/volumes, 刪掉 container 時, volume 還會不會自動刪除, 要手動清除

- file

將 host 的檔案直接給 container 使用

```bash
rhel:~ # docker run -it -v /tmp/lxc_1.history:/root/.history centos /bin/bash
rhel:~ # docker run -it -v /tmp/config:/etc/app/config:ro centos /bin/bash # 使用 read only 模式
```

多個目錄或檔案時, 可同時使用多個 -v folder|file 方式

`container - container`

```bash
rhel:~ # docker run -it --name web_master -v /opt/webapp centos /bin/bash
rhel:~ # docker run -it --name web_slave --volumes-from web_master -v /opt/webapp ubuntu /bin/bash
```

`command`

```bash
rhel:~ # docker volume ls
rhel:~ # docker volume create <vol>
rhel:~ # docker volume inspect <vol>
rhel:~ # docker volume rm <vol>

rhel:~ # docker run -itd -v <vol>:<path> <image>
```

default path: /var/lib/docker/volumes/<vol>


---

## Dokcer Network

docker 在設定 port forwarding 時使用 iptables, 但 RHEL 7 預設的防火牆 firewalld 可能會有問題, 目前建議換成 iptables 或是關掉 firewalld. 在 docker run -P 的使用上, 會隨機將 container 上的 EXPOSE port 對應到 host 上的 49000 ~ 49900 port

`port`

```bash
rhel:~ # docker run -t -d -p 8000:9000 --name nc busybox /bin/sh # -p: host 開啟 8000 port 轉到 container 9000 port

# 從 iptable 觀察
rhel:~ # iptables -L -n
rhel:~ # iptables -S DOCKER

# nic 是透過 bridge-utils
rhel:~ # brctl show

# 顯示 port map
rhel:~ # dock ps nc

# 測試
# container 端使用 nc 開啟 9000 port, 之後在 host 端使用 nc 任意打字, 都會在 container 出現
container:~ # nc -l -p 9000 

# host side
rhel:~ # nc localhost 8000
```

`ip`

`link`

同一台 host 之間的 container 可透過 link 方式互相

```
rhel:~ # docker run -d --name db training/postgres
rhel:~ # docker run -d -P --name web --link db:db training/webapp python app.py
rhel:~ # docker inspect -f "{{ .HostConfig.Links }}" web
```


`multi nic`

```bash
# create network
centos:~ # docker network ls
centos:~ # docker network create blue_network
centos:~ # docker network create red_network

# create container
centos:~ # docker run -td --network=blue_network <container>

# attach network
centos:~ # docker network connect red_network <container>

# verify container
centos:~ # docker inspect <container> | jq '.[0].NetworkSettings.Networks'
centos:~ # docker inspect -f '{{json .NetworkSettings.Networks}}' <container>
centos:~ # docker exec -it <container> ip link show
```


### manual create veth

```bash
# create namespace
centos:~ # ip netns add <ns>

# list namespace
centos:~ # ip netns

# exec namespace
centos:~ # ip link netns <ns> ip link  ~=  ip link netns <ns> <cmd>  # all command
centos:~ # ip -n <ns> link                                           # only for ip command


# create veth
centos:~ # ip link add <veth> type veth peer name <peer>
centos:~ # ip link set <veth> netns <ns>

# delete veth
centos:~ # ip link del <veth> netns <ns>


# create bridge
centos:~ # ip link add <br> type bridge
centos:~ # ip link set dev <br> up

# add eth to bridge
centos:~ # ip link set <eth> master <br>
```


---

## Docker Hub / Registry

![docker hub](https://smlsunxie.gitbooks.io/docker-book/content/basic/images/docker-hub.png)

```bash
rhel:~ # docker login # 登入 Docker Hub, 設定在 $HOME/.dockercfg
rhel:~ # docker logout

rhel:~ # cat ~/.docker/config.json

rhel:~ # docker tag
rhel:~ # docker push
rhel:~ # docker pull
```

### Registry Server

```bash
server:~ # vi /etc/docker/daemon.json
{
  "live-restore": true,
  "group": "dockerroot",
  "insecure-registries": ["<registry_ip>:5000"]
}

server:~ # systemctl restart docker

# start service
server:~ # docker run -d -p 5000:5000 --restart=always --name registry -v /data/registry:/var/lib/registry registry:2

# delete image
server:~ # rm -rf /data/registry/docker/registry/v2/repositories/<name>

# web
server:~ # docker run -d -p 8080:8080 --restart=always --name registry-web --link registry -e REGISTRY_URL=http://<registry_ip>:5000/v2 hyper/docker-registry-web
```

### Registry Client

```bash
client:~ # vi /etc/docker/daemon.json
{
  "live-restore": true,
  "group": "dockerroot",
  "insecure-registries": ["<registry_ip>:5000"]
}

# upload image
client:~ # docker pull docker.io/busybox
client:~ # docker tag docker.io/busybox <registry_ip>:5000/busybox
client:~ # docker push <registry_ip>:5000/busybox

# list image
client:~ # curl -X GET http://<registry_ip>:5000/v2/_catalog
client:~ # curl -X GET http://<registry_ip>:5000/v2/<name>/tags/list

client:~ # curl -k -X GET https://<registry_ip>:5000/v2/_catalog
client:~ # curl -k -X GET https://<registry_ip>:5000/v2/<name>/tags/list

# download image
client:~ # docker rmi docker.io/busybox <registry_ip>:5000/busybox
client:~ # docker images
client:~ # docker pull <registry_ip>:5000/busybox
```


## Docker File

Docker File 用來在已建立/存在 image 上, 在建立新的 image

```bash
rhel:~ # cat robotframework/Dockerfiles     # create image for robotframework
# comment
FROM centos

RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
RUN yum makecache
RUN yum install -y python-pip
RUN pip install --upgrade pip
RUN pip install robotframework

VOLUME /robot_log

CMD ["/bin/bash"]

rhel:~ # cat nginx/Dockerfiles              # create image for nginx
# comment
FROM centos

RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
RUN yum makecache
RUN yum install -y nginx

CMD ["/bin/bash"]

// create docker image
// syntax:
// docker build  [-t image_name] [.|-f /path/Dockerfile]
rhel:~ # docker -t robot -f robotframework/Dockerfiles
rhel:~ # docker -t nginx -f nginx/Dockerfiles

// create image
rhel:~ # docker run -itd -v /data:/robot_log --name robot robot
rhel:~ # docker run -itd -p 80:80 --name nginx nginx
```


```bash
# dockerfile
rhel:~ # cat Dockerfile
FROM centos

RUN yum install epel
RUN yum makecache
RUN yum install -y nginx

CMD ["/bin/bash"]

# dockerfile
rhel:~ # cat Dockerfile
FROM centos

RUN yum install epel \
 && yum makecache \
 && yum install -y nginx

CMD ["/bin/bash"]

# dockerfile
rhel:~ # cat Dockerfile
FROM centos

RUN <<EOF
yum install epel
yum makecache
yum install -y nginx
EOF

CMD ["/bin/bash"]
```



## Docker Registry

```bash
rhel:~ # docker login
rhel:~ # docker login -u user -p password private_registry:5000

rhel:~ # docker logout

rhel:~ # cat ~/.docker/config.json 
```


---

## Run GUI Apps on Docker


### UNIX X11 Socket

```bash
rhel:~ # cat Dockerfile
FROM ubuntu:14.04

RUN apt-get update && apt-get install -y firefox

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

USER developer
ENV HOME /home/developer
CMD /usr/bin/firefox

rhel:~ # docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw firefox

rhel:~ # docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -e XAUTHORITY=/tmp/.Xauthority -v /home/kam/.Xauthority:/tmp/.Xauthority firefox
```

`Note`

check /tmp/.X11-unix permission (chmod 1777 /tmp/.X11-unix)


### VNC


----

## Docker IPv6

### NAT

`Network Topology`

```
            host_1                  ---     host_2
ens33:      2001:db8:1::1:2/64              2001:db:1::1/64
docker0:    fc00:db8::1/125
            |
            |
            container0
eth0:       fc00:db8::2/125
```


`Enable IPv6`

```bash
host_1:~ # sysctl net.ipv6.conf.default.forwarding=1
host_1:~ # sysctl net.ipv6.conf.all.forwarding=1
host_1:~ # sysctl net.ipv6.conf.all.proxy_ndp=1

host_1:~ # cat /etc/docker/daemon.json 
{
  "ipv6": true,
  "fixed-cidr-v6": "fc00:db8::1/125"
}

host_1:~ # systemctl restart docker
```


`Internal Network`

```
# host ping internel
host_1:~ # ping -6 -c3 2001:db8:1::1:2
host_1:~ # ping -6 -c3 fc00:db8::1
host_1:~ # ping -6 -c3 fc00:db8::2

# container ping internel
host_1:~ # docker exec -it <container> ping -6 -c3 2001:db8:1::1:2
host_1:~ # docker exec -it <container> ping -6 -c3 fc00:db8::1
host_1:~ # docker exec -it <container> ping -6 -c3 fc00:db8::2
```


`External Network`

```
# setup iptable
host_1:~ # ip6tables -t nat -I POSTROUTING -s fc00:db8::1/125 -j MASQUERADE
host_1:~ # ip6tables -I FORWARD ! -i docker0 -o docker0 -m state --state RELATED,ESTABLISHED -j ACCEPT
host_1:~ # ip6tables -I FORWARD -i docker0 ! -o docker0 -j ACCEPT

# host ping external
host_1:~ # ping -6 -c3 2001:db8:1::1

# container ping external
host_1:~ # docker exec -it <container> ping -6 -c3 2001:db8:1::1
```


### Direct

`Network Topology`

```
            host_1                  ---     host_2
ens33:      2001:db8:1::1:2/64              2001:db:1::1/64
docker0:    2001:db8:1::1:9/125
            |
            |
            container0
eth0:       2001:db8:1::1:a/125
```


`Enable IPv6`

```bash
host_1:~ # sysctl net.ipv6.conf.default.forwarding=1
host_1:~ # sysctl net.ipv6.conf.all.forwarding=1
host_1:~ # sysctl net.ipv6.conf.all.proxy_ndp=1

host_1:~ # cat /etc/docker/daemon.json 
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::1:8/125"
}

host_1:~ # systemctl restart docker
```


`Internal Network`

```bash
# routing setup
host_1:~ # ip -6 route add <container_subnet>/<prefix> dev <docker_bridge>
host_1:~ # ip -6 route add 2001:db8:1::/64 dev docker0
host_1:~ # ip -6 route show
host_1:~ # docker exec -it <container> sh -c "ip -6 addr show; ip -6 route show"

# host ping internel
host_1:~ # ping -6 -c3 2001:db8:1::1:2
host_1:~ # ping -6 -c3 2001:db8:1::1:9
host_1:~ # ping -6 -c3 2001:db8:1::1:a

# container ping internel
host_1:~ # docker exec -it <container> ping -6 -c3 2001:db8:1::1:2
host_1:~ # docker exec -it <container> ping -6 -c3 2001:db8:1::1:9
host_1:~ # docker exec -it <container> ping -6 -c3 2001:db8:1::1:a
```


`External Network`

```bash
# ndp setup
host_1:~ # ip -6 neigh add proxy <container_ip> dev <host_nic>
host_1:~ # ip -6 neigh add proxy 2001:db8:1::1:a dev ens33
host_1:~ # ip -6 neigh show
host_1:~ # ip -6 neigh show proxy

# host ping external
host_1:~ # ping -6 -c3 2001:db8:1::1

# container ping external
host_1:~ # docker exec -it <container> ping -6 -c3 2001:db8:1::1
```


---

## GUI

### Portainer

```bash
rhel: # docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock --name portainer portainer/portainer
```


---

## Ref

[docker](https://docs.docker.com/)

[Docker —— 從入門到實踐­](https://www.gitbook.com/book/philipzheng/docker_practice/details)

[docker-book](https://www.gitbook.com/book/smlsunxie/docker-book)

[Using GUI's with Docker](http://wiki.ros.org/docker/Tutorials/GUI)

[Running GUI apps with Docker](http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/)

