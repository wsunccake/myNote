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
master:~ $ kubectl rollout undo|status|history deployment <deploy>
```


---

## demo

```bash
master:~ $ kubectl create deployment hello-world --image=gcr.io/google-samples/node-hello:1.0
master:~ $ kubectl expose deployment hello-world --type=LoadBalancer --port=8080
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
