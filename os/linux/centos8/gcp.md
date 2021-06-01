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


### auth

```bash
[centos:~ ] # gcloud init [--skip-diagnostics|--console-only]
...

[centos:~ ] # ls .boto
[centos:~ ] # gcloud auth login <account>
```

web: https://console.cloud.google.com/


### config

```bash
# project
[centos:~ ] # gcloud projects list
[centos:~ ] # gcloud config set project <PROJECT_ID>
[centos:~ ] # gcloud config get-value project

[centos:~ ] # gcloud config --help
[centos:~ ] # gcloud config list [--all]
[centos:~ ] # gcloud config set core/project <project>

[centos:~ ] # gcloud config configurations list
[centos:~ ] # gcloud config configurations activate <conf>
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
# download and valid
[centos:~ ] # curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
[centos:~ ] # curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
[centos:~ ] # echo "$(<kubectl.sha256) kubectl" | sha256sum --check

# install for system
[centos:~ ] # install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# install for user
[centos:~ ] $ mkdir -p $HOME/.local/bin/kubectl
[centos:~ ] $ mv ./kubectl $HOME/.local/bin/kubectl
[centos:~ ] $ export PATH=$HOME/.local/bin/kubectl:$PATH

# install bash-completion
[centos:~ ] # dnf install bash-completion

# auto-completetion for system
[centos:~ ] # kubectl completion bash >/etc/bash_completion.d/kubectl

# auto-completetion for user
[centos:~ ] $ echo "source <(kubectl completion bash)" >> ~/.bashrc
[centos:~ ] $ echo 'alias k=kubectl' >>~/.bashrc
[centos:~ ] $ echo 'complete -F __start_kubectl k' >>~/.bashrc

# auto-completetion for user
[centos:~ ] $ source <(kubectl completion zsh) >>~/.zshrc
[centos:~ ] $ echo 'alias k=kubectl' >>~/.zshrc
[centos:~ ] $ echo 'complete -F __start_kubectl k' >>~/.zshrc

# test
[centos:~ ] # kubectl version --client
```


### import gke credentials to kubectl

```bash
[centos:~ ] # gcloud container clusters list
[centos:~ ] # gcloud container clusters get-credentials <cluster> [--zone <zone>]

[centos:~ ] # kubectl config get-contexts
[centos:~ ] # kubectl config get-cluster
[centos:~ ] # kubectl config set-cluster <cluster>
[centos:~ ] # kubectl config current-context

[centos:~ ] # kubectl cluster-info
```
