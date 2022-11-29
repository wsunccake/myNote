# harbor 2.x

## install

download from https://github.com/goharbor/harbor/releases

```bash
# for online
harbor:~ # curl -LO https://github.com/goharbor/harbor/releases/download/v2.3.1/harbor-online-installer-v2.3.1.tgz
harbor:~ # tar zxf harbor-online-installer-v2.3.1.tgz -C /opt
harbor:~ # cd /opt/harbor

# for offline
harbor:~ # curl -LO https://github.com/goharbor/harbor/releases/download/v2.6.2/harbor-offline-installer-v2.6.2.tgz
harbor:~ # tar zxf harbor-offline-installer-v2.6.2.tgz -C /opt
harbor:~ # cd /opt/harbor

harbor:/opt/harbor # cp harbor.yml.tmpl harbor.yml
harbor:/opt/harbor # vi harbor.yml
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

harbor:/opt/harbor # ./prepare
harbor:/opt/harbor # ./install.sh

# web ui password
harbor:/opt/harbor # grep harbor_admin_password harbor.yml
```

web ui -> http://<ip>

default: admin/Harbor12345

default image folder: /data


---

## manage

```bash
harbor:/opt/harbor # docker-compose -f docker-compose.yml ps
harbor:/opt/harbor # docker-compose -f docker-compose.yml start
harbor:/opt/harbor # docker-compose -f docker-compose.yml stop
harbor:/opt/harbor # docker-compose -f docker-compose.yml rm
harbor:/opt/harbor # docker-compose -f docker-compose.yml up -dv
```

Projects \ New Project

format: <harbor_ip or harbor_hostname>[:<harbor_port>]/<project>/<REPOSITORY>[:TAG]


---

## usage

```bash
# add privte registry
client:~ # vi  /etc/docker/daemon.json
{
  "insecure-registries": [ "<harbor_ip or harbor_hostname>:<harbor_port>" ]
}
client:~ # systemctl restart docker.service

client:~ # docker login <harbor_ip or harbor_hostname>:<harbor_port>    # $HOME/.docker/config.json
client:~ # docker logout
```

```bash
# push image
client:~ # docker pull <image>
client:~ # docker images <image>
client:~ # docker tag <image> <harbor_ip or harbor_hostname>:<harbor_port>/<project>/<image>
client:~ # docker push <harbor_ip or harbor_hostname>:<harbor_port>/<project>/<image>

# ie
client:~ # docker tag alpine 192.168.0.1:80/test/apline
client:~ # docker login -u admin -p Harbor12345 192.168.0.1:80
client:~ # docker push 192.168.0.1:80/test/apline
client:~ # docker logout
```

```bash
# pull image
client:~ # docker pull <harbor_ip or harbor_hostname>:<harbor_port>/<project>/<image>

# ie
client:~ # docker login -u admin -p Harbor12345 192.168.0.1:80
client:~ # docker pull 192.168.0.1:80/test/apline
client:~ # docker logout
```


---

## example

```
harbor             ---   client
192.168.10.10            192.168.10.x
```

```bash
harbor:~ # echo "192.168.10.10  harbor" >> /etc/hosts

harbor:~ # curl -LO https://github.com/goharbor/harbor/releases/download/v2.6.2/harbor-offline-installer-v2.6.2.tgz
harbor:~ # tar zxf harbor-offline-installer-v2.6.2.tgz -C /opt
harbor:~ # cd /opt/harbor

harbor:/opt/harbor # cp harbor.yml.tmpl harbor.yml
harbor:/opt/harbor # vi harbor.yml
# setup host
hostname: harbor
http:
  port: 5000
...

# disable https
 https:
   port: 443
   certificate: /your/certificate/path
   private_key: /your/private/key/path
->
# https:
#   port: 443
#   certificate: /your/certificate/path
#   private_key: /your/private/key/path

harbor:/opt/harbor # ./prepare
harbor:/opt/harbor # ./install.sh
```

```bash
client:~ # echo "192.168.10.10  harbor" >> /etc/hosts

client:~ # vi /etc/docker/daemon.json 
{
  "insecure-registries": ["192.168.10.10:5000", "harbor:5000", "0.0.0.0"]
}
client:~ # systemctl restart docker 
client:~ # systemctl status docker

client:~ # docker login --username admin --password Harbor12345 http://harbor:5000
```

---

## ref

Harbor 2.6 Documentation](https://goharbor.io/docs/2.6.0/)
