# prometheus

## all server

prometheus + node_export + grafana


---

## prometheus

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


---

## node_exporter

```bash
# pull image
[linux:~ ] # docker pull prom/node-exporter

# run container
[linux:~ ] # docker run -d \
  -p 9100:9100 \
  --name node-exporter \
  prom/node-exporter
```


---

## grafana

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
