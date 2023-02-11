# drone

## network

```
git server  ---   drone server   ---  drone runner/agent
                                 \
                                  +-  drone runner/agent
                                        ...
```

---

## git server

### oauth application

create DRONE_GIT_CLIENT_ID and DRONE_GIT_CLIENT_SECRET

```
# github
Settings / Developer settings / OAuth Apps

# gitlab
Settings / Applications
```

### shared secret

create DRONE_RPC_SECRET

```bash
[linux:~ ] # openssl rand -hex 16
```

---

## drone server

```bash
[linux:~ ] # docker pull drone/drone:2

# for github
[linux:~ ] # docker run \
  --volume={{DRON_DATA}}:/data \
  --env=DRONE_GITHUB_CLIENT_ID={{DRONE_GITHUB_CLIENT_ID}} \
  --env=DRONE_GITHUB_CLIENT_SECRET={{DRONE_GITHUB_CLIENT_SECRET}} \
  --env=DRONE_RPC_SECRET={{DRONE_RPC_SECRET}} \
  --env=DRONE_SERVER_HOST={{DRONE_SERVER_HOST}} \
  --env=DRONE_SERVER_PROTO={{DRONE_SERVER_PROTO}} \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:2

# for gitlab
[linux:~ ] # docker run \
  --volume={{DRON_DATA}}:/data \
  --env=DRONE_GITLAB_SERVER=https://gitlab.com \
  --env=DRONE_GITLAB_CLIENT_ID={{DRONE_GITLAB_CLIENT_ID}} \
  --env=DRONE_GITLAB_CLIENT_SECRET={{DRONE_GITLAB_CLIENT_SECRET}} \
  --env=DRONE_RPC_SECRET={{DRONE_RPC_SECRET}} \
  --env=DRONE_SERVER_HOST={{DRONE_SERVER_HOST}} \
  --env=DRONE_SERVER_PROTO={{DRONE_SERVER_PROTO}} \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:2

# check
[linux:~ ] # docker logs -f drone

# ie
[linux:~ ] # docker run \
  -v /drone_data:/data \
  -e DRONE_GITHUB_CLIENT_ID=123456789 \
  -e DRONE_GITHUB_CLIENT_SECRET=123456789abcdef \
  -e DRONE_RPC_SECRET=xyz \
  -e DRONE_SERVER_HOST=192.168.1.10 \
  -e DRONE_SERVER_PROTO=http \
  -p 80:80 \
  -p 443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:2

# test
[linux:~ ] # curl http://localhost
```

DRONE_SERVER_HOST: dron server ip or hostname

DRONE_SERVER_PROTO: http or https

---

## drone runner

```bash
# docker runner
[linux:~ ] # docker pull drone/drone-runner-docker:1
[linux:~ ] # docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DRONE_RPC_PROTO={{DRONE_SERVER_PROTO}} \
  -e DRONE_RPC_HOST={{DRON_SERVER_HOST}} \
  -e DRONE_RPC_SECRET={{DRONE_RPC_SECRET}} \
  -e DRONE_RUNNER_CAPACITY=2 \
  -e DRONE_RUNNER_NAME=${HOSTNAME} \
  -p 3000:3000 \
  --restart always \
  --name runner \
  drone/drone-runner-docker:1

# check
[linux:~ ] # docker logs -f runner

# ie
[linux:~ ] # docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DRONE_RPC_PROTO=http \
  -e DRONE_RPC_HOST=192.168.1.10 \
  -e DRONE_RPC_SECRET=xyz \
  -e DRONE_RUNNER_CAPACITY=2 \
  -e DRONE_RUNNER_NAME=${HOSTNAME} \
  -p 3000:3000 \
  --restart always \
  --name runner \
  drone/drone-runner-docker:1
```

---

## pipeline

```bash
[linux:~ ] # mkdir demo
[linux:~ ] # cd demo
[linux:~/demo ] # git init
[linux:~/demo ] # cat << EOF > .drone.yml
kind: pipeline
type: docker
name: default

steps:
- name: greeting
  image: alpine
  commands:
  - echo hello
  - echo world
EOF
[linux:~/demo ] # git add .drone.yml
[linux:~/demo ] # git commit -m "drone demo"
[linux:~/demo ] # git push
```

### multiple step

```yaml
kind: pipeline
type: docker
name: greeting

steps:
  - name: en
    image: alpine
    commands:
      - echo hello world

  - name: fr
    image: alpine
    commands:
      - echo bonjour monde
    when:
      branch:
        - develop
```

### multiple pipeline

```yaml
kind: pipeline
type: docker
name: en

steps:
  - name: greeting
    image: alpine
    commands:
      - echo hello world

trigger:
  event:
    - push

---
kind: pipeline
type: docker
name: fr

steps:
  - name: greeting
    image: alpine
    commands:
      - echo bonjour monde

trigger:
  event:
    - pull_request

---
kind: pipeline
type: docker
name: build

steps:
  - name: test
    image: gcr.io/library/golang
    commands:
      - go build
      - go test -v
```

### parallel

```yaml
kind: pipeline
type: docker
name: default

steps:
  - name: en
    image: alpine
    commands:
      - date
      - echo hello world
      - sleep 10
      - date

  - name: fr
    image: alpine
    commands:
      - date
      - echo bonjour monde
      - sleep 5
      - date

  - name: hi
    image: alpine
    commands:
      - date
    depends_on:
      - en
      - fr
```

---

## cli

get info from http://localhost/account

```bash
# install
[linux:~] # curl -L https://github.com/drone/drone-cli/releases/latest/download/drone_linux_amd64.tar.gz | tar zx
[linux:~] # install -t /usr/local/bin drone

# setup
[linux:~] # export DRONE_SERVER=http://<drone_host>
[linux:~] # export DRONE_TOKEN=<drone_token>
[linux:~] # drone info

# repo
[linux:~] # drone repo ls
[linux:~] # drone repo info <repo>
[linux:~] # drone repo enable <repo>
[linux:~] # drone repo disable <repo>
[linux:~] # drone repo update <repo> --config=.drone.yml

# build
[linux:~] # drone build ls <repo>
[linux:~] # drone build info <repo> [<build>]
[linux:~] # drone build create <repo>
[linux:~] # drone build stop <repo> [<build>]
[linux:~] # drone log view <repo> <build> <stage> <step>
[linux:~/demo] # drone exec
```

---

## ref

[docs](https://docs.drone.io/)
