# container app

## jenkins

```bash
# pull image
[linux:~ ] # docker pull jenkins/jenkins:lts

# run container
[linux:~ ] # export JENKINS_HOME=<path>
[linux:~ ] # mkdir -p JENKINS_HOME
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

## elk stack

https://www.docker.elastic.co/

```bash
# when all elk container in one machine, use docker-network
[linux:~ ] # docker network create elk
```


### elasticsearch

```bash
# pull image
[linux:~ ] # docker pull docker.elastic.co/elasticsearch/elasticsearch:7.13.1

# run container
[linux:~ ] # export ELASTICSEARCH_DATA=<path>
[linux:~ ] # mkdir -p $ELASTICSEARCH_DATA
[linux:~ ] # docker run -d \
  --name elasticsearch \
  --net elk \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -v $ELASTICSEARCH_DATA:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:7.13.1
```


### kibana

```bash
# pull image
[linux:~ ] # docker pull docker.elastic.co/kibana/kibana:7.13.1

# run container
[linux:~ ] # docker run -d \
  --name kibana \
  --net elk \
  -p 5601:5601 \
  -e "ELASTICSEARCH_HOSTS=http://<es ip>:9200" \
  docker.elastic.co/kibana/kibana:7.13.1
```

```
Environment Variable      Kibana Setting
----------------------------------------------
ELASTICSEARCH_HOSTS       elasticsearch.hosts
SERVER_NAME               server.name
SERVER_BASEPATH           server.basePath
MONITORING_ENABLED        monitoring.enabled
```


---

### logstash

```bash
# pull image
[linux:~ ] # docker pull docker.elastic.co/logstash/logstash:7.13.1

# setup config
[linux:~ ] # export LOGSTASH_PIPELINE=<path>
[linux:~ ] # mkdir -p $LOGSTASH_PIPELINE
[linux:~ ] # cat << EOF > $LOGSTASH_PIPELINE/beat.conf 
input {
  beats {
    port => 5044
  }
}

filter {
  if [type] == "syslog" {
     grok {
        match => { "message" => "%{SYSLOGLINE}" }
  }
     date {
        match => [ "timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
     }
  }
}

output {
  elasticsearch {
    hosts => ["<es ip>:9200"]
    index => "%{[@metadata][beat]}-%{+YYYY.MM.dd}"
  }
}
EOF

# run container
[linux:~ ] # docker run -d \
  --name logstash \
  --net elk \
  -p 5044:5044 \
  -v $LOGSTASH_PIPELINE:/usr/share/logstash/pipeline \
  docker.elastic.co/logstash/logstash:7.13.1
```

```
Environment Variable      Logstash Setting
----------------------------------------------
PIPELINE_WORKERS          pipeline.workers
LOG_LEVEL                 log.level
MONITORING_ENABLED        monitoring.enabled
```


---

## filebeat

```bash
# pull image
[linux:~ ] # docker pull docker.elastic.co/beats/filebeat:7.13.1

# setup config
[linux:~ ] # export FILEBEAT_HOME=<path>
[linux:~ ] # mkdir -p $FILEBEAT_HOME
[linux:~ ] # curl -L -O https://raw.githubusercontent.com/elastic/beats/7.13/deploy/docker/filebeat.docker.yml && mv filebeat.docker.yml $FILEBEAT_HOME/.
[linux:~ ] # cat << 'EOF' > $FILEBEAT_HOME/filebeat.docker.yml
filebeat.config:
  modules:
    path: ${path.config}/modules.d/*.yml
    reload.enabled: false

filebeat.autodiscover:
  providers:
    - type: docker
      hints.enabled: true

processors:
- add_cloud_metadata: ~

output.elasticsearch:
  hosts: '${ELASTICSEARCH_HOSTS:elasticsearch:9200}'
  username: '${ELASTICSEARCH_USERNAME:}'
  password: '${ELASTICSEARCH_PASSWORD:}'
EOF

# create index
[linux:~ ] # docker run --rm \
  docker.elastic.co/beats/filebeat:7.13.1 \
  setup -E setup.kibana.host="<kibana ip>:5601" \
  -E output.elasticsearch.hosts=["<es ip>:9200"]

# run container
[linux:~ ] # docker run -d \
  --name filebeat \
  --net elk \
  -u root \
  -v "$FILEBEAT_HOME/filebeat.docker.yml:/usr/share/filebeat/filebeat.yml:ro" \
  -v "/var/lib/docker/containers:/var/lib/docker/containers:ro" \
  -v "/var/run/docker.sock:/var/run/docker.sock:ro" \
  docker.elastic.co/beats/filebeat:7.13.1 \
  filebeat -e -strict.perms=false \
  -E output.elasticsearch.hosts=["<es ip>:9200"]
```
