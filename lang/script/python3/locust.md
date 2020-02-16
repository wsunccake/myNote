# locust


## install

```bash
linux:~ # pip install locustio
```


---

## usage

```bash
# for gui, http://127.0.0.1:8089
linux:~ # locust -H https://<ip>:<port> -f locustfile.py

# for cli
linux:~ # locust -H https://<ip>:<port> -f locustfile.py --no-web -c10 -r1 -t10s
```


---

## demo

### web server


```python
# app.py
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello Flask'


@app.route('/login', methods=['POST'])
def login():
    return f'Login username: {request.values["username"]}, password: {request.args.get("password")}'


@app.route('/logout', methods=['POST'])
def logout():
    return f'Logout username: {request.form["username"]}, password: {request.form.get("password")}'


@app.route('/profile')
def profile():
    return 'Profile'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

```bash
linux:~ # pip install flask
linux:~ # python app.py
```


### test function

```python
# locustfile.py
import functools

from locust import HttpLocust, TaskSet, between
from locust.log import console_logger


def validate_response_time(timeout=10.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(a):
            response = func(a)
            if response.elapsed.total_seconds() > timeout:
                response.failure(f'response time take over: {timeout} second')
            else:
                response.success()
            return response

        return wrapper

    return decorator


def show_response_time(func):
    @functools.wraps(func)
    def wrapper(a):
        response = func(a)
        console_logger.info(
            f'url: {response.url}, response time: {response.elapsed.total_seconds()}, status: {response.status_code}')
        return response

    return wrapper


def login(l):
    l.client.post("/login", {"username": "ellen_key", "password": "education"})


def logout(l):
    l.client.post("/logout", {"username": "ellen_key", "password": "education"})


def index(l):
    l.client.get("/")


@validate_response_time()
@show_response_time
def profile(l):
    response = l.client.get("/profile", catch_response=True)
    return response


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
```


### class test

```python
# locustfile.py
from locust import HttpLocust, TaskSet, task, between
from locust.log import console_logger
import functools


def validate_response_time(timeout=10.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(a):
            response = func(a)
            if response.elapsed.total_seconds() > timeout:
                response.failure(f'response time take over: {timeout} second')
            else:
                response.success()
            return response

        return wrapper

    return decorator


def show_response_time(func):
    @functools.wraps(func)
    def wrapper(a):
        response = func(a)
        console_logger.info(
            f'url: {response.url}, response time: {response.elapsed.total_seconds()}, status: {response.status_code}')
        return response

    return wrapper


class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()

    def login(self):
        self.client.post("/login", {"username": "ellen_key", "password": "education"})

    def logout(self):
        self.client.post("/logout", {"username": "ellen_key", "password": "education"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    @validate_response_time()
    @show_response_time
    def profile(self):
        response = self.client.get("/profile", catch_response=True)
        return response


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)
```
