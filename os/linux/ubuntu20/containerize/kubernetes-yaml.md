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

[ubuntu:~ ] $ kubectl exec -it hello-pod  [-c <container>] -- sh
[ubuntu:~ ] $ kubectl logs -f hello-pod
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
#  type: LoadBalancer
  type: ClusterIP
EOF

[ubuntu:~ ] $ kubectl exec -it svc/hello-service -- sh
```


---

## kube-dns / coredns

only service and pod record on dns, service isn't ping

service fqdn: <service>.<namespace>.svc.cluster.local

pod fqdn: <pod ip>.<namespace>.pod.cluster.local

example:

<pod ip>: 192.168.30.11 -> 192-168-30-11


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

[ubuntu:~ ] $ kubectl config view --minify
[ubuntu:~ ] $ kubectl config get-contexts
[ubuntu:~ ] $ kubectl config set-context <context> [--namespace <namespace>]

# ie
[ubuntu:~ ] $ kubectl config get-contexts
[ubuntu:~ ] $ kubectl config set-context kubernetes-admin@cluster.local
[ubuntu:~ ] $ kubectl config set-context kubernetes-admin@cluster.local --namespace demo
[ubuntu:~ ] $ kubectl config set-context kubernetes-admin@cluster.local --namespace ""

```


---

## env var

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: dapi-envars-fieldref
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "sh", "-c"]
      args:
      - while true; do
          echo -en '\n';
          printenv MY_NODE_NAME MY_POD_NAME MY_POD_NAMESPACE;
          printenv MY_POD_IP MY_POD_SERVICE_ACCOUNT;
          printenv MY_CPU_REQUEST MY_CPU_LIMIT;
          printenv MY_MEM_REQUEST MY_MEM_LIMIT;
          sleep 10;
        done;
      resources:
        requests:
          memory: "32Mi"
          cpu: "125m"
        limits:
          memory: "64Mi"
          cpu: "250m"
      env:
        - name: MY_NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: MY_POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: MY_POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: MY_POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: MY_POD_SERVICE_ACCOUNT
          valueFrom:
            fieldRef:
              fieldPath: spec.serviceAccountName
        - name: MY_CPU_REQUEST
          valueFrom:
            resourceFieldRef:
              containerName: test-container
              resource: requests.cpu
        - name: MY_CPU_LIMIT
          valueFrom:
            resourceFieldRef:
              containerName: test-container
              resource: limits.cpu
        - name: MY_MEM_REQUEST
          valueFrom:
            resourceFieldRef:
              containerName: test-container
              resource: requests.memory
        - name: MY_MEM_LIMIT
          valueFrom:
            resourceFieldRef:
              containerName: test-container
              resource: limits.memory
  restartPolicy: Never
EOF

[ubuntu:~ ] $ kubectl get pods
[ubuntu:~ ] $ kubectl logs dapi-envars-fieldref
[ubuntu:~ ] $ kubectl exec -it dapi-envars-fieldref [-c <container>] -- printenv
```


---

## alpine

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alpine
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alpine
  template:
    metadata:
      labels:
        app: alpine
    spec:
      containers:
      - name: alpine
        image: alpine
        stdin: true
        tty: true
EOF

[ubuntu:~ ] $ kubectl exec -it alpine-7cf564f7f5-jh48q [-c <container>] -- sh
```


---

## mount

### hostPath

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alpine
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alpine
  template:
    metadata:
      labels:
        app: alpine
    spec:
      volumes:
      - name: test-volume
        hostPath:
          path: /data
          type: Directory

      containers:
      - name: alpine
        image: alpine
        stdin: true
        tty: true
        workingDir: /test-data
        volumeMounts:
        - mountPath: /test-data
          name: test-volume
EOF

[ubuntu:~ ] $ kubectl exec -it alpine-7cf564f7f5-jh48q [-c <container>] -- ls /test-data
```

### nfs

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alpine
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alpine
  template:
    metadata:
      labels:
        app: alpine
    spec:
      volumes:
      - name: test-volume
        nfs:
          path: /data
          server: 192.168.10.1

      containers:
      - name: alpine
        image: alpine
        stdin: true
        tty: true
        volumeMounts:
        - mountPath: /test-data
          name: test-volume
EOF

[ubuntu:~ ] $ kubectl exec -it alpine-7cf564f7f5-jh48q [-c <container>] -- ls /test-data
```

node must install nfs-common to support nfs


---

## job

```bash
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl"]
        args: ["-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
EOF

[ubuntu:~ ] $ kubectl get jobs.batch
[ubuntu:~ ] $ kubectl get pod
[ubuntu:~ ] $ kubectl logs pi-xg6kh
```
