# kubernetes 1.17


## prepare

### selinux

```bash
centos:~ # sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
centos:~ # reboot
```


### hosts

```bash
centos:~ # vi /etc/hosts
192.168.31.200	master
192.168.31.201	node1
192.168.31.202	node2
192.168.31.203	node3
...
```


### ntp / chronyc

```bash
centos:~ # chronyc -a makestep
centos:~ # chronyc -a 'burst 4/4'
```


### firewall

```bash
centos:~ # firewall-cmd --permanent --add-port=6443/tcp
centos:~ # firewall-cmd --permanent --add-port=2379-2380/tcp
centos:~ # firewall-cmd --permanent --add-port=10250/tcp
centos:~ # firewall-cmd --permanent --add-port=10251/tcp
centos:~ # firewall-cmd --permanent --add-port=10252/tcp
centos:~ # firewall-cmd --permanent --add-port=10255/tcp
centos:~ # firewall-cmd --reload
```


### docker

```bash
centos:~ # dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
centos:~ # dnf install docker-ce --nobest
centos:~ # systemctl enable --now docker

# forwarding
centos:~ # vi /lib/systemd/system/docker.service
[Service]
...
ExecStartPost=/sbin/iptables -I FORWARD -s 0.0.0.0/0 -j ACCEPT

centos:~ # systemctl daemon-reload
centos:~ # systemctl restart docker
```


### kubernetes

```bash
centos:~ # cat << EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

centos:~ # dnf install iproute-tc ipvsadm
centos:~ # dnf install kubelet kubeadm kubectl --disableexcludes=kubernetes
centos:~ # systemctl enable --now kubelet

# sysctl
centos:~ # cat << EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
vm.swappiness = 0
EOF

centos:~ # sysctl --system

# disable swap
centos:~ # swapoff -a
centos:~ # vi /etc/fstab
# remove swap
```


---

## config

### master

master 必須做過 prepare 步驟

```bash
# init kube
master:~ # kubeadm config images pull
master:~ # kubeadm init --pod-network-cidr 10.244.0.0/16
master:~ # mkdir -p $HOME/.kube
master:~ # cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
master:~ # chown $(id -u):$(id -g) $HOME/.kube/config

# other
## auto completion
master:~ # dnf install bash-completion
master:~ # echo "source <(kubectl completion bash)" >> ~/.bashrc

## token id
master:~ # kubeadm token list


## ca hash
master:~ # openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

master:~ # kubectl -n kube-system get cm kubeadm-config -o yaml
master:~ # kubectl config view
```


### network

