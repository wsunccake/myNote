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

## cli

```bash
[linux:~ ] # argocd version
[linux:~ ] # argocd help
[linux:~ ] # argocd cluster list

# login / logout
[linux:~ ] # argocd login <ip>:<port> [--username <username> --password <password>]
[linux:~ ] # argocd logout

# account
[linux:~ ] # argocd account list
[linux:~ ] # argocd account get
[linux:~ ] # argocd account get-user-info
[linux:~ ] # argocd account update-password

# app
[linux:~ ] # argocd repo list
[linux:~ ] # argocd app create <app> --repo <repo url> --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
[linux:~ ] # argocd app get <app>
[linux:~ ] # argocd app sync <app>
[linux:~ ] # argocd app delete <app>

# ie
[linux:~ ] # argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
[linux:~ ] # argocd app sync guestbook
[linux:~ ] # argocd app get guestbook
[linux:~ ] # kubectl get pod
[linux:~ ] # kubectl get svc
[linux:~ ] # argocd app get delete

# repo
[linux:~ ] # argocd repo list
[linux:~ ] # argocd repo get <repo url>
[linux:~ ] # argocd repo add <repo url> [--username <username>] [--password <password>]
[linux:~ ] # argocd repo rm <repo url>

# project
[linux:~ ] # argocd proj list
[linux:~ ] # argocd proj get <proj>
```

default account admin

private repo must add repo then create app

---

## yaml

```bash
[linux:~ ] # mkdir demo
[linux:~ ] # cd demo
[linux:~/demo ] # git init
[linux:~/demo ] # cat << EOF > app-deploy.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx
EOF
[linux:~/demo ] # cat << EOF > app-svc.yml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx
  name: nginx
  namespace: default
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx
  type: NodePort
EOF

[linux:~/demo ] # git add app-deploy.yml app-svc.yml
[linux:~/demo ] # git commit -m "argocd demo"

[linux:~ ] # argocd app create demo --repo <git url> --path . --dest-server https://kubernetes.default.svc --dest-namespace default
```

---

[Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/)
