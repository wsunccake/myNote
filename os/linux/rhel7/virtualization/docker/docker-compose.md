# Docker Compose


## Install

```bash
# Download From Github
rhel:~ # curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
rhel:~ # chmod +x /usr/local/bin/docker-compose

# Install From EPEL
rhel:~ # yum install docker-compose
```


---

## Compose file

```bash
rhel:~ # cat docker-compose.yml
version: '3'
services:
  hello:
    image: hello-world
    container_name: hello

rhel:~ # docker-compose up
```

```bash
rhel:~/hello # cat app.py 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

rhel:~/hello # cat requirements.txt 
Flask==1.0.2

rhel:~/hello # cat Dockerfile 
FROM python:alpine

EXPOSE 8080

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /usr/src/app/app.py

CMD [ "python", "app.py" ]

rhel:~/hello # cat docker-compose.yml
version: '3'
services:
  hello:
    container_name: hello
    build: .
    image: hello
    ports:
    - "8080:8080"

rhel:~/hello # docker-compose -f docker-compose.yml up -d
```

