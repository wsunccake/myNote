# kubectl

## install

```bash
# download and valid
linux:~ # curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
linux:~ # curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
linux:~ # echo "$(<kubectl.sha256) kubectl" | sha256sum --check

# install for system
linux:~ # install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# install for user
linux:~ $ mkdir -p $HOME/.local/bin
linux:~ $ mv ./kubectl $HOME/.local/bin/kubectl
linux:~ $ export PATH=$HOME/.local/bin/kubectl:$PATH

# config for user
linux:~ $ mkdir -p $HOME/.kube
linux:~ $ touch $HOME/.kube/config
linux:~ $ chmod 600 $HOME/.kube/config
linux:~ $ cat <k8s cluster config> >> $HOME/.kube/config
```


---

## auto-completetion

```bash
# install bash-completion
linux:~ # dnf install bash-completion

# auto-completetion for system
linux:~ # kubectl completion bash > /etc/bash_completion.d/kubectl

# auto-completetion for bash user
linux:~ # echo "source <(kubectl completion bash)" >> ~/.bashrc
linux:~ # echo 'alias k=kubectl' >>~/.bashrc
linux:~ # echo 'complete -F __start_kubectl k' >>~/.bashrc

# auto-completetion for zsh user
linux:~ # echo "source <(kubectl completion zsh)" >>~/.zshrc
linux:~ # echo 'alias k=kubectl' >>~/.zshrc
linux:~ # echo 'complete -F __start_kubectl k' >>~/.zshrc
```


---

## test

```bash
linux:~ # kubectl version --client
```


---

## common

```bash
linux:~ # kubectl api-versions
linux:~ # kubectl api-resources

linux:~ # kubectl get node [-o wide|json|yaml] [--all-namespaces|-A]
linux:~ # kubectl get pod,deploy,svc

linux:~ # kubectl apply -f <file>.yaml
linux:~ # kubectl delete [-f <file>.yaml|<type>/<name>]
linux:~ # kubectl edit [-f <file>.yaml|<type>/<name>]

linux:~ # kubectl exec [-it] <type>/<name> [-c <container>] -- <command>
linux:~ # kubectl describe <type>/<name>
linux:~ # kubectl logs [-f] <type>/<name> [-c <container>]

linux:~ # kubectl wait --for=condition=Ready [-f <file>.yaml|<type>/<name>]
linux:~ # kubectl describe <type>/<name> | grep Condition -A5       # list all condition
```


---

## config

```bash
linux:~ # cat /etc/kubernetes/admin.conf                              # system default
linux:~ # cat $HOME/.kube/config                                      # user default
linux:~ # export KUBECONFIG=<kube config>                             # environment variable

# view
linux:~ # kubectl config view --minify [--kubeconfig <kube config>]

# combine multi config
linux:~ # env KUBECONFIG=<config 1>:<config 2>:... kubectl config view --flatten > $HOME/.kube/config
linux:~ # chmod 600 $HOME/.kube/config

# context
linux:~ # kubectl config get-contexts
linux:~ # kubectl config rename-context <old name> <new name>
linux:~ # kubectl config use-context <context>
linux:~ # kubectl config current-context
linux:~ # kubectl config set-context <context>
\ [--namespace <namespace>]
\ [--cluster=<cluster>]
\ [--user=user_nickname]
linux:~ # kubectl config delete-context <context>

# cluster
linux:~ # kubectl config get-clusters
linux:~ # kubectl config set-cluster <cluster>
```


---

## namespace

```bash
linux:~ # kubectl get namespace
linux:~ # kubectl create namespace <namespace>
linux:~ # kubectl delete namespace <namespace>
```


---

## other

```bash
linux:~ # kubectl port-forward <type>/<name> [<local port>:]<remote port>

linux:~ # kubectl -n <namespace> cp <file spec src> <file spec dest> [-c <container>]
remote: [<namespace>/]<pod>:<path>
local: <path>
```
