# Google Cloud Platform


## Google Cloud SDK


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
[centos:~ ] # gcloud config --help
[centos:~ ] # gcloud config list [--all]
[centos:~ ] # gcloud config set core/project <project>

[centos:~ ] # gcloud config configurations list
[centos:~ ] # gcloud config configurations activate <conf>
```
