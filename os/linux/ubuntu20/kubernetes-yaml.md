# kubernetes yaml

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
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
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
EOF

[ubuntu:~ ] $ kubectl exec -it hello-pod -- sh
```


### kubectl - depoly

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
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
EOF

[ubuntu:~ ] $ kubectl exec -it deploy/hello-deploy -- sh
```


### kubectl - service

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
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
EOF

[ubuntu:~ ] $ kubectl exec -it svc/hello-service -- sh
```


---

## kube-dns / coredns

only service and pod record on dns, service isn't ping

service fqdn: <service>.<namespace>.svc.cluster.local

pod fqdn: <pod ip>.<namespace>.pod.cluster.local


```bash
# create service and deploy
[ubuntu:~ ] $ kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4
[ubuntu:~ ] $ kubectl expose deployment hello-node --type=LoadBalancer --port=8080
[ubuntu:~ ] $ minikube service hello-node   # only for minikube

# hpa
[ubuntu:~ ] $ kubectl autoscale deployment hello-node --cpu-percent=50 --min=1 --max=10
[ubuntu:~ ] $ kubectl get hpa

# kube dns server
[ubuntu:~ ] $ kubectl get svc kube-dns -n kube-system

# kube dns utils
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: dnsutils
  namespace: default
spec:
  containers:
  - name: dnsutils
    image: gcr.io/kubernetes-e2e-test-images/dnsutils:1.3
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
EOF

[ubuntu:~ ] $ kubectl exec -it dnsutils -- nslookup hello-node.default.svc.cluster.local
[ubuntu:~ ] $ kubectl exec -it dnsutils -- nslookup 172-17-0-10.default.pod.cluster.local
```


---

## kube-proxy

```bash
[ubuntu:~ ] $ kubectl get ds -n kube-system
[ubuntu:~ ] $ kubectl get ds kube-proxy -n kube-system -o json | jq '.spec.template.spec.volumes[].configMap.name'  # get cm kube-proxy

[ubuntu:~ ] $ kubectl -n kube-system get cm kube-proxy -o json | jq '.data."config.conf"' | sed 's/\\n/\n/g' | grep mode
[ubuntu:~ ] $ kubectl -n kube-system get cm kube-proxy -o yaml | grep mode
```


---

## kube config

```bash
[ubuntu:~ ] $ cat /etc/kubernetes/admin.conf
[ubuntu:~ ] $ cat $HOME/.kube/config
[ubuntu:~ ] $ export KUBECONFIG=<kube_config>

kubectl config view --minify
kubectl config get-contexts
kubectl config set-context <context>
```
