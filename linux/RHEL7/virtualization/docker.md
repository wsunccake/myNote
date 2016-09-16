# Docker


## Install

```
rhel:~ # cat /etc/yum.repo.d/docker.repo
[virt7-docker-common-testing]
name=virt7-docker-common-testing
baseurl=http://cbs.centos.org/repos/virt7-docker-common-testing/x86_64/os/ 
enabled=1
gpgcheck=0

rhel:~ # yum install docker

rhel:~ # systemctl start docker.service                     # 啟動服務
rhel:~ # systemctl enable docker.service                    # 常駐服務
rhel:~ # docker run hello-world                             # 測試

rhel:~ # usermod -aG docker user                            # 將使用者加入 docker 群組, 確定 docker daemon -G docker
```


## Run

![docker_intro](https://smlsunxie.gitbooks.io/docker-book/content/basic/images/docker-stages.png)

```
rhel:~ # docker info
rhel:~ # docker run -it centos /bin/bash                    # 啟用 centos image 的 container, i: inter active mode, t: terminal
rhel:~ # docker run -it --name my_centos centos /bin/bash   # 指令 container name
rhel:~ # docker run -itdP centos /bin/bash                  # d: background mode, P: container port forwading (當 image 有先定義 EXPOSE 才會有效)

rhel:~ # docker exec <container_id> /bin/sh                 # 在 host 端送 command 到 container 端執行

rhel:~ # nsenter --target <container_id_pid>  --mount --uts --ipc --net --pid /bin/sh

rhel:~ # dock ps                                            # 顯示執行中的 container
rhel:~ # dock ps -l                                         # 顯示最後一個 container
rhel:~ # dock ps -a                                         # 顯示所有的 container (包括未執行的)

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
```


## Docker Image 

```
rhel:~ # docker search archlinux                            # 搜尋 Docker Hub 上的 image

rhel:~ # docker images                                      # 顯示本機上的 images

rhel:~ # docker pull base/archlinux                         # 從 Docker Hub 下載 image
rhel:~ # docker pull ubuntu:last                            # 下載 image 並指定 tag

rhel:~ # docker rmi hello-world                             # 刪除 image
rhel:~ # docker rmi -f hello-world                          # 強制刪除 image
```

`method 1`

已有的 image 上 create image

```
rhel:~ # docker commit -m -a <container_id> <image_name> [tag]
```

`method 2`

匯入 LXC template, 可到 [OpenVZ 下載](https://openvz.org/Download/template/precreated)

```
rhel:~ # docker import http://download.openvz.org/template/precreated/suse-13.1-x86_64-minimal.tar.gz <image_name[:tag]>

rhel:~ # wget http://download.openvz.org/template/precreated/suse-13.1-x86_64-minimal.tar.gz
rhel:~ # cat suse-13.1-x86_64-minimal.tar.gz | docker import - <image_name[:tag]>
```

`method 3`

從 dockerfile 產生

```
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

```
rhel:~ # docker save <image_name[:tag]> > <image>.tar
rhel:~ # docker load <image_name[:tag]> < <image>.tar

rhel:~ # docker export <container_id> > image.tar
rhel:~ # docker import image.tar <image_name>
```

## Docker Volume ##

`container`

```
rhel:~ # docker run -it --name webser -v /opt/webapp centos /bin/bash # -v: 建立 /opt/webapp
rhel:~ # docker exec webser ls /opt
```

`host - container`

- folder

將 host 的目錄直接給 container 使用

```
rhel:~ # docker run -it --name webser -v /tmp/webapp:/opt/webapp centos /bin/bash
rhel:~ # touch /tmp/webapp/tmp_file
rhel:~ # docker exec webser ls /opt/webapp
rhel:~ # docker inspect --format '{{.Mounts}}' webser # 顯示 volume
```

預設在 /var/lib/docker/volumes, 刪掉 container 時, volume 還會不會自動刪除, 要手動清除

- file

將 host 的檔案直接給 container 使用

```
rhel:~ # docker run -it -v /tmp/lxc_1.history:/root/.history centos /bin/bash
rhel:~ # docker run -it -v /tmp/config:/etc/app/config:ro centos /bin/bash # 使用 read only 模式
```

多個目錄或檔案時, 可同時使用多個 -v folder|file 方式

`container - container`

```
rhel:~ # docker run -it --name web_master -v /opt/webapp centos /bin/bash
rhel:~ # docker run -it --name web_slave --volumes-from web_master -v /opt/webapp ubuntu /bin/bash
```

## Dokcer Network ##

docker 在設定 port forwarding 時使用 iptables, 但 RHEL 7 預設的防火牆 firewalld 可能會有問題, 目前建議換成 iptables 或是關掉 firewalld. 在 docker run -P 的使用上, 會隨機將 container 上的 EXPOSE port 對應到 host 上的 49000 ~ 49900 port

`port`

```
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

## Docker Hub / Registry

![docker hub](https://smlsunxie.gitbooks.io/docker-book/content/basic/images/docker-hub.png)

```
rhel:~ # docker login # 登入 Docker Hub, 設定在 $HOME/.dockercfg
rhel:~ # docker logout

rhel:~ # docker tag
rhel:~ # docker push
rhel:~ # docker pull
```

## Docker File

Docker File 用來在已建立/存在 image 上, 在建立新的 image

```
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

## Run GUI Apps on Docker


### UNIX X11 Socket

```
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


# Dokcer Machine

因為 Linux 本身就支援 LXC, 所以 Dokcer 有支援. 而 Windows 和 Mac OS X 並沒支援, 要使用 Docker 需要透過 VM. 在此會先安裝 VirtualBox, 然後安裝 Linux VM (這步驟在安裝後第一次啟動會自動執行). 之後的 Container 皆是透過該 Linux VM 啟動.


## Command

Linux VM 的設定, 可以透過 docker-machine 操作

```
osx:~ $ docker-machine help
osx:~ $ docker-machine ls

osx:~ $ docker-machine start <docker_machine>
osx:~ $ docker-machine stop <docker_machine>
osx:~ $ docker-machine status <docker_machine>

osx:~ $ docker-machine ip <docker_machine>
osx:~ $ docker-machine ssh <docker_machine>
osx:~ $ docker-machine inspect <docker_machine>

osx:~ $ docker-machine kill <docker_machine>
osx:~ $ docker-machine rm <docker_machine>
```

----


# Docker Compose


## Install

```
rhel:~ # curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
rhel:~ # chmod +x /usr/local/bin/docker-compose
```

## Compose file

```
rhel:~ # cat docker-compose.yml
```


# Ref

[docker](https://docs.docker.com/)

[Docker —— 從入門到實踐­](https://www.gitbook.com/book/philipzheng/docker_practice/details)

[docker-book](https://www.gitbook.com/book/smlsunxie/docker-book)

[Using GUI's with Docker](http://wiki.ros.org/docker/Tutorials/GUI)

[Running GUI apps with Docker](http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/)