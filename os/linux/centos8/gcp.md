# Google Cloud Platform


## google cloud sdk


### install

```bash
[centos:~ ] # tee -a /etc/yum.repos.d/google-cloud-sdk.repo << EOM
[google-cloud-sdk]
name=Google Cloud SDK
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOM

[centos:~ ] # dnf install google-cloud-sdk
```


### component

```bash
[centos:~ ] # gcloud components list
[centos:~ ] # gcloud components install <component id>
[centos:~ ] # gcloud components remove <component id>
[centos:~ ] # gcloud components update
```


### auth

```bash
[centos:~ ] # gcloud init [--skip-diagnostics|--console-only]
...
# -> ls $HOME/.boto

[centos:~ ] # gcloud auth login <account>
```

web: https://console.cloud.google.com/


### config

```bash
[centos:~ ] # gcloud config --help
[centos:~ ] # gcloud config list [--all]
[centos:~ ] # gcloud config get-value
[centos:~ ] # gcloud config set <section>/<property> <value>
[centos:~ ] # gcloud config unset

[centos:~ ] # gcloud config get-value core/project
[centos:~ ] # gcloud config get-value compute/region
[centos:~ ] # gcloud config get-value compute/zone

[centos:~ ] # gcloud config set core/project <project id>
[centos:~ ] # gcloud config set compute/region <region>
[centos:~ ] # gcloud config set compute/zone <zone>

[centos:~ ] # gcloud config configurations list
[centos:~ ] # gcloud config configurations activate <conf>
```


## project

```bash
[centos:~ ] # gcloud projects list
[centos:~ ] # export PROJECT_ID=$(gcloud config get-value project -q)
[centos:~ ] # gcloud projects get-iam-policy $PROJECT_ID
```


---

## gce

```bash
[centos:~ ] # gcloud compute regions list               # regsion
[centos:~ ] # gcloud compute zones list                 # all zone
[centos:~ ] # gcloud compute instances list             # vm on zone
```


---

## gke

```bash
# cluster
[centos:~ ] # gcloud container clusters list
[centos:~ ] # gcloud container clusters describe <cluster> [--zone <zone>]
[centos:~ ] # gcloud container clusters get-credentials <cluster> \
  [--project <project>] \
  [--region <region>] \
  [--zone <zone>] # import gcloud credentials to local kubectl
# -> $HOME/.kube/config

[centos:~ ] # gcloud container images list
[centos:~ ] # gcloud container node-pools list --cluster <cluster>
```

---

## cloud sql

```bash
[centos:~ ] # gcloud sql instances list
[centos:~ ] # gcloud sql instances describe <instance>   # host
[centos:~ ] # gcloud sql databases list -i <instance>    # ip
[centos:~ ] # gcloud sql users list -i <instance>        # user
```


---

## kubectl

### install

```bash
[centos:~ ] # gcloud components install kubectl
```


### auto-completetion

```bash
# install bash-completion
[centos:~ ] # dnf install bash-completion

# auto-completetion for bash user
[centos:~ ] $ echo "source <(kubectl completion bash)" >> ~/.bashrc
[centos:~ ] $ echo 'alias k=kubectl' >>~/.bashrc
[centos:~ ] $ echo 'complete -F __start_kubectl k' >>~/.bashrc

# auto-completetion for zsh user
[centos:~ ] $ echo "source <(kubectl completion zsh)" >>~/.zshrc
[centos:~ ] $ echo 'alias k=kubectl' >>~/.zshrc
[centos:~ ] $ echo 'complete -F __start_kubectl k' >>~/.zshrc
```


### import gke credentials to kubectl

```bash
# cluster
[centos:~ ] # kubectl config get-clusters
[centos:~ ] # kubectl config set-cluster <cluster>

# context
[centos:~ ] # kubectl config get-contexts
kubectl config rename-context <old name> <new name>
[centos:~ ] # kubectl config use-context <context>
[centos:~ ] # kubectl config current-context
[centos:~ ] # kubectl config set-context <context>
\ [--namespace <namespace>]
\ [--cluster=<cluster>]
\ [--user=user_nickname]

[centos:~ ] # kubectl cluster-info
```
