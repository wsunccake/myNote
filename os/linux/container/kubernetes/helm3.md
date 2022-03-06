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

[linux:~ ] # helm search repo|hub [ --version] <keyword>                    # search chart
[linux:~ ] # helm pull <chart url>|<repo>/<chart name>                      # download chart
[linux:~ ] # helm install <release name> <chart url>|<repo>/<chart name>    # install release from chart
[linux:~ ] # helm uninstall <release name>                                  # uninstall release
[linux:~ ] # helm list                                                      # list all release
[linux:~ ] # helm status <relase name>

[linux:~ ] # helm show chart <chart>
[linux:~ ] # helm show values <chart>

# example
[linux:~ ] # helm search repo mysql
[linux:~ ] # helm search repo --version mysql
[linux:~ ] # helm pull bitnami/mysql
[linux:~ ] # helm install mysql bitnami/mysql
[linux:~ ] # helm install bitnami/mysql -g
[linux:~ ] # helm install bitnami/mysql --debug
[linux:~ ] # helm install bitnami/mysql --dry-run
[linux:~ ] # helm install bitnami/mysql --values <helm values>.yaml
[linux:~ ] # helm uninstall mysql
[linux:~ ] # helm list

[linux:~ ] # helm show chart bitnami/mysql
[linux:~ ] # helm show values bitnami/mysql
```


---

## chart

```bash
[linux:~ ] # helm create hello-world
[linux:~ ] # tree hello-world
tree hello-world/
hello-world/
├── charts                          # chart depends
├── Chart.yaml                      # about information
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
└── values.yaml                     # default configuration

[linux:~ ] # cat hello-world/Chart.yaml
[linux:~ ] # cat hello-world/values.yaml
[linux:~ ] # cat hello-world/templates/deployment.yaml
[linux:~ ] # cat hello-world/templates/service.yaml

[linux:~ ] # helm lint ./hello-world
[linux:~ ] # helm template ./hello-world

# method 1
[linux:~ ] # helm install hello-world ./hello-world

# method 2
[linux:~ ] # helm package hello-world
[linux:~ ] # ls hello-world-0.1.0.tgz
[linux:~ ] # helm install hello-world hello-world-0.1.0.tgz

[linux:~ ] # helm list

[linux:~ ] # helm upgrade hello-world ./hello-world
[linux:~ ] # helm history
[linux:~ ] # helm status hello-world
[linux:~ ] # helm rollback hello-world 1
```


---

## auto-completetion

```bash
# for bash
[linux:~ ] # helm completion bash > /etc/bash_completion.d/helm     # system
[linux:~ ] # echo "source <(helm completion bash)" >> ~/.bashrc     # user

# for zsh
[linux:~ ] # echo "source <(helm completion zsh)" >> ~/.zshrc       # user
```

---

## ref

[helm](https://helm.sh/)
