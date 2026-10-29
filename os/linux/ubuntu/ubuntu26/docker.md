# docker

```bash
# 1. 更新套件清單並安裝基礎憑證工具
ubuntu:~ # apt update
ubuntu:~ # apt install ca-certificates curl -y
ubuntu:~ # install -m 0755 -d /etc/apt/keyrings

# 2. 下載並匯入 Docker 官方的 GPG 金鑰
ubuntu:~ # curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
ubuntu:~ # chmod a+r /etc/apt/keyrings/docker.asc

# 3. 將 Docker 套件庫加入 Apt 來源清單
ubuntu:~ # echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. 更新套件庫索引，並直接安裝 Docker 核心組件與常用的 Docker Compose
ubuntu:~ # apt update
ubuntu:~ # apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# 將帳號加入 docker 使用者群組
ubuntu:~ # usermod -aG docker <username>
```

---


```bash
docker pull [<REPOSITORY>[:<TAG>]]
docker image ls [<REPOSITORY>[:<TAG>]]
docker image rm <REPOSITORY>[:<TAG>]


```

```bash
docker pull alpine
docker pull alpine:3.24

docker image ls
docker image ls -aq

docker image $(docker image ls -aq)
docker image $(docker image ls rms --format "{{.Repository}}:{{.Tag}}")
```
