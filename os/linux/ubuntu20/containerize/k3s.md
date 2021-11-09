# k3s

## prepare

```bash
[ubunut:~ ] # vi /etc/hosts
192.168.0.11   master
192.168.0.12   node1
192.168.0.13   node2
```


---

## install

```bash
[master:~ ] # curl -sfL https://get.k3s.io | sh -
[master:~ ] # systemctl status k3s
[master:~ ] # cat /var/lib/rancher/k3s/server/token  # token
[master:~ ] # cat /etc/rancher/k3s/k3s.yaml          # config
```

```bash
[node:~ ] # k3s_url=https://<master>:6443
[node:~ ] # k3s_token=<token>
[node:~ ] # curl -sfL https://get.k3s.io | K3S_URL=${k3s_url} K3S_TOKEN=${k3s_token} sh -
[node:~ ] # systemctl status k3s-agent
```

```bash
[master:~ ] # kubectl config get-clusters
[master:~ ] # kubectl cluster-info
[master:~ ] # kubectl get nodes
[master:~ ] # kubectl get namespaces
[master:~ ] # kubectl get endpoints -n kube-system
[master:~ ] # kubectl get pods -n kube-system
```


---

## test

```bash
[master:~ ] # kubectl create deployment hello-world --image=gcr.io/google-samples/node-hello:1.0
[master:~ ] # kubectl expose deployment hello-world --type=LoadBalancer --port=8080
[master:~ ] # kubectl get svc

[master:~ ] # curl http://<EXTERNAL-IP>:8080
```


---

## other

containerd map docker

```bash
ctr image ls                            docker images
ctr image pull <image>                  docker pull <image>
ctr image tag <old> <new>               docker tag <old> <new>
ctr image push <image>                  docker push <image>
ctr image pull <image>                  docker pull <image>
ctr image import <image>.tar            docker load < <image>.tar.gz
ctr run -d <image> <name>               docker run -d --name=<name> <image>
ctr task ls                             docker ps
```

```bash
[ubuntu:~ ] # crictl ps
[ubunut:~ ] # ip -d link show flannel.1
```


---

## uninstall

```bash
[master:~ ] # /usr/local/bin/k3s-uninstall.sh

[node:~ ] # /usr/local/bin/k3s-agent-uninstall.sh
```


---

## klipper

klipper is k3s default Service LB

```bash
# disable servicelb for master
[master:~ ] # curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable servicelb" sh -

# check
[master:~ ] # kubectl get all -n kube-system | grep svclb
# no kube-system/svclb-traefik
```


---

## ref

[K3s - Lightweight Kubernetes](https://rancher.com/docs/k3s/latest/en/)
