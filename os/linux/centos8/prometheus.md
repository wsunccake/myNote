# prometheus

port: 9090


## service

node_export  <--  prometheus  <--  grafana
                      |
                      |
                      + -->  alertmangager


## install

```bash
# repo
[centos:~ ] # cat > /etc/yum.repos.d/prometheus.repo << 'EOF'
[prometheus]
name=prometheus
baseurl=https://packagecloud.io/prometheus-rpm/release/el/$releasever/$basearch
repo_gpgcheck=1
enabled=1
gpgkey=https://packagecloud.io/prometheus-rpm/release/gpgkey
       https://raw.githubusercontent.com/lest/prometheus-rpm/master/RPM-GPG-KEY-prometheus-rpm
gpgcheck=1
metadata_expire=300
EOF

# package
[centos:~ ] # dnf install prometheus2

# service
[centos:~ ] # systemctl enable prometheus
[centos:~ ] # systemctl start prometheus
[centos:~ ] # systemctl status prometheus

# firewall
[centos:~ ] # firewall-cmd --permanent --add-port=9090/tcp
[centos:~ ] # firewall-cmd --reload

# test
[centos:~ ] # curl http://localhost:9090
```


## config

```bash
[centos:~ ] # tree -L 1 /etc/prometheus/
/etc/prometheus/
`-- prometheus.yml

[centos:~ ] # grep -Ev '^#|^$|\s#' /etc/prometheus/prometheus.yml
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
    - targets: ['localhost:9090']

# add local machine by node_exporter
[centos:~ ] # vi /etc/prometheus/prometheus.yml
...
scrape_configs:
  ...
  - job_name: 'node_exporter'
    static_configs:
    - targets: ['localhost:9100']

[centos:~ ] # systemctl restart prometheus
```


---

# node_exporter

port: 9100


## install

```bash
# repo
# same prometheus

# package
[centos:~ ] # dnf install node_exporter

# service
[centos:~ ] # systemctl enable node_exporter
[centos:~ ] # systemctl start node_exporter
[centos:~ ] # systemctl status node_exporter

# test
[centos:~ ] # curl http://localhost:9100/metrics
```


---

# grafana

port: 3000


## install

```bash
# package
[centos:~ ] # wget https://dl.grafana.com/oss/release/grafana-8.0.0-1.x86_64.rpm
[centos:~ ] # dnf install grafana-8.0.0-1.x86_64.rpm

# service
[centos:~ ] # systemctl enable grafana-server
[centos:~ ] # systemctl start grafana-server
[centos:~ ] # systemctl status grafana-server

# firewall
[centos:~ ] # firewall-cmd --permanent --add-port=3000/tcp
[centos:~ ] # firewall-cmd --reload

# test
[centos:~ ] # curl -L http://localhost:3000
```

default account and password: admin/admin

import https://grafana.com/grafana/dashboards/1860 dashboard template


---

## alertmanager

port: 9093, 9094

## install

```bash
[centos:~ ] # dnf install alertmanager

# service
[centos:~ ] # systemctl enable alertmanager
[centos:~ ] # systemctl start alertmanager
[centos:~ ] # systemctl status alertmanager

# firewall
[centos:~ ] # firewall-cmd --permanent --add-port=9093/tcp --add-port=9094/tcp
[centos:~ ] # firewall-cmd --reload
```


## config - alertmanager

```bash
[centos:~ ] # grep -Ev '^#|^$' /etc/prometheus/alertmanager.yml
global:
  resolve_timeout: 5m
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://127.0.0.1:5001/'
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']

[centos:~ ] # mv /etc/prometheus/alertmanager.yml /etc/prometheus/alertmanager.yml.org
[centos:~ ] # vi /etc/prometheus/alertmanager.yml
global:
  smtp_smarthost: 'localhost:25'
  smtp_require_tls: false
  smtp_from: 'Alertmanager <root@dlp.srv.world>'
  # smtp_auth_username: 'alertmanager'
  # smtp_auth_password: 'password'

route:
  receiver: 'email-notice'
  group_by: ['alertname', 'Service', 'Stage', 'Role']
  group_wait:      30s
  group_interval:  5m
  repeat_interval: 4h

receivers:
- name: 'email-notice'
  email_configs:
  - to: "root@localhost"

[centos:~ ] # systemctl restart alertmanager
```


## config - promethues

```bash
[centos:~ ] # vi /etc/prometheus/alert_rules.yml
groups:
- name: Instances
  rules:
  - alert: InstanceDown
    expr: up == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      description: '{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes.'
      summary: 'Instance {{ $labels.instance }} down'

[centos:~ ] # vi /etc/prometheus/prometheus.yml
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # line 12 : change to (Alertmanager Host):(Port)
      - 'localhost:9093'

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"
  - "alert_rules.yml"

[centos:~ ] # systemctl restart prometheus 
```
