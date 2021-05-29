# container yaml

## basic

### docker

```bash
# for python - flask
[ubuntu:~ ] $ vi app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

# for docker
[ubuntu:~ ] $ vi Dockerfile
FROM python:alpine

RUN pip install flask
WORKDIR /app
ADD app.py /app

EXPOSE 5000/tcp

CMD ["python", "app.py"]

[ubuntu:~ ] $ docker build -t local/webapp .
[ubuntu:~ ] $ docker run -td --name flaskapp -p 5000:5000 local/webapp
[ubuntu:~ ] $ curl localhost:5000
```


### docker-compose

```bash
[ubuntu:~ ] $ vi docker-compose.yaml
version: '2.1'

services:
  webservice:
    build: .
    image: local/webapp
    container_name: flaskapp
    restart: always
    ports:
      - "5000:5000"

[ubuntu:~ ] $ docker-compose up -d
[ubuntu:~ ] $ curl localhost:5000
```


### kubectl - pod

```bash
[ubuntu:~ ] $ vi pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-pod
  labels:
    app: hello-world
spec:
  containers:
  - name: flaskapp
    image: local/webapp
    ports:
    - containerPort: 5000
    imagePullPolicy: Never

[ubuntu:~ ] $ kubectl apply -f pod.yaml
[ubuntu:~ ] $ kubectl exec -it hello-pod -- sh
```


### kubectl - depoly

```bash
[ubuntu:~ ] $ vi deploy.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-app
  template:
    metadata:
      labels:
        app: hello-app
    spec:
      containers:
      - name: flaskapp
        image: local/webapp
        ports:
        - containerPort: 5000
        imagePullPolicy: Never

[ubuntu:~ ] $ kubectl apply -f deploy.yaml
[ubuntu:~ ] $ kubectl exec -it deploy/hello-deploy -- sh
```


### kubectl - service

```bash
[ubuntu:~ ] $ vi service.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-app
  template:
    metadata:
      labels:
        app: hello-app
    spec:
      containers:
      - name: flaskapp
        image: local/webapp
        ports:
        - containerPort: 5000
        imagePullPolicy: Never
---
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  selector:
    app: hello-app
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 9376

[ubuntu:~ ] $ kubectl apply -f sevice.yaml
[ubuntu:~ ] $ kubectl exec -it svc/hello-service -- sh
```
