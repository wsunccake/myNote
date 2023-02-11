# efk stask - elasticsaerch fluent-bit kinbana

## topology

```
                fluentd     elasticsearch       kibana          alpine
                |           |                   |               |
                |           |                   |               |
                +-----------+-------------------+---------------+
daemonset       x
statefulset                 x
deployment                                      x               x
service         x           x                   x
pod             x           x                   x               x
serviceaccount  x                               x
configmap       x                               x
```

---

## elasticsearch

```bash
# create namespce
master:~ $ kubectl create namespace logging

# add helm repo
master:~ $ helm repo add bitnami https://charts.bitnami.com/bitnami

# no pv and replica
master:~ $ cat << EOF > values.yaml
master:
  replicas: 1
  persistence:
    enabled: false
data:
  persistence:
    enabled: false
EOF
master:~ $ helm -n logging install -f values.yaml elasticsearch bitnami/elasticsearch
```

---

## kibana

```bash
# create namespace
master:~ $ kubectl create namespace logging

# add helm repo
master:~ $ helm repo add bitnami https://charts.bitnami.com/bitnami

# create app
master:~ $ helm -n logging install kibana bitnami/kibana
master:~ $ helm -n logging upgrade --set elasticsearch.hosts[0]=elasticsearch-master,elasticsearch.port=9200,persistence.enabled=false,service.type=LoadBalancer kibana bitnami/kibana
```

---

## fluent-bit

```bash
# add helm repo
master:~ $ helm repo add fluent https://fluent.github.io/helm-charts

# create app
master:~ $ helm -n logging install fluent-bit fluent/fluent-bit
```

---

## alpine

```bash
master:~ $ kubectl -n logging create deployment alpine --image=alpine
master:~ $ kubectl -n logging patch deploy alpine -p '{"spec": {"spec": {"containers": {"stdin": true, "tty": true}}}}'
master:~ $ kubectl -n logging get deploy alpine
master:~ $ kubectl -n logging exec -it <alpine pod> -- sh

# test elasticsearch
alpine:~ # curl http://<elasticsearch svc>:9200/
alpine:~ # curl http://<elasticsearch svc>:9200/_cluster
alpine:~ # curl http://<elasticsearch svc>:9200/_cat/health
# test kibana
alpine:~ # curl http://<kibana svc>:5601/app/managemnet
alpine:~ # curl http://<kibana svc>:5601/app/dicover
# test fluent-bit
alpine:~ # curl http://<fluent-bit svc>:2020

master:~ $ kubectl run alpine --image=alpine --command -- /bin/sh -c 'i=0; while true; do echo "$i: Hello"; i=$((i+1)); sleep 1; done'
master:~ $ kubectl logs alpine
```

---

## setup

### kibana

step 1. setup kibana index patterns

http://<kibana svc>:5601/app/management/kibana/indexPatterns

step 2. search by discover page

setup http://<kibana svc>:5601/app/discover

---

## problem

```
elasticsearch
ERROR - failed to store async-search
Data too large, data for [<reused_arrays>] would be [...], which is larger than the limit of [...], real usage: [...], new bytes reserved: [...], usages [...]


curl -XPOST 'http://<elasticsearch svc>:9200/fdns/_cache/clear?fielddata=true'
curl -XPUT http://<elasticsearch>:9200/_cluster/settings -H 'Content-Type: application/json' -d '{"persistent" : {"indices.breaker.fielddata.limit" : "40%"} }'
```

```
fluent bit
[2022/03/10 17:52:50] [ warn] [engine] failed to flush chunk '1-1646934524.644358141.flb', retry in 20 seconds: task_id=310, input=tail.0 > output=es.0 (out_id=0)
```

---

## ref

[Fluent Bit v1.8 Documentation](https://docs.fluentbit.io/manual/installation/kubernetes)