[Installing Addons](https://kubernetes.io/docs/concepts/cluster-administration/addons/)

`flannel`

```bash
master:~ # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
## config: /etc/cni/net.d/10-flannel.conflist,  /run/flannel/subnet.env
## container: kube-flannel
## nic: flannel

master:~ # wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
master:~ # 
kind: ConfigMap
apiVersion: v1
...
  net-conf.json: |
    { 
      "Network": "10.244.0.0/16",  # 可成自訂的 --pod-network-cidr
      "Backend": {
        "Type": "vxlan"
      }
    }
...

apiVersion: apps/v1
kind: DaemonSet
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        - --iface=<eth>  # 可指定 nic

# forwarding
master:~ # iptables -P FORWARD ACCEPT
node:~ # iptables -P FORWARD ACCEPT
```


`calico`

```bash
master:~ # wget https://docs.projectcalico.org/v3.8/manifests/calico.yaml
master:~ # sed -i 's@192.168.0.0/16@10.244.0.0/16@' calico.yaml
master:~ # kubectl apply -f calico.yaml
## config: /etc/cni/net.d/10-calico.conflist, /etc/cni/net.d/calico-kubeconfig
## container: calico
```


### node

node 必須做過 prepare 步驟

```bash
node:~ # kubeadm join <master_ip>:6443 --token <token_id> --discovery-token-ca-cert-hash sha256:<ca_hash>
```


### tip

```bash
# reset master
master:~ # rm -rf $HOME/.kube
master:~ # rm -rf /etc/cni/net.d/*
master:~ # kubeadm reset

# reset node
master:~ # kubectl delete node <node>
node:~ # rm -rf $HOME/.kube
node:~ # rm -rf /etc/cni/net.d/*
node:~ # kubeadm reset

# basic
master:~ # kubectl version
master:~ # kubectl api-resources
master:~ # kubectl --help
master:~ # kubectl <cmd> --help

# debug
master:~ # kubectl describe pod <pod>
master:~ # kubectl logs <pod> -c <container>
master:~ # kubectl exec <pod> [-c <container>] -it <cmd>
master:~ # kubectl run -it alpine --image=alpine --restart=Never -- sh
```


### question

1. coredns READY,  是因為有可能是因為網路尚未設定, 只要將 network plugin 裝起來即可

```bash
master:~ # kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                           READY   STATUS
kube-system   coredns-6955765f44-dnmxh       0/1     ContainerCreating
kube-system   coredns-6955765f44-r56gm       0/1     ContainerCreating
kube-system   etcd-master                    1/1     Running
kube-system   kube-apiserver-master          1/1     Running
kube-system   kube-controller-manager-master 1/1     Running
kube-system   kube-proxy-wkqx9               1/1     Running
kube-system   kube-scheduler-master          1/1     Running

master:~ # journalctl -f
Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady messa>
Unable to update cni config: no networks found in /etc/cni/net.d
```


2. network plugin 會產生新的 nic, 所以在 reset 或 apple/delete 要去注意

```bash
master:~ # ip link show
1: lo: <LOOPBACK,UP,LOWER_UP>
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP>
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP>

# ie, flannel
master:~ # ip link show
1: lo: <LOOPBACK,UP,LOWER_UP>
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP>
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP>
4. flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> 
```


---

## namespace

```bash
master:~ # kubectl get ns                  # namespace
master:~ # kubectl create ns <namespace>
master:~ # kubectl delete ns <namespace>
```

`ie`

```yml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <namespace>
```

```bash
mater:~ # kubectl create -f namespace.yaml
mater:~ # kubectl delete -f namespace.yaml
```


---

## pod

```bash
# create pod
master:~ # kubectl create -f pod.yml

# delete pod
master:~ # kubectl delete -f pod.yml
master:~ # kubectl delete pod <pod>
master:~ # kubectl delete pods --all

# list/show pod
master:~ # kubectl get pods
master:~ # kubectl describe pod <pod>

# operate pod
master:~ # kubectl exec <pod> <cmd>
master:~ # kubectl logs <pod>

# access pod by port-forward
master:~ # kubectl port-forward <pod> <host_port>:<container_port>

# access pod by service
master:~ # kubectl expose pod <pod> --type=NodePort
```

`ie`

```yml
# pod.yml 
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
```

```bash
master:~ # kubectl create namespace demo

master:~ # kubectl -n demo create -f pod.yml
master:~ # kubectl -n demo get pods
master:~ # kubectl -n demo describe pods hello
master:~ # kubectl -n demo exec hello env
master:~ # kubectl -n demo exec -it hello sh
master:~ # kubectl -n demo logs hello

# access pod by port-forwad
master:~ # kubectl -n demo port-forward hello 3000:8080
master:~ # curl 127.0.0.1:3000

# access pod by service
master:~ # kubectl -n demo expose pods hello --type=NodePort
master:~ # kubectl -n demo describe service hello   # get node port
master:~ # kubectl -n demo get service              # get node port
master:~ # kubectl -n demo get service hello -o json | jq '.items[].spec.ports[].nodePort'
master:~ # kubectl -n demo describe pods hello # get node ip
master:~ # curl <node_ip>:<node_port>

master:~ # kubectl delete namespace demo
```


---

## node

```bash
master:~ # kubectl get nodes 
master:~ # kubectl describe node <node>
```


---

## replication controller

```bash
master:~ # kubectl get all  -o wide --show-labels
master:~ # kubectl get pods -o wide --show-labels
master:~ # kubectl get rc   -o wide --show-labels    # replicationcontrollers
master:~ # kubectl describe pods <pod>
master:~ # kubectl describe rc <rc>

master:~ # kubectl scale --replicas=4 -f <rc>.yml
```

`ie`

```yml
# replication-controller.yml
apiVersion: v1
kind: ReplicationController
metadata:
  name: hello
spec:
  replicas: 3
  selector:
    app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello
        image: gcr.io/google-samples/node-hello:1.0
        ports:
        - containerPort: 8080
```

```bash
master:~ # kubectl create ns demo
master:~ # kubectl -n demo create -f repication-controller.yml

master:~ # kubectl -n demo get all  -o wide --show-labels
master:~ # kubectl -n demo get pods -o wide --show-labels
master:~ # kubectl -n demo get rc   -o wide --show-labels    # replicationcontrollers
master:~ # kubectl -n demo describe pods hello-xxx
master:~ # kubectl -n demo describe rc hello

# scale
master:~ # kubectl -n demo get pod -l app=hello-world
master:~ # kubectl -n demo get rc hello -o wide
master:~ # kubectl -n demo get rc hello -o json | jq '.status.replicas'
master:~ # kubectl -n demo delete pods hello-xxx
master:~ # kubectl -n demo scale --replicas=4 -f repication-controller.yml

master:~ # kubectl -n demo delete -f repication-controller.yml
master:~ # kubectl delete nss demo
```

---

## replica set

```bash
master:~ # kubectl get all  -o wide --show-labels
master:~ # kubectl get pods -o wide --show-labels
master:~ # kubectl get rs   -o wide --show-labels    # replica-set
master:~ # kubectl describe pods <pod>
master:~ # kubectl describe rs <rs>

master:~ # kubectl scale --replicas=4 -f <rs>.yml
```

`ie`

```yml
# replica-set.yml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: hello
spec:
  replicas: 3
  selector:
    matchLabels:
      env: dev
    matchExpressions:
      - {key: env, operator: In, values: [dev]}
      - {key: env, operator: NotIn, values: [prod]}
  template:
    metadata:
      labels:
        app: hello-world
        env: dev
        version: v1
    spec:
      containers:
      - name: hello
        image: gcr.io/google-samples/node-hello:1.0
        ports:
        - containerPort: 8080
```

```bash
master:~ # kubectl create ns demo
master:~ # kubectl -n demo create -f repica-set.yml

master:~ # kubectl -n demo get all  -o wide --show-labels
master:~ # kubectl -n demo get pods -o wide --show-labels
master:~ # kubectl -n demo get rs   -o wide --show-labels    # replicasets.apps
master:~ # kubectl -n demo describe pods hello-xxx
master:~ # kubectl -n demo describe rs hello

# scale
master:~ # kubectl -n demo get pod -l app=hello-world
master:~ # kubectl -n demo get rs hello -o wide
master:~ # kubectl -n demo get rs hello -o json | jq '.status.replicas'
master:~ # kubectl -n demo delete pods hello-xxx
master:~ # kubectl -n demo scale --replicas=4 -f repica-set.yml

master:~ # kubectl -n demo delete -f repica-set.yml
master:~ # kubectl delete nss demo
```


---

## deployment

```bash
master:~ # kubectl get all
master:~ # kubectl get pods
master:~ # kubectl get rs      # replicasets.apps
master:~ # kubectl get deploy  # deployments.apps
master:~ # kubectl describe pods <pod>
master:~ # kubectl describe rs <rs>
master:~ # kubectl describe deploy <dploy>

# expose deploy to service
master:~ # kubectl expose deploy <deploy> --type=NodePort --external-ip=<master_ip> --port=<node_port> --target-port=<container_port>

# scale
master:~ # kubectl scale --replicas=4 -f <deployment>.yml

# rollout
master:~ # kubectl set image deployment.apps/<deploy> hello=<img>:<tag> --record  # rollup
master:~ # kubectl edit deployments.apps <deploy>                                 # rollup, interactive mode
master:~ # kubectl get deployments.apps -o yaml
master:~ # kubectl path deployments.apps <deploy> -p <patch>                      # rollup, non-interactive mode
master:~ # kubectl rollout undo deployment <deploy>                               # rollback
master:~ # kubectl rollout status deployment <deploy>
master:~ # kubectl rollout history deployment <deploy>
```

`ie`

```yml
# deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello
        image: wsunccake/hello-go:v1
        ports:
        - containerPort: 8080
```

```bash
master:~ # kubectl create ns demo
master:~ # kubectl -n demo create -f deployment.yml

master:~ # kubectl -n demo get all    -o wide --show-labels
master:~ # kubectl -n demo get pods   -o wide --show-labels
master:~ # kubectl -n demo get rs     -o wide --show-labels    # replicasets.apps
master:~ # kubectl -n demo get deploy -o wide --show-labels    # deployments.apps
master:~ # kubectl -n demo describe pods hello-xxx-xxx
master:~ # kubectl -n demo describe rs hello-xxx
master:~ # kubectl -n demo describe deploy hello

# scale
master:~ # kubectl -n demo get pod -l app=hello-world
master:~ # kubectl -n demo get rs hello-xxx- -o wide
master:~ # kubectl -n demo get rs hello-xxx -o json | jq '.status.replicas'
master:~ # kubectl -n demo get deply hello -o wide
master:~ # kubectl -n demo get deply hello -o json | jq '.status.replicas'
master:~ # kubectl -n demo delete pods hello-xxx-xxx
master:~ # kubectl -n demo scale --replicas=4 -f deployment.yml

# rollout
master:~ # kubectl -n demo expose deploy hello --type=NodePort --external-ip=<master_ip> --port=3000 --target-port=8080
master:~ # curl <master_ip>:3000
master:~ # kubectl -n demo get all    -o wide --show-labels
master:~ # kubectl -n demo set image deployment.apps/hello hello=wsunccake/hello-go:v2 --record  # rollup
master:~ # kubectl -n demo rollout status deployment hello
master:~ # kubectl -n demo rollout history deployment hello
master:~ # kubectl -n demo edit deployments.apps hello    # rollup
master:~ # kubectl -n demo rollout undo deployment hello  # rollback

master:~ # kubectl -n demo delete -f deployment.yml
master:~ # kubectl -n demo delete service hello
master:~ # kubectl delete ns demo
```


---

## service

```bash
master:~ # kubectl create -f <svc>.yml
master:~ # kubectl delete -f <svc>.yml

master:~ # kubectl get all
master:~ # kubectl get svc             # services

master:~ # kubectl describe svc <svc>
```

`ie`

```yml
# service.yml 
apiVersion: v1
kind: Service
metadata:
  name: hello
spec:
  type: NodePort
  ports:
  - port: 3000
    nodePort: 30080
    protocol: TCP
    targetPort: 8080
  selector:
    app: hello-world
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: hello
          image: gcr.io/google-samples/node-hello:1.0
        ports:
        - containerPort: 8080
```

```bash
master:~ # kubectl create ns demo
master:~ # kubectl -n demo create -f service.yml

master:~ # kubectl -n demo get all    -o wide --show-labels
master:~ # kubectl -n demo get pods   -o wide --show-labels
master:~ # kubectl -n demo get rs     -o wide --show-labels    # replicasets.apps
master:~ # kubectl -n demo get deploy -o wide --show-labels    # deployments.apps
master:~ # kubectl -n demo get svc    -o wide --show-labels    # services

master:~ # kubectl -n demo describe pods hello-xxx-xxx
master:~ # kubectl -n demo describe deploy hello
master:~ # kubectl -n demo describe svc hello

master:~ # curl master:30080

master:~ # kubectl -n demo delete -f service.yml
master:~ # kubectl delete ns demo
```


---

## label

```bash
master:~ # kubectl get <resource> -l '<key> = <val>'                        # equal
master:~ # kubectl get <resource> -l '<key> != <val>'                       # not equal
master:~ # kubectl get <resource> -l '<key1> = <val1>, <key2> != <val2>'    # () and ()
master:~ # kubectl get <resource> -l '<key> in (<val1>, <val2>)'            # in
master:~ # kubectl get <resource> -l '<key> notin (<val1>, <val2>)'         # not in
```

```yaml
# label.yml
apiVersion: v1
kind: Namespace
metadata:
  name: p1
  labels:
    env: prod
    tier: frontend
    ver: v1.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: p2
  labels:
    env: prod
    tier: frontend
    ver: v2.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: p3
  labels:
    env: prod
    tier: backend
    ver: v1.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: p4
  labels:
    env: prod
    tier: backend
    ver: v2.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: q1
  labels:
    env: qa
    tier: frontend
    ver: v1.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: q2
  labels:
    env: qa
    tier: frontend
    ver: v2.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: q3
  labels:
    env: qa
    tier: backend
    ver: v1.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: q4
  labels:
    env: qa
    tier: backend
    ver: v2.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: d1
  labels:
    env: dev
    tier: frontend
    ver: v1.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: d2
  labels:
    env: dev
    tier: frontend
    ver: v2.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: d3
  labels:
    env: dev
    tier: backend
    ver: v1.0
---

apiVersion: v1
kind: Namespace
metadata:
  name: d4
  labels:
    env: dev
    tier: backend
    ver: v2.0
---
```

```bash
master:~ # kubectl create -f label.yml 

master:~ # kubectl get ns --show-labels
master:~ # kubectl get ns --show-labels -l 'env = prod'                        # equal
master:~ # kubectl get ns --show-labels -l 'env != prod'                       # not equal
master:~ # kubectl get ns --show-labels -l 'env = prod, ver != v1.0'           # (env=prod) and (ver!=v1.0)
master:~ # kubectl get ns --show-labels -l 'env in (qa, dev)'                  # in
master:~ # kubectl get ns --show-labels -l 'env notin (qa, dev)'               # not in
master:~ # kubectl get ns --show-labels -l 'env in (qa, dev), tier = frontend' 

master:~ # kubectl delete -f label.yml 
```

---

## envar

```bash
master:~ # kubectl set env <resource> --all --list
master:~ # kubectl set env <resource> <key>=<val>
```

`ie`

```yml
# envar.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
        env: dev
        version: v1
    spec:
      containers:
      - name: hello
        image: gcr.io/google-samples/node-hello:1.0
        ports:
        - containerPort: 8080
        env:
        - name: DEMO_MESSAGE
          value: "Hello from the environment"
        - name: DEMO_APP_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
```

```bash
master:~ # kubectl create ns demo
master:~ # kubectl -n demo create -f envar.yml

master:~ # kubectl -n demo exec hello env
master:~ # kubectl -n demo exec hello -- sh -c 'echo $DEMO_MESSAGE'
master:~ # kubectl -n demo set env pods --all --list
master:~ # kubectl -n demo set env deployment.apps/hello --all MY_ENV=my_val

master:~ # kubectl -n demo delete -f envar.yml
master:~ # kubectl delete ns demo
```


---

## secret

```bash
master:~ # kubectl create secret generic <secret> --from-literal=<key>=<val> --from-file=<file>
master:~ # kubectl delete secret <secret>
```

`ie`

```yml
# secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: demo-secret
type: Opaque
data:
  passphrase: cGhyYXNl
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
        env: dev
        version: v1
    spec:
      containers:
      - name: hello
        image: gcr.io/google-samples/node-hello:1.0
        ports:
        - containerPort: 8080
        env:
        - name: SECRET_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: username
        - name: SECRET_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        - name: SECRET_PASSPHRASE
          valueFrom:
            secretKeyRef:
              name: demo-secret
              key: passphrase
        volumeMounts:
          - name: secret-volume
            mountPath: /tmp
            readOnly: true
      volumes:
        - name: secret-volume
          secret:
            secretName: demo-secret
```

```bash
master:~ # kubectl create ns demo

master:~ # echo -n "pass" > ./password
master:~ # echo -n "phrase" | base64
master:~ # echo 'cGhyYXNl' | base64 --decode

master:~ # kubectl -n demo create secret generic db-secret --from-literal=username=admin --from-file=./password
master:~ # kubectl -n demo get secrets
master:~ # kubectl -n demo describe secret db-secret

master:~ # kubectl -n demo create -f secret.yml
master:~ # kubectl -n demo exec hello-xxx-xxx env
master:~ # kubectl -n demo exec -it hello-xxx-xxx -- ls /tmp/
master:~ # kubectl -n demo exec -it hello-xxx-xxx -- cat /tmp/passphrase

master:~ # kubectl -n demo delete -f secret.yml
master:~ # kubectl -n demo delete secret db-secret
master:~ # kubectl delete ns demo
```


---

## config map

```bash
master:~ # kubectl create configmap <configmap> --from-file=<file>
master:~ # kubectl get configmaps
master:~ # kubectl describe configmaps <config>

master:~ # kubectl delete configmaps <config>
```

`ie`

```yml
# configMap.yml
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: NodePort
  ports:
  - port: 80
    nodePort: 30080
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: hello
        image: nginx:alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - name: conf-volume
          mountPath: /usr/share/nginx/html
      volumes:
      - name: conf-volume
        configMap:
          name: configmap-html
          items:
          - key: test.html
            path: test.html
```

```html
<!-- test.html -->
<!DOCTYPE html>
<html>
<head>
<title>title</title>
</head>
<body>

<h1>test</h1>
<p>configMap</p>

</body>
</html>
```

```bash
master:~ # kubectl create ns demo

master:~ # kubectl -n demo create configmap configmap-html --from-file=./test.html
master:~ # kubectl -n demo get configmaps
master:~ # kubectl -n demo describe configmaps configmap-html
master:~ # kubectl -n demo create -f configMap.yml

master:~ # curl <master_ip>:30080
master:~ # curl <master_ip>:30080/test.html

master:~ # kubectl -n demo delete -f configMap.yml
master:~ # kubectl -n demo delete configmap configmap-html
master:~ # kubectl delete ns demo
```


---

## service discovery


---

## health check


---

## volume


---

## file

```bash
master:~ # kubectl cp <src> <pod>:<dest>
master:~ # kubectl cp <pod>:<src> <dest>
```


---

## app

```bash
# name space
master:~ # kubectl get namespace
master:~ # kubectl create namespace <namespace>
master:~ # kubectl delete namespace <namespace>

# list
master:~ # kubectl get nodes       [-o wide] [--all-namespaces|-A]
master:~ # kubectl get pods        [-o wide] [--all-namespaces] [--show-all] [--show-labels]
master:~ # kubectl get deployments [-o wide] [--all-namespaces]
master:~ # kubectl get services    [-o wide] [--all-namespaces]
master:~ # kubectl get replicasets [-o wide] [--all-namespaces]
master:~ # kubectl describe nodes        [--all-namespaces]
master:~ # kubectl describe pods         [--all-namespaces]
master:~ # kubectl describe deployments  [--all-namespaces]
master:~ # kubectl describe services     [--all-namespaces]
master:~ # kubectl describe replicasets  [--all-namespaces]

# create app
master:~ # kubectl run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=<container_port>
master:~ # kubectl expose deployment hello-world --external-ip=<mater_ip>|<node_ip> --port=<external_port> --target-port=<container_port> --type=NodePort

# delete app
master:~ # kubectl delete service hello-world
master:~ # kubectl delete deployment hello-world
```


### example

```bash
master:~ # kubectl create namespace demo
master:~ # kubectl -n demo run hello-world --image=gcr.io/google-samples/node-hello:1.0 --port=8080
master:~ # kubectl -n demo get pods
master:~ # kubectl -n demo get deployments

master:~ # kubectl -n demo expose deployment hello-world --external-ip=192.168.31.200 --port=80 --target-port=8080 --type=NodePort
master:~ # curl http://192.168.31.200
master:~ # kubectl -n demo exec hello-world -it bash

master:~ # kubectl -n demo delete service hello-world
master:~ # kubectl -n demo delete deployment hello-world
master:~ # kubectl delete namespace demo
```

---

## ref

[kubernetes-handbook](https://github.com/rootsongjc/kubernetes-handbook)
