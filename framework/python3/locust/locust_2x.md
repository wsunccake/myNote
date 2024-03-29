# locust 2.x

## install

```bash
linux:~ # pip install locustio==2.8.2
```


```bash
# sysctl
linux:~ # cat /proc/sys/fs/file-max
lixnu:~ # vi /etc/sysctl.cong
fs.file-max=500000
...

lixnu:~ # sysctl -w fs.file-max=500000

# hard limit
linux:~ # ulimit -Hn
* hard nofile 4096

# soft limit
linux:~ # ulimit -Sn
* soft nofile 1024
```


---

## usage

```bash
# for gui, http://127.0.0.1:8089
linux:~ # locust -H https://<ip>:<port> -f locustfile.py

# for cli
linux:~ # locust -H https://<ip>:<port> -f locustfile.py --headless -u<n> -r<m> -t<time>
linux:~ # locust -H https://<ip>:<port> -f locustfile.py --autostart -u<n> -r<m> -t<time>
# -u: NUM_USERS
# -r: SPAWN_RATE
# -t: RUN_TIME

# other
linux:~ # locust -H https://<ip>:<port> -f locustfile.py --headless -u<n> -r<m> -t<time> \
  --html <html file> \
  --loglevel DEBUG \
  --logfile <log file>
```


---

## HttpUser

```python
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_item(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")

    def on_start(self):
        self.client.post("/login", json={"username": "foo", "password": "bar"})
```


---

## TaskSet

```python
from locust import HttpUser, TaskSet, task, between

def index(l):
    l.client.get("/")

def stats(l):
    l.client.get("/stats/requests")

class UserTasks(TaskSet):
    tasks = [index, stats]

    @task
    def page404(self):
        self.client.get("/does_not_exist")

class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8089"
    wait_time = between(2, 5)
    tasks = [UserTasks]
```


---

## master - slave

```
           + --- slave1
           |
master --- + --- slave2
           |
           + --- slave3
           ...
```

```bash
master:~ $ locust -f locustfile.py \
  -H https://<ip>:<port> \
  -u<n> -r<m> -t<time> \
  --autostart --autoquit 0 \
  --headless \
  --master \
  --master-bind-port <master port>
```

```bash
slave:~ $ locust -f locustfile.py \
  --headless \
  --worker \
  --master-host <master host> --master-port <master port>
```

method 1

先將所有 slave 執行 locust command, 在 master 執行 locust command


method 2

先在 master 執行 locust command (最好加上 --expect-workers 或 --expect-workers-max-wait), 要不然只有要一台 slave 執行 locust command, 就開始跑 test


---

## ref

[Locust](https://locust.io/)

[Locust Documentation](http://docs.locust.io/en/stable/index.html)

[locustio/locust](https://github.com/locustio/locust)
