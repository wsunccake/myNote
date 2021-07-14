# argo cd

## install

### api server

```bash
# create namespace
[linux:~ ] # kubectl create namespace argocd

# install argo cd
[linux:~ ] # kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml        # non ha
[linux:~ ] # kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.0.4/manifests/ha/install.yaml     # ha

# access argo cd api server
[linux:~ ] # kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'   # load balancer
[linux:~ ] # kubectl port-forward svc/argocd-server -n argocd 8080:443                           # port forwarding

# retrieve password
[linux:~ ] # kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```


### client cli

```bash
# install cli
[linux:~ ] # curl -L -O https://github.com/argoproj/argo-cd/releases/download/v2.0.4/argocd-linux-amd64
[linux:~ ] # install -m 755 argocd-linux-amd64 /usr/local/bin/argocd
```


---

```bash
[linux:~ ] # argocd login <ip>:<port> --username <username> --password <password>
```
