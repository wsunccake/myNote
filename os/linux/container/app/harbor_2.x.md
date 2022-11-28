# harbor 2.x

## install

download from https://github.com/goharbor/harbor/releases

```bash
# for online
[linux:~ ] # curl -LO https://github.com/goharbor/harbor/releases/download/v2.3.1/harbor-online-installer-v2.3.1.tgz
[linux:~ ] # tar zxf harbor-online-installer-v2.3.1.tgz -C /opt
[linux:~ ] # cd /opt/harbor

# for offline
[linux:~ ] # curl -LO https://github.com/goharbor/harbor/releases/download/v2.6.2/harbor-offline-installer-v2.6.2.tgz
[linux:~ ] # tar zxf harbor-offline-installer-v2.6.2.tgz -C /opt
[linux:~ ] # cd /opt/harbor

[linux:/opt/harbor ] # cp harbor.yml.tmpl harbor.yml
[linux:/opt/harbor ] # vi harbor.yml
# setup host
 hostname: reg.mydomain.com
->
 hostname: <harbor_ip or harbor_hostname>

...

# disable https
 https:
   # https port for harbor, default is 443
   port: 443
   # The path of cert and key files for nginx
   certificate: /your/certificate/path
   private_key: /your/private/key/path
->
# https:
#   # https port for harbor, default is 443
#   port: 443
#   # The path of cert and key files for nginx
#   certificate: /your/certificate/path
#   private_key: /your/private/key/path

[linux:/opt/harbor ] # ./prepare
[linux:/opt/harbor ] # ./install.sh

# web ui password
[linux:/opt/harbor ] # grep harbor_admin_password harbor.yml
```

web ui -> http://<ip>

default: admin/Harbor12345

default image folder: /data


---

## manage

```bash
[linux:/opt/harbor ] # docker-compose -f docker-compose.yml ps
[linux:/opt/harbor ] # docker-compose -f docker-compose.yml start
[linux:/opt/harbor ] # docker-compose -f docker-compose.yml stop
[linux:/opt/harbor ] # docker-compose -f docker-compose.yml rm
[linux:/opt/harbor ] # docker-compose -f docker-compose.yml up -dv
```

Projects \ New Project

format: <harbor_ip or harbor_hostname>[:<harbor_port>]/<project>/<REPOSITORY>[:TAG]


---

## usage

```bash
# add privte registry
[linux:~ ] # vi  /etc/docker/daemon.json
{
  "insecure-registries": [ "<harbor_ip or harbor_hostname>:<harbor_port>" ]
}
[linux:~ ] # systemctl restart docker.service

[linux:~ ] # docker login <harbor_ip or harbor_hostname>:<harbor_port>    # $HOME/.docker/config.json
[linux:~ ] # docker logout
```

```bash
# push image
[linux:~ ] # docker pull <image>
[linux:~ ] # docker images <image>
[linux:~ ] # docker tag <image> <harbor_ip or harbor_hostname>:<harbor_port>/<project>/<image>
[linux:~ ] # docker push <harbor_ip or harbor_hostname>:<harbor_port>/<project>/<image>

# ie
[linux:~ ] # docker tag alpine 192.168.0.1:80/test/apline
[linux:~ ] # docker login -u admin -p Harbor12345 192.168.0.1:80
[linux:~ ] # docker push 192.168.0.1:80/test/apline
[linux:~ ] # docker logout
```

```bash
# pull image
[linux:~ ] # docker pull <harbor_ip or harbor_hostname>:<harbor_port>/<project>/<image>

# ie
[linux:~ ] # docker login -u admin -p Harbor12345 192.168.0.1:80
[linux:~ ] # docker pull 192.168.0.1:80/test/apline
[linux:~ ] # docker logout
```


---
