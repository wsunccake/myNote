# container app

## jenkins

```bash
# pull image
[linux:~ ] # docker pull jenkins/jenkins:lts

# run container
[linux:~ ] # export JENKINS_HOME=<path>
[linux:~ ] # docker run -d \
  -v $JENKINS_HOME:/var/jenkins_home \
  -v 8080:8080 \
  -p 50000:50000 \
  [-u <uid>[:<gid>]] \
  --name jenkins \
  [--restart always] \
  jenkins/jenkins:lts
# -d = -detach, -v = --volume, -p = --publish, -u = --user

# install plugin
[linux:~ ] # docker exec -it jenkins sh -c "echo greenballs:latest | /usr/local/bin/install-plugins.sh"

[linux:~ ] # cat plugins.txt
greenballs:latest
[linux:~ ] # docker cp plugins.txt jenkins:/tmp/.
[linux:~ ] # docker exec -it jenkins sh -c "/usr/local/bin/install-plugins.sh < /tmp/plugis.txt"
```


---

## prometheus + node_export + grafana


### prometheus

```bash
# pull image
[linux:~ ] # docker pull prom/prometheus

# setup config
[linux:~ ] # export PROMETHEUS_CONF=<path>
[linux:~ ] # mkdir -p $PROMETHEUS_CONF
[linux:~ ] # vi $PROMETHEUS_HOME/prometheus.yml
global:
  scrape_interval:     15s
  evaluation_interval: 15s
alerting:
  alertmanagers:
  - static_configs:
    - targets:
rule_files:
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
    - targets: ['<prometheus ip>:9090']
  - job_name: 'node_exporter'
    static_configs:
    - targets: ['<node_export ip>:9100']

# run container
[linux:~ ] # export PROMETHEUS_DATA=<path>
[linux:~ ] # mkdir -p $PROMETHEUS_DATA
[linux:~ ] # docker run -d \
    -p 9090:9090 \
    -v $PROMETHEUS_CONF:/etc/prometheus \
    -v $PROMETHEUS_DATA:/prometheus \
    --name prometheus \
    -u <uid>:<gid> \
    prom/prometheus
```


### node_exporter

```bash
# pull image
[linux:~ ] # docker pull prom/node-exporter

# run container
[linux:~ ] # docker run -d \
  -p 9100:9100 \
  --name node-exporter \
  prom/node-exporter
```


### grafana

```bash
# pull image
[linux:~ ] # docker pull grafana/grafana

# run container
[linux:~ ] # export GRAFANA_DATA=<path>
[linux:~ ] # mkdir -p $GRAFANA_DATA
[linux:~ ] # docker run -d \
  -p 3000:3000 \
  -v $GRAFANA:/var/lib/grafana \
  --name=grafana \
  grafana/grafana
```

default account and password: admin/admin


---
