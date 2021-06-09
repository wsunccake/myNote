＃ elk

install order

1. Elasticsearch

2. Kibana

3. Logstash

4. Beats

5. APM Server

6. Elasticsearch Hadoop


---

## elasticsearch

indexes data

limitation:

1. mem max 50%, leatest 2GB

2. under 32GB

port: 9200

```bash
# repo
[centos:~ ] # dnf install java-11-openjdk
[centos:~ ] # rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
[centos:~ ] # cat << EOF > /etc/yum.repos.d/elasticsearch.repo
[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

# install
[centos:~ ] # dnf makecache
[centos:~ ] # dnf install elasticsearch

# service
[centos:~ ] # systemctl enable elasticsearch
[centos:~ ] # systemctl start elasticsearch
[centos:~ ] # systemctl status elasticsearch

# firewall
[centos:~ ] # firewall-cmd --permanent --add-port=9200/tcp
[centos:~ ] # firewall-cmd --reload

# config
[centos:~ ] # tree -L 1 /etc/elasticsearch
/etc/elasticsearch
|-- elasticsearch.keystore
|-- elasticsearch.yml
|-- jvm.options
|-- jvm.options.d
|-- log4j2.properties
|-- role_mapping.yml
|-- roles.yml
|-- users
`-- users_roles

[centos:~ ] # vi /etc/elasticsearch/jvm.options
...
-Xms1g   # min mem
-Xmx1g   # max mem

[centos:~ ] # grep -Ev '^$|^#' /etc/elasticsearch/elasticsearch.yml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

[centos:~ ] # systemctl restart elasticsearch

# test
[centos:~ ] # curl "localhost:9200/?pretty"
[centos:~ ] # curl -L http://localhost:9200/_cat/nodes
[centos:~ ] # curl -L http://localhost:9200/_cat/indices
```


---

## kibana

visualizes data

port: 5601

```bash

# install
[centos:~ ] # dnf install kibana

# service
[centos:~ ] # systemctl enable kibana
[centos:~ ] # systemctl start kibana
[centos:~ ] # systemctl status kibana

# firewall
[centos:~ ] # firewall-cmd --permanent --add-port=5601/tcp
[centos:~ ] # firewall-cmd --reload

# config
[centos:~ ] # tree -L 1 /etc/kibana
/etc/kibana
|-- kibana.keystore
|-- kibana.yml
`-- node.options

[centos:~ ] # cat << EOF > /etc/kibana/kibana.yml
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
EOF

[centos:~ ] # systemctl restart kibana

# test
[centos:~ ] # curl -L http://localhost:5601
```


---

## logstash

collects data

```bash
# install
[centos:~ ] # dnf install logstash

# service
[centos:~ ] # systemctl enable logstash
[centos:~ ] # systemctl start logstash
[centos:~ ] # systemctl status logstash

# firewall
[centos:~ ] # firewall-cmd --permanent --add-port=5044/tcp
[centos:~ ] # firewall-cmd --reload

# config
[centos:~ ] # tree -L 1 /etc/logstash
/etc/logstash/
|-- conf.d
|-- jvm.options
|-- log4j2.properties
|-- logstash-sample.conf
|-- logstash.yml
|-- pipelines.yml
`-- startup.options

[centos:~ ] # grep -Ev '^#|^$' /etc/logstash/pipelines.yml
- pipeline.id: main
  path.config: "/etc/logstash/conf.d/*.conf"

[centos:~ ] # cat << EOF > /etc/logstash/beat.conf 
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
    hosts => ["localhost:9200"]
    index => "%{[@metadata][beat]}-%{+YYYY.MM.dd}"
  }
}
EOF

[centos:~ ] # systemctl restart logstash
```


---

## filebeat

```bash
# install
[centos:~ ] # dnf install filebeat

# setup
[centos:~ ] # filebeat modules enable system     # enable module
[centos:~ ] # filebeat setup                     # create index
[centos:~ ] # filebeat setup --template -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["localhost:9200"]'
[centos:~ ] # filebeat setup -e -E output.logstash.enabled=false -E output.elasticsearch.hosts=['localhost:9200'] -E setup.kibana.host=localhost:5601

# usage
[centos:~ ] # filebeat --help
[centos:~ ] # filebeat modules --help
[centos:~ ] # filebeat modules list

# config
[centos:~ ] # tree -L 1 /etc/filebeat 
/etc/filebeat
|-- fields.yml
|-- filebeat.reference.yml
|-- filebeat.yml
`-- modules.d

[centos:~ ] # grep -Ev '^#|^$|\s#' /etc/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: false
  paths:
    - /var/log/*.log
- type: filestream
  enabled: false
  paths:
    - /var/log/*.log
filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false
setup.template.settings:
  index.number_of_shards: 1
setup.kibana:
output.elasticsearch:
  hosts: ["localhost:9200"]
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~

[centos:~ ] # vi /etc/filebeat/filebeat.yml
...
#output.elasticsearch:
#  hosts: ["localhost:9200"]

output.logstash:
  hosts: ["localhost:5044"]

# service
[centos:~ ] # systemctl enable filebeat
[centos:~ ] # systemctl start filebeat
[centos:~ ] # systemctl status filebeat
```


---

## apm-server

```bash
# install
[centos:~ ] # dnf install apm-server

# service
[centos:~ ] # systemctl enable apm-server
[centos:~ ] # systemctl start apm-server
[centos:~ ] # systemctl status apm-server
```
