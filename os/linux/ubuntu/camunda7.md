# Camunda 7

[Camunda Download Hub](https://camunda.com/download/)

---

## prepare

```bash
ubuntu:~ # apt install openjdk-17-jdk
ubuntu:~ # export JAVA_HOME=$(readlink -f `which java` | sed s@/bin/java@@)
```

---

## Camunda Platform

### install - binary

```bash
ubuntu:~ # wget https://downloads.camunda.cloud/release/camunda-bpm/run/7.21/camunda-bpm-run-7.21.0.tar.gz
ubuntu:~ # mkdir /usr/local/camunda7
ubuntu:~ # tar zxf camunda-bpm-run-7.21.0.tar.gz -C /usr/local/camunda7

ubuntu:~ # /usr/local/camunda7/start.sh --help
```

### install - container

```bash
docker pull camunda/camunda-bpm-platform:run-latest
docker run -d --name camunda -p 8080:8080 camunda/camunda-bpm-platform:run-latest
```

### launch

```bash
# start service
ubuntu:~ # /usr/local/camunda7/start.sh --detached

# shutdown service
ubuntu:~ # /usr/local/camunda7/shutdown.sh
```

Web: http://127.0.0.1:8080
Username: demo
Password: demo

---

## Camunda Modeler

```bash
ubuntu:~ $ wget https://downloads.camunda.cloud/release/camunda-modeler/5.22.0/camunda-modeler-5.22.0-linux-x64.tar.gz
ubuntu:~ $ tar zxf camunda-modeler-5.22.0-linux-x64.tar.gz
```

```
File > New File > BPMN Diagram
```
