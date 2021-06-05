# prometheus

## install

`method 1`

```bash
centos:~ # cat > /etc/yum.repos.d/prometheus.repo << EOF
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

centos:~ # dnf -y install prometheus2 node_exporter

# service
centos:~ # systemctl enable --now prometheus node_exporter

# firewall
centos:~ # firewall-cmd --add-service=prometheus --permanent
centos:~ # firewall-cmd --reload

# test
centos:~ # curl http://localhost:9090
```


`method 2`

```bash
centos:~ # docker run -d \
    -p 9090:9090 \
    -v /home/prometheus:/etc/prometheus \
    --name prometheus \
    prom/prometheus

centos:~ # docker run -d \
    --net="host" \
    -p 9100:9100 \
    --name node-exporter \
    prom/node-exporter

```


---

## config

```bash
centos:~ # vi /etc/prometheus/prometheus.yml   # use docker, vi /home/prometheus/prometheus.yml
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

  # add  : grab stats about the local machine by [node-exporter]
  - job_name: node
    static_configs:
    - targets: ['localhost:9100']
```
