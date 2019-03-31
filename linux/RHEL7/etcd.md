# etcd

# server

## binary

```bash
server:~ # wget https://github.com/etcd-io/etcd/releases/download/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz
server:~ # tar zxf etcd-v3.3.12-linux-amd64.tar.gz
server:~ # export PATH=$PATH:$HOME/etcd-v3.3.12-linux-amd64
server:~ # export NODE1=192.168.0.1

# start up with argument
server:~ # ./etcd \
  --data-dir=/etcd-data --name node1 \
  --advertise-client-urls http://${NODE1}:2379 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster node1=http://0.0.0.0:2380

# start up with config file
server:~ # etcd --config-file etcd.conf
```


## docker

```bash
server:~ # export NODE1=10.206.86.128
server:~ # export DATA_DIR=/data/etcd

server:~ # docker run -d \
  -p 2379:2379 \
  -p 2380:2380 \
  --volume=${DATA_DIR}:/etcd-data \
  --name etcd quay.io/coreos/etcd:latest \
  /usr/local/bin/etcd \
  --data-dir=/etcd-data --name node1 \
  --advertise-client-urls http://${NODE1}:2379 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster node1=http://0.0.0.0:2380
```


---

# command

## v2

```bash
server:~ # docker exec -it etcd /usr/local/bin/etcdctl [--endpoints=http://${NODE1}:2379] member list

server:~ # etcdctl member list
server:~ # etcdctl cluster-health
server:~ # etcdctl ls

# set key/value
server:~ # etcdctl set <key> <value>
server:~ # etcdctl set /foo bar

# get key/value
server:~ # etcdctl get <key>
server:~ # etcdctl get /foo

# rm key/value
server:~ # etcdctl rm <key-data>
server:~ # etcdctl rmdir <key-folder>
```

## v3

```bash
server:~ # ETCDCTL_API=3 etcdctl member list

# or
server:~ # export ETCDCTL_API=3 
server:~ # etcdctl member list

server:~ # etcdctl endpoint status
server:~ # etcdctl endpoint health

# put key/value
server:~ # etcdctl put <key> <value> --keepalive-time=2s
server:~ # etcdctl put foo bar

# get key/value
server:~ # etcdctl put <key>
server:~ # etcdctl get /
server:~ # etcdctl get "" --prefix=true
server:~ # etcdctl get "" --from-key
server:~ # etcdctl get "" --prefix --keys-only
```


---

# api


## v2

```bash
server:~ # curl -L http://127.0.0.1:2379/version

# put key/value
server:~ # curl -XPUT http://127.0.0.1:2379/v2/keys/<key> -XPUT -d value="<value>"
server:~ # curl -XPUT http://127.0.0.1:2379/v2/keys/foo -XPUT -d value="bar"
server:~ # curl -XPUT http://127.0.0.1:2379/v2/keys/node/n1 -XPUT -d value="{'ip': '192.168.1.1', 'port': 1234}" -d ttl=5

# get key/value
server:~ # curl http://127.0.0.1:2379/v2/keys/<key>
server:~ # curl http://127.0.0.1:2379/v2/keys/foo

# del key/value
server:~ # curl -XDELETE http://127.0.0.1:2379/v2/keys/<key>
server:~ # curl -XDELETE http://127.0.0.1:2379/v2/keys/foo
```


---

# python

```bash
server:~ # pip install python-etcd

server:~ # cat ex.py
import etcd

client = etcd.Client(host='192.168.0.1', port=2379)

# set key/value
client.write('/nodes/n1', 1)
client.write('/service/api', {'ip': '192.168.0.100', 'port': 1234}, ttl=60)

# get key/value
print(client.read('', recursive=True, sorted=True))
print(client.read('/nodes/n1'))
try:
    print(client.read('/service/resource-api'))
except etcd.EtcdKeyNotFound:
    # do something
    print("error")

# del key/value
client.delete('/nodes/n1')
```
