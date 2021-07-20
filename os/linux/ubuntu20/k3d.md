# k3d

## prepare

[docker-ce][./docker-ce.md]


---

## install

```bash
[ubunut:~ ] # curl -sLf https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
# -s, --silent
# -L, --location
# -f, --fail

[ubunut:~ ] # curl -sLf https://raw.githubusercontent.com/rancher/k3d/main/install.sh | TAG=v4.4.7 bash
```


---

## kubectl

```bash
[ubunut:~ ] # curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
[ubunut:~ ] # install -m 755 kubectl /usr/local/bin/.
```


---

## usge

```bash
# help
[ubunut:~ ] # k3d help
[ubunut:~ ] # k3d version

# cluster
[ubunut:~ ] # k3d cluster list
[ubunut:~ ] # k3d cluster create <cluster> [-s <n>] [-a <m>]
# -a, --agent
# -s, --servers
[ubunut:~ ] # k3d cluster delete <cluster>

# kubeconfig
[ubunut:~ ] # k3d kubeconfig get -a
[ubunut:~ ] # k3d kubeconfig merge -a

# ie
[ubunut:~ ] # k3d cluster create mycluster -s 3 -a 3
[ubunut:~ ] # k3d kubeconfig merge mycluster > ~/.k3d/kubeconfig-mycluster.yaml
[ubunut:~ ] # KUBECONFIG=~/.k3d/kubeconfig-mycluster.yaml kubectl get nodes

# test
[ubunut:~ ] # kubectl create deployment hello-world --image=gcr.io/google-samples/node-hello:1.0
[ubunut:~ ] # kubectl expose deployment hello-world --type=LoadBalancer --port=8080
[ubunut:~ ] # kubectl get svc
```


---

## ref

[k3d](https://k3d.io/)
