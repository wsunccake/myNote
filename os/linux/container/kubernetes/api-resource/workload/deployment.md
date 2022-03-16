# [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## command

```bash
master:~ $ kubectl get delpoy [-o wide | yaml | json] [-l <selector>]
master:~ $ kubectl create [-f <deploy>.yaml | deploy <deploy>]
master:~ $ kubectl delete [-f <deploy>.yaml | deploy <deploy>]
master:~ $ kubectl apply -f <deploy>.yaml
master:~ $ kubectl describe deploy <deploy>
master:~ $ kubectl wait --for=condition=Ready --timeout=60s deploy <deploy>
master:~ $ kubectl edit deploy <deploy>
master:~ $ kubectl patch deploy <deploy> -p '{"key": "value"}'

master:~ $ kubectl expose deploy <deploy> [--external-ip=<mater_ip>|<node_ip>] [--port=<external_port>] [--target-port=<container_port>]
master:~ $ kubectl scale [-f <deploy>.yaml | deploy <deploy>] --replica=<n>
master:~ $ kubectl set image deploy <deploy> <container>=<img>:<tag>
master:~ $ kubectl rollout undo|status|history deploy <deploy>
```


---

## demo

```bash
master:~ $ kubectl create deploy nginx --image=nginx:1.20-alpine
master:~ $ kubectl get all
master:~ $ kubectl get pod,rs,deploy

master:~ $ kubectl port-forward nginx-5b7c575f67-dd7tc 8080:80 &
master:~ $ curl http://localhost:8080
master:~ $ curl http://localhost:8080/version

# scale out
master:~ $ kubectl scale deploy nginx --replicas=2

# expose service
master:~ $ kubectl expose deploy nginx --type=LoadBalancer --port=8080
master:~ $ curl http://<external ip>:8080
master:~ $ curl http://<external ip>:8080/version

# rolling upgrade
master:~ $ kubectl get pod nginx-5b7c575f67-dd7tc -o jsonpath='{.spec.containers[0].image}'
master:~ $ kubectl set image deploy nginx nginx=nginx:1.21-alpine
master:~ $ kubectl rollout history deployment nginx
master:~ $ kubectl rollout status deployment nginx
master:~ $ kubectl rollout undo deployment nginx
```

```
    deployment
    <name>
      |
      v
    replica set
    <name>-xxxx
      |
      v
    pod
    <name>-xxxx-yyyy
```


---

## yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      containers:
      - name: hello
        image: gcr.io/google-samples/node-hello:1.0
        ports:
        - containerPort: 5000
        imagePullPolicy: Never
```
