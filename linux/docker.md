# Docker #


## Docker Install ##

	rhel:~ # cat /etc/yum.repo.d/docker.repo
	[virt7-docker-common-testing]
	name=virt7-docker-common-testing
	baseurl=http://cbs.centos.org/repos/virt7-docker-common-testing/x86_64/os/ 
	enabled=1
	gpgcheck=0

	rhel:~ # systemctl start docker.service # 啟動服務
	rhel:~ # systemctl enable docker.service # 常駐服務
	rhel:~ # docker run hello-world # 測試

	rhel:~ # usermod -aG docker user # 將使用者加入 docker 群組


## Docker Run ##

	rhel:~ # docker info
	rhel:~ # docker run -it ubuntu /bin/bash # 啟用 ubuntu image 的 container, i: inter active mode, t: terminal
	rhel:~ # docker run -it --name my_ubuntu ubuntu /bin/bash # 指令 container name
	rhel:~ # docker run -itdP ubuntu /bin/bash # d: background mode, P: 開放 container port forwading (當 image 有先定義 EXPOSE 才會有效)

	rhel:~ # docker exec <container_id> /bin/sh # 在 host 端送 command 到 container 端執行

	rhel:~ # nsenter --target <container_id_pid>  --mount --uts --ipc --net --pid /bin/sh

	rhel:~ # dock ps # 顯示執行中的 container
	rhel:~ # dock ps -l # 顯示最後一個 container
	rhel:~ # dock ps -a # 顯示所有的 container (包括未執行的)

	rhel:~ # docker rm <container_id> # 刪除 container

	rhel:~ # docker start <container_id> # 啟動 container
	rhel:~ # docker stop <container_id> # 停止 container
	rhel:~ # docker restart <container_id> # 重啟 container
	rhel:~ # docker kill <container_id> # 強制停止 container

	rhel:~ # docker attch <container_id> # 進入 container, deattch 使用 ctrl^p ctrl^q
	rhel:~ # docker exec -it <container_id> /bin/exec # 進入 container

	rhel:~ # docker top <container_id>
	rhel:~ # docker logs -ft <container_id>
	rhel:~ # docker stats <container_id>
	rhel:~ # docker inspect <container_id>


## Docker Image ##

	rhel:~ # docker search archlinux # 搜尋 Docker Hub 上的 image

	rhel:~ # docker images # 顯示本機上的 images

	rhel:~ # docker pull base/archlinux # 從 Docker Hub 下載 image
	rhel:~ # docker pull ubuntu:last # 下載 image 並指定 tag

	rhel:~ # docker rmi hello-world # 刪除 image
	rhel:~ # docker rmi -f hello-world # 強制刪除 image


`method 1`

已有的 image 上 create image

	rhel:~ # docker commit -m -a <container_id> <image_name> [tag]


`method 2`

匯入 LXC template, 可到 [OpenVZ 下載](https://openvz.org/Download/template/precreated)

	rhel:~ # docker import http://download.openvz.org/template/precreated/suse-13.1-x86_64-minimal.tar.gz <image_name[:tag]>

	rhel:~ # wget http://download.openvz.org/template/precreated/suse-13.1-x86_64-minimal.tar.gz
	rhel:~ # cat suse-13.1-x86_64-minimal.tar.gz | docker import - <image_name[:tag]>


`method 3`

從 dockerfile 產生

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

`import / export, save / load`

	rhel:~ # docker save <image_name[:tag]> > <image>.tar
	rhel:~ # docker load <image_name[:tag]> < <image>.tar

	rhel:~ # docker export <container_id> > image.tar
	rhel:~ # docker import image.tar <image_name>


## Docker Volume ##

`container`

	rhel:~ # docker run -it --name webser -v /opt/webapp centos /bin/bash # -v: 建立 /opt/webapp
	rhel:~ # docker exec webser ls /opt

`host - container`

- folder

將 host 的目錄直接給 container 使用

	rhel:~ # docker run -it --name webser -v /tmp/webapp:/opt/webapp centos /bin/bash
	rhel:~ # touch /tmp/webapp/tmp_file
	rhel:~ # docker exec webser ls /opt/webapp
	rhel:~ # docker inspect --format '{{.Mounts}}' webser # 顯示 volume

預設在 /var/lib/docker/volumes, 刪掉 container 時, volume 還會不會自動刪除, 要手動清除

- file

將 host 的檔案直接給 container 使用

	rhel:~ # docker run -it -v /tmp/lxc_1.history:/root/.history centos /bin/bash
	rhel:~ # docker run -it -v /tmp/config:/etc/app/config:ro centos /bin/bash # 使用 read only 模式

多個目錄或檔案時, 可同時使用多個 -v folder|file 方式

`container - container`

	rhel:~ # docker run -it --name web_master -v /opt/webapp centos /bin/bash
	rhel:~ # docker run -it --name web_slave --volumes-from web_master -v /opt/webapp ubuntu /bin/bash


## Dokcer Network ##

docker 在設定 port forwarding 時使用 iptables, 但 RHEL 7 預設的防火牆 firewalld 可能會有問題, 目前建議換成 iptables 或是關掉 firewalld. 在 docker run -P 的使用上, 會隨機將 container 上的 EXPOSE port 對應到 host 上的 49000 ~ 49900 port

`port`

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

`ip`

`link`

同一台 host 之間的 container 可透過 link 方式互相

	rhel:~ # docker run -d --name db training/postgres
	rhel:~ # docker run -d -P --name web --link db:db training/webapp python app.py
	rhel:~ # docker inspect -f "{{ .HostConfig.Links }}" web


## Docker Hub / Registry ##

	rhel:~ # docker login # 登入 Docker Hub, 設定在 $HOME/.dockercfg
	rhel:~ # docker logout

	rhel:~ # docker tag
	rhel:~ # docker push
	rhel:~ # docker pull