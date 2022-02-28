# locust 2.x

## install

```bash
linux:~ # pip install locustio==2.8.2
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

## ref

[Locust](https://locust.io/)

[Locust Documentation](http://docs.locust.io/en/stable/index.html)

[locustio/locust](https://github.com/locustio/locust)
