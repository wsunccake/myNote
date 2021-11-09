# rancher

## install

```bash
[linux:~ ] # docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged \
  rancher/rancher:latest
```


---

## cli

```bash
# install
[linux:~ ] # curl -sL https://releases.rancher.com/cli2/v2.4.11/rancher-linux-amd64-v2.4.11.tar.gz
[linux:~ ] # tar zxf rancher-linux-amd64-v2.4.11.tar.gz
[linux:~ ] # install -m 755 rancher-v2.4.11/rancher /usr/local/bin/.

# help
[linux:~ ] # rancher help

# login
[linux:~ ] # rancher login https://<rancher ip> --token <token>

# context
[linux:~ ] # rancher context current
[linux:~ ] # rancher context switch

# cluster
[linux:~ ] # rancher cluster
[linux:~ ] # rancher cluster create <cluster>
[linux:~ ] # rancher cluster add-node --controlplane --etcd <cluster>   # return command to deploy control node
[linux:~ ] # rancher cluster add-node --worker <cluster>                # return command to deploy work node
[linux:~ ] # rancher cluster delete <cluster>

# node
[linux:~ ] # rancher node
[linux:~ ] # rancher node delete <node>

# kubectl
[linux:~ ] # rancher kubectl config view --raw
[linux:~ ] # rancher kubectl get node

# inspect
[linux:~ ] # rancher inspect --type cluster <cluster>
[linux:~ ] # rancher inspect --type <node> <node>
```

https://<rancher ip>/apikeys to create <token>


---

## deploy issue

### cert issue

```bash
[node:~ ] # docker stop $(docker ps -aq)
[node:~ ] # docker system prune -f
[node:~ ] # docker volume rm $(docker volume ls -q)
[node:~ ] # docker image rm $(docker image ls -q)
[node:~ ] # rm -rf /etc/ceph \
  /etc/cni \
  /etc/kubernetes \
  /opt/cni \
  /opt/rke \
  /run/secrets/kubernetes.io \
  /run/calico \
  /run/flannel \
  /var/lib/calico \
  /var/lib/etcd \
  /var/lib/cni \
  /var/lib/kubelet \
  /var/lib/rancher/rke/log \
  /var/log/containers \
  /var/log/pods \
  /var/run/calico
```


---

## ref

[Rancher 2.5.7-2.5.9](https://rancher.com/docs/rancher/v2.5/en/)
