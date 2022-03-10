# efk stack - elasticsearch fluentd kibana

## topology

```
fluentd     elasticsearch       kibana
daemonset   statefulset         deployment
|           |                   |
|           |                   |
+-----------+------------------ +
```

<worker>: /var/log/pods

/var/log/pods/<namespace>_<pod_name>_<pod_id>/<container_name>/


---

## elasticsearch

```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-data-0
spec:
# storageClassName: <storage_class_name>
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /data
```

spec.capacitystorage: 依據需求調整


```yaml
# values.yaml
replicas: 1
minimumMasterNodes: 1
clusterHealthCheckParams: 'wait_for_status=yellow&timeout=1s'
volumeClaimTemplate:
  resources:
    requests:
      storage: 500Mi

# disalbe pv
#persistence:
#  enabled: false
```

volumeClaimTemplate.resources.requests.storage: 依據需求調整, 一般 production 大概 500 Gb

replicas: single cluster setup 1

minimumMasterNodes: single cluster setup 1


```bash
# create naemspace
[master:~ ] $ kubectl create namespace kube-logging
[master:~ ] $ kubectl -n kube-logging apply -f pv.yaml

# create statefulset
[master:~ ] $ helm repo add elastic https://helm.elastic.co
[master:~ ] $ helm repo list
[master:~ ] $ helm search repo --versions elastic/elasticsearch
[master:~ ] $ helm show values elastic/elasticsearch
[master:~ ] $ helm pull [--version 7.16.3] elastic/elasticsearch
[master:~ ] $ helm -n kube-logging install elasticsearch --version 7.16.3 --values values.yaml elastic/elasticsearch

[master:~ ] $ kubectl -n kube-logging get pod,deploy,sts,svc,pv,pvc
[master:~ ] $ kubectl -n kube-logging get all,pv,pvc

# test
[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://localhost:9200
[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://localhost:9200/_cluster
[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://localhost:9200/_cat/health

[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://<elasticsearch sts>:9200
[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://<elasticsearch sts>:9200/_cluster
[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://<elasticsearch sts>:9200/_cat/health

[master:~ ] $ kubectl -n kube-logging port-forward <elasticsearch pod> 9200:9200
[master:~ ] $ curl http://localhost:9200
[master:~ ] $ curl http://localhost:9200/_cluster
[master:~ ] $ curl http://localhost:9200/_cat/health
```


---

## kibana

```bash
# create naemspace
[master:~ ] $ kubectl create namespace kube-logging

# create deploy
[master:~ ] $ helm repo add elastic https://helm.elastic.co
[master:~ ] $ helm repo list
[master:~ ] $ helm search repo --versions elastic/kibana
[master:~ ] $ helm show values elastic/kibana
[master:~ ] $ helm pull [--version 7.16.3] elastic/kibana
[master:~ ] $ helm -n kube-logging install kibana --version 7.16.3 elastic/kibana

[master:~ ] $ kubectl -n kube-logging get pod,deploy,sts,svc,pv,pvc
[master:~ ] $ kubectl -n kube-logging get all,pv,pvc

# test
[master:~ ] $ kubectl -n kube-logging exec -it <kibana pod> -- curl http://localhost:5601

[master:~ ] $ kubectl -n kube-logging exec -it <kibana pod> -- curl http://<elasticsearch sts>:9200
[master:~ ] $ kubectl -n kube-logging exec -it <kibana pod> -- curl http://<elasticsearch sts>:9200/_cluster
[master:~ ] $ kubectl -n kube-logging exec -it <kibana pod> -- curl http://<elasticsearch sts>:9200/_cat/health
[master:~ ] $ kubectl -n kube-logging exec -it <kibana pod> -- curl http://<kibana deploy>:5601

[master:~ ] $ kubectl -n kube-logging port-forward <kibana pod> 5601:5601
[master:~ ] $ curl http://localhost:5601
```


---

## metricbeat

```bash
# create naemspace
[master:~ ] $ kubectl create namespace kube-logging

# create deploy, ds
[master:~ ] $ helm repo add elastic https://helm.elastic.co
[master:~ ] $ helm repo list
[master:~ ] $ helm search repo --versions elastic/metricbeat
[master:~ ] $ helm show values elastic/metricbeat
[master:~ ] $ helm pull [--version 7.16.3] elastic/metricbeat
[master:~ ] $ helm -n kube-logging install metricbeat --version 7.16.3 elastic/metricbeat

[master:~ ] $ kubectl -n kube-logging get pod,deploy,sts,svc,pv,pvc
[master:~ ] $ kubectl -n kube-logging get all,pv,pvc

# test
[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://localhost:9200_cat/indices

[master:~ ] $ kubectl -n kube-logging exec -it <elasticsearch pod> -c elasticsearch -- curl http://<elasticsearch sts>:9200/_cat/indices

[master:~ ] $ kubectl -n kube-logging port-forward <elasticsearch pod> 9200:9200
[master:~ ] $ curl http://localhost:9200/_cat/indices
```


---

## fluentd

```bash
[master:~ ] $ helm repo add fluent https://fluent.github.io/helm-charts
[master:~ ] $ helm repo list
[master:~ ] $ helm search repo --versions fluent/fluentd
[master:~ ] $ helm show values fluent/fluentd
[master:~ ] $ helm pull [--version 0.3.5] fluent/fluentd
[master:~ ] $ helm -n kube-logging install fluentd --version 0.3.5 fluent/fluentd

[master:~ ] $ kubectl -n kube-logging get pod,deploy,sts,svc,pv,pvc
[master:~ ] $ kubectl -n kube-logging get all,pv,pvc
```


---

## ref

[Install Elasticsearch on Kubernetes Using Helm Chart](https://phoenixnap.com/kb/elasticsearch-helm-chart)

[How to Setup EFK Stack on Kubernetes: Step by Step Guides](https://devopscube.com/setup-efk-stack-on-kubernetes/)
