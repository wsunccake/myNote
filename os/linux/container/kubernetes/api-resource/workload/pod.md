# [pod](https://kubernetes.io/docs/concepts/workloads/pods/)

## command

```bash
master:~ $ kubectl get pod [-o wide | yaml | json] [-l <selector>]
master:~ $ kubectl create -f <pod>.yaml
master:~ $ kubectl delete [-f <pod>.yaml | pod <pod>]
master:~ $ kubectl apply -f <pod>.yaml
master:~ $ kubectl describe pod <pod>
master:~ $ kubectl wait --for=condition=Ready --timeout=60s pod <pod>
master:~ $ kubectl edit pod <pod>
master:~ $ kubectl patch pod <pod> -p '{"key": "value"}'

master:~ $ kubectl run <pod> --image=<image url> [--port=<port>] [--command=<command>]
master:~ $ kubectl exec -it <pod> [-c <container>] -- <command>
master:~ $ kubectl logs -f <pod>
master:~ $ kubectl port-forward <pod> [<host_port>:]<container_port>
```

---

## demo

```bash
master:~ $ kubectl run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=8080
master:~ $ kubectl port-forward hello-world 8080:8080 &
master:~ $ curl http://localhost:8080

master:~ $ kubectl run alpine --image=alpine --command -- hostname
```

---

## yaml

```bash
# example
master:~ $ cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: hello
  labels:
    app: hello-world
spec:
  containers:
  - name: hello
    image: gcr.io/google-samples/node-hello:1.0
    ports:
    - containerPort: 8080
EOF

master:~ $ kubectl get pod -o yaml
master:~ $ kubectl wait --for=condition=Ready --timeout=60s pod hello

master:~ $ kubectl logs -f hello
master:~ $ kubectl describe pod hello
```
