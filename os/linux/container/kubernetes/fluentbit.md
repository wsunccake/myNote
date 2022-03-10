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
alpine:~ # curl http://elasticsearch-master:9200/
alpine:~ # curl http://elasticsearch-master:9200/_cluster
alpine:~ # curl http://elasticsearch-master:9200/_cat/health
alpine:~ # curl http://elasticsearch-data:9200/
alpine:~ # curl http://elasticsearch-coordinating-only:9200/
# test kibana
alpine:~ # curl http://kibana:5601/app/managemnet
alpine:~ # curl http://kibana:5601/app/dicover
# test fluent-bit
alpine:~ # curl http://fluent-bit:2020
```


---

## ref

[Fluent Bit v1.8 Documentation](https://docs.fluentbit.io/manual/installation/kubernetes)
