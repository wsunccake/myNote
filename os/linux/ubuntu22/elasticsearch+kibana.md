# elasticSearch + kibana

---

## content

- [prepare](#prepare)
- [elasticsearch](#elasticsearch)
- [kibana](#kibana)
- [url](#url)

---

## prepare

```bash
# prepare
ubuntu:~ # apt update
ubuntu:~ # apt install default-jdk

# import gpg key
ubuntu:~ # apt-get install apt-transport-https
ubuntu:~ # wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# add repo
ubuntu:~ # echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list

# update repo db
ubuntu:~ # apt update
```

---

## elasticsearch

```bash
# install
ubuntu:~ # apt install elasticsearch

# firewall
ubuntu:~ # ufw allow 9200

# service
ubuntu:~ # systemctl daemon-reload
ubuntu:~ # systemctl enable elasticsearch
ubuntu:~ # systemctl start elasticsearch
ubuntu:~ # systemctl status elasticsearch
ubuntu:~ # systemctl stop elasticsearch

# test
ubuntu:~ $ curl -X GET "localhost:9200/"

# config dir
ubuntu:~ # ls -l /etc/elasticsearch
```

---

## kibana

```bash
# install
ubuntu:~ # apt install kibana

# firewall
ubuntu:~ # ufw allow 5601

# service
ubuntu:~ # systemctl daemon-reload
ubuntu:~ # systemctl enable kibana
ubuntu:~ # systemctl start kibana
ubuntu:~ # systemctl status kibana
ubuntu:~ # systemctl stop kibana

# test
ubuntu:~ # curl http://localhost:5601/

# config dir
ubuntu:~ # ls /etc/kibana

# config file
ubuntu:~ # vi /etc/kibana/kibana.yml
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
```

---

## url

```text
http://localhost:5601/app/management
http://localhost:5601/app/discover
http://localhost:5601/app/home#/tutorial_directory/fileDataViz
```
