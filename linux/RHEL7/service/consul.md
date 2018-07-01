## Install

```bash
linux:~ # curl -L https://releases.hashicorp.com/consul/1.1.0/consul_1.1.0_linux_amd64.zip > consul_1.1.0_linux_amd64.zip
linux:~ # unzip consul_1.1.0_linux_amd64.zip
linux:~ # mv consul /usr/local/sbin/
```


---

## Server

```bash
server:~ # mkdir -p /data/consul

# start service
server:~ # consul agent -server -bootstrap -ui -advertise=<server_ip> -client=0.0.0.0 -data-dir /data/consul

# check cluster
server:~ # consul members
server:~ # consul operator raft list-peers

# check port
server:~ # ss -nlutp | grep consul
# udp: 8301, 8302, 8600
# tcp: 8301, 8302, 8600, 8500, 8300
```

dns: 8600

http: 8500

server: 8300

serf_lan: 8301

serf_wan: 8302

`config file`

```bash
server:~ # mkdir /etc/consul.d

# config
server:~ # vi /etc/consul.d/consul.json
{
  "data_dir": "/data/consul",
  "datacenter": "dc1",
  "log_level": "INFO",
  "server": true,
  "bootstrap_expect": 1,
  "bind_addr": "<server_ip>",
  "client_addr": "0.0.0.0",
  "ui": true
}

# 如需要變動 port, 在 josn 加入以下設定
"ports": {
  "dns": 53,
  "http": 80,
  "server": 8300,
  "serf_lan": 8301,
  "serf_wan": 8302
}

# start service for daemon
server:~ # nohup consul agent -server -config-dir /etc/consul.d >& consul.log
```

---

## Client

```bash
client:~ # mkdir -p /data/consul

# start server
client:~ # consul agent -bind=<client_ip> -join=<server_ip> -data-dir /data/consul

# check port
server:~ # ss -nlutp | grep consul
# udp: 8301, 8600
# tcp: 8301, 8600, 8500
```

`config`

```bash
client:~ # mkdir /etc/consul.d

# config
client:~ # vi /etc/consul.d/consul.json
{
  "data_dir": "/data/consul",
  "enable_script_checks": true,
  "bind_addr": "<client_ip>",
  "retry_join": ["<server_ip>"],
  "retry_interval": "30s",
  "rejoin_after_leave": true,
  "start_join": ["<server_ip>"]
}

# start service for daemon
client:~ # nohup consul agent -config-dir /etc/consul.d >& consul.log

# check dns
client:~ # dig @<server_ip> -p 8600 <client_name>.node.dc1.consul
```

---

## Test

```bash
# HTTP API
linux:~ # curl <server_ip>:8500/v1/catalog/nodes | jq
linux:~ # curl <server_ip>:8500/v1/catalog/services?pretty

# DNS
linux:~ # dig @<server_ip> -p 8600 <server_name>
linux:~ # dig @<server_ip> -p 8600 <node>.node.<dc>.consul  # for node
linux:~ # dig @<server_ip> -p 8600 <service>.service.consul # for service

# WEB UI
linux:~ # curl http://<server_ip>:8500/ui
```


---

## Service

`register service`

```bash
# config file
linux:~ # vi /etc/consul.d/service.json 
{
  "services": [
    {
      "name": "web",
      "id": "web1",
      "tags": [
        "master"
      ],
      "address": "<service_ip>",
      "port": <service_port>,
      "check": {
        "args": [
          "nc",
          "-zv",
          "127.0.0.1",
          "80"
        ],
        "interval": "10s"
      }
    }
}

# check 可省略
# name 可相同, 但 id 必須唯一

# by daemon
linux:~ # consul reload

# by api


# health check
curl http://<server_ip>:8500/v1/health/service/web
curl http://<server_ip>:8500/v1/health/service/web?passing
curl http://<server_ip>:8500/v1/health/service/web?failing
```


---

## API

`agent`

HTTP Method   | URL                     | Description
---           | ---                     | ---
GET           | /agent/members          | list member
GET           | /agent/self             | read config
PUT           | /agent/reload           | reload agent
PUT           | /agent/maintenance      | enable maintenance
GET           | /agent/monitor          | stream log
PUT           | /agent/join/<address>   | join
PUT           | /agent/leave            | shutdown
PUT           | /agent/force-leave      | force shutdown

`catalog`

HTTP Method   | URL                         | Description
---           | ---                         | ---
GET           | /catalog/datacenters        | list datacenter
GET           | /catalog/nodes              | list node
GET           | /catalog/nodes/<node>       | list service for node
GET           | /catalog/services           | list service
GET           | /catalog/service/<service>  | list node for service
PUT           | /catalog/register           | register entity
PUT           | /catalog/deregister         | deregister entity

```bash
# register node
linux:~ # curl -X PUT -d '{"node": "<node>", "address": "<node_ip>"}' <server_ip>:8500/v1/catalog/register

# deregister node
linux:~ # curl -X PUT -d '{"datacent": "<dc>", "node": "<node>"}' <server_ip>:8500/v1/catalog/deregister
```

`service`

HTTP Method   | URL                                   | Description
---           | ---                                   | ---
GET           | /agent/services                       | list service
PUT           | /agent/service/register               | register service
PUT           | /agent/service/deregister/<service>   | deregister service
PUT           | /agent/service/maintenance/<service>  | enable maintenance


```bash
# config file
linux:~ # vi /etc/consul.d/service.json 
{
  "name": "web",
  "id": "web2",
  "tags": [
    "slave"
  ],
  "address": "<service_ip>",
  "port": <service_port>,
  "check": {
    "args": [
      "nc",
      "-zv",
      "127.0.0.1",
      "80"
    ],
    "interval": "10s"
  }
}

# register service
linux:~ # curl -X PUT -d @/etc/consul.d/service.json <server_ip>:8500/v1/agent/service/register

# deregister service
linux:~ # curl -X PUT <server_ip>:8500/v1/agent/service/deregister/my_service
```


---

## Command

```bash
linux:~ # consul agent
linux:~ # consul reload
linux:~ # consul members
linux:~ # consul info
linux:~ # consul leave
linux:~ # consul force-leave
```


---

## Reference

[Install Consul](https://www.consul.io/docs/install/index.html)

[Consul 與 Registrator](https://blog.mallux.me/2017/03/19/consul/)

[基於 Consul 的數據庫高可用架構](https://hk.saowen.com/a/2144d9d1c9b06ca6ab8deb3bc21d4be919708324a44f7cff160949403376a68f)
