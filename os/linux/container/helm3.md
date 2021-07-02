# helm 3.x

## install

```bash
[linux:~ ] # curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
[linux:~ ] # chmod 700 get_helm.sh
[linux:~ ] # env VERIFY_CHECKSUM=false ./get_helm.sh
```

```bash
[linux:~ ] # helm help
[linux:~ ] # helm version
```


---

## repo

```bash
[linux:~ ] # helm repo --help
[linux:~ ] # helm repo add <repo name> <repo url>
[linux:~ ] # helm repo remove <repo name>
[linux:~ ] # helm repo list
[linux:~ ] # helm repo update

# example
[linux:~ ] # helm repo add bitnami https://charts.bitnami.com/bitnami
[linux:~ ] # helm repo remove bitnami
[linux:~ ] # helm repo list
[linux:~ ] # helm repo update
```


---

## release

```bash
[linux:~ ] # kubectl config view
[linux:~ ] # kubectl config current-context

[linux:~ ] # helm search repo|hub <keyword>                        # search chart
[linux:~ ] # helm pull <chart url>|<repo>/<chart name>             # download chart
[linux:~ ] # helm install <name> <chart url>|<repo>/<chart name>   # install release from chart
[linux:~ ] # helm uninstall <name>                                 # uninstall release
[linux:~ ] # helm list                                             # list all release
[linux:~ ] # helm status <name>

# example
[linux:~ ] # helm search repo mysql
[linux:~ ] # helm pull bitnami/mysql
[linux:~ ] # helm install mysql bitnami/mysql
[linux:~ ] # helm install bitnami/mysql -g
[linux:~ ] # helm uninstall mysql
[linux:~ ] # helm list
```


---

## chart

```bash
[linux:~ ] # helm create hello-world
[linux:~ ] # tree hello-world
tree hello-world/
hello-world/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml

[linux:~ ] # cat hello-world/Chart.yaml 
[linux:~ ] # cat hello-world/values.yaml
[linux:~ ] # cat hello-world/templates/deployment.yaml
[linux:~ ] # cat hello-world/templates/service.yaml

[linux:~ ] # helm lint ./hello-world
[linux:~ ] # helm template ./hello-world

[linux:~ ] # helm install hello-world ./hello-world
[linux:~ ] # helm list

[linux:~ ] # helm upgrade hello-world ./hello-world
[linux:~ ] # helm history
[linux:~ ] # helm status hello-world
[linux:~ ] # helm rollback hello-world 1
```


---

## ref

[helm](https://helm.sh/)
