# helm

## install 2.16

```bash
# check kube info
master:~ # kubectl config current-context
master:~ # kubectl cluster-info
master:~ # cat ~/.kube/config

# prepare kube account and role
## serviceaccount
master:~ # kubectl get serviceaccount --all-namespaces
master:~ # kubectl -n kube-system create serviceaccount tiller
## clusterrole
master:~ # kubectl get clusterrole --all-namespaces
master:~ # kubectl create clusterrolebinding tiller-cluster-admin --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
## patch
master:~ # kubectl -n kube-system get clusterrole cluster-admin -o yaml
master:~ # kubectl -n kube-system patch deploy tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'


# install
master:~ # curl https://get.helm.sh/helm-v2.16.0-linux-amd64.tar.gz -o helm-v2.16.0-linux-amd64.tar.gz
master:~ # tar zxf helm-v2.16.0-linux-amd64.tar.gz
master:~ # mv linux-amd64/helm /usr/local/bin/

# init
master:~ # helm init --history-max 200
## config: $HOME/.helm
## conatienr: tiller-deploy
master:~ # helm reset
```


---

## repo

```bash
master:~ # helm repo update
master:~ # helm repo list
master:~ # helm repo add <repo> <url>
master:~ # helm repo remove <repo>
master:~ # helm search repo <pkg>

## ie
master:~ # helm repo add stable https://kubernetes-charts.storage.googleapis.com/

# environment variable
master:~ # kubectl -n kube-system describe pod tiller-deploy
# get the <helm_ip>, <helm_port>
# [env HELM_HOST=<helm_ip>:<helm_port>] 
```


---

## package

```bash
master:~ # helm search <chart>
master:~ # helm list
master:~ # helm install <serivce>
master:~ #helm delete <serivce>

## ie
master:~ # kubectl create namespace demo
master:~ # helm search mysql
master:~ # helm install stable/mysql --namespace demo
master:~ # kubectl get services --all-namespaces
master:~ # helm delete --purge washed-squid-mysql
master:~ # kubectl delete namespace demo
```
