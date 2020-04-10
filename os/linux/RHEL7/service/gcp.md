# Google Cloud Platform


## Google Cloud SDK


### install

```bash
linux:~ # wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-245.0.0-linux-x86_64.tar.gz
linux:~ # curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-245.0.0-linux-x86_64.tar.gz

linux:~ # tar zxf google-cloud-sdk-245.0.0-linux-x86_64.tar.gz
linux:~ # cd google-cloud-sdk
linux:~/google-cloud-sdk # ./install.sh

linux:~ # cat ~/.bashrc
...
# The next line updates PATH for the Google Cloud SDK.
if [ -f '$HOME/google-cloud-sdk/path.bash.inc' ]; then . '$HOME/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '$HOME/google-cloud-sdk/completion.bash.inc' ]; then . '$HOME/google-cloud-sdk/completion.bash.inc'; fi
```


### auth

```bash
linux:~ # gcloud init [--skip-diagnostics|--console-only]
...

linux:~ # ls .boto


linux:~ # gcloud auth login <account>
```

web: https://console.cloud.google.com/


### config

```bash
linux:~ # gcloud config --help
linux:~ # gcloud config list [--all]
linux:~ # gcloud config set core/project <project>
```


---

## Google Storage


### cli

```bash
linux:~ # gsutil help
linux:~ # gsutil version

linux:~ # gsutil ls -la [gs://]
linux:~ # gsutil mb gs://<bucket>
linux:~ # gsutil du -hs [gs://]
linux:~ # gsutil mv gs://<src> gs://<dst>

linux:~ # gsutil cp <src> <dst>
linux:~ # gsutil cp gs://old.txt gs://new.txt
linux:~ # gsutil cp file.txt gs://file.txt
linux:~ # gsutil cp gs://file.txt file.txt 

linux:~ # gsutil rm gs://<file>
linux:~ # gsutil cat gs://<file>

linux:~ # gsutil mb -l asia gs://<bucket>
linux:~ # gsutil ls -Lb gs://<bucket>/
```


---

## Google Compute Engine

```bash
# zone
## list
linux:~ # gcloud compute zones list
linux:~ # gcloud compute zones describe <zone>

# image
## list
linux:~ # gcloud compute images list
linux:~ # gcloud compute images list --filter="name=<xxx>"
linux:~ # gcloud compute images describe <image>
linux:~ # gcloud compute images create <image> --source-uri=gs://<dst>

# machine-type
## list
linux:~ # gcloud compute machine-types list 
linux:~ # gcloud compute machine-types list --filter="zone:asia-east"
linux:~ # gcloud compute machine-types list --filter="name~n1-standard AND zone~asia-east"
linux:~ # gcloud compute machine-types describe <machine-type>

# disk-type
## list
linux:~ # gcloud compute disk-types list
linux:~ # gcloud compute disk-types describe <disk-type>

# instance/vm
## list
linux:~ # gcloud compute instances list
linux:~ # gcloud compute instances list --filter="status=RUNNING"
linux:~ # gcloud compute instances list --filter="zone:asia-east AND name~<xxx>"
linux:~ # gcloud compute instances describe <instance>
## create with machine-type
linux:~ # gcloud compute instances create <instance> --zone=<zone> --image-project=<image-project> --image=<image> --machine-type=<machine-type> [--boot-disk-size=<disk-szie> --boot-disk-type=<disk-type>]
## create with custom
linux:~ # gcloud compute instances create <instance> --zone=<zone> --image-project=<image-project> --image=<image> --custom-cpu=<cpu-number> --custom-memory=<mem-size> [--boot-disk-size=<disk-size> --boot-disk-type=<disk-type> --tags=<tag1>,<tag2>]
## delete
linux:~ # gcloud compute instances delete <instance>
## start
linux:~ # gcloud compute instances start <instance>
## stop
linux:~ # gcloud compute instances stop <instance>
## show
linux:~ # gcloud compute instances describe <instance>

# ssh
linux:~ # gcloud compute ssh [<user>@]<instance>
<vm>:~ $ sudo passwd `whoami`

# serial, ~. to escape
linux:~ # gcloud compute connect-to-serial-port <instance>

# info
linux:~ # gcloud compute project-info describe
linux:~ # gcloud compute project-info add-metadata --metadata enable-oslogin=TRUE
linux:~ # gcloud compute project-info remove-metadata --keys=enable-oslogin

# address
linux:~ # gcloud compute addresses list
linux:~ # gcloud compute addresses create <access_config> --region <region>
linux:~ # gcloud compute addresses delete <access_config>

linux:~ # gcloud compute instances describe <vm>   # show current access config
linux:~ # gcloud compute instances add-access-config <vm> --access-config-name <access_config> --address <ip>
linux:~ # gcloud compute instances delete-access-config <vm> --access-config-name <access_config>
```

---

## Google Container Registry


```bash
# build container image
## main.go
linux:~ # cat main.go
package main

import (
    "fmt"
    "net/http"
)

func handler(writer http.ResponseWriter, request *http.Request) {
    fmt.Fprint(writer, "Hello Go")
}

func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}


## Dockerfile
linux:~ # cat Dockerfile
FROM golang:alpine
WORKDIR /app
ADD . /app
RUN cd /app && go build -o app
EXPOSE 8080
ENTRYPOINT ./app


## build and run
linux:~ # docker build -t app .
linux:~ # docker run -d -p 8080:8080 app
linux:~ # curl http://127.0.0.1:8080


# setup gcp project
linux:~ # gcloud auth configure-docker                 # create $HOME/.docker/config.json
linux:~ # gcloud config list
linux:~ # gcloud config set project <project>
linux:~ # gcloud config set compute/zone <zone>
## use asia
linux:~ # gcloud config set compute/zone asia-east1-a


# upload container image
## rename
linux:~ # docker tag <iamge> <gcr>/<project>/<iamge>
linux:~ # docker tag app asia.gcr.io/myproject/app
## upload
linux:~ # docker push <gcr>/<project>/<iamge>
linux:~ # docker push asia.gcr.io/myproject/app

# list container image
linux:~ # gcloud container images list
linux:~ # gcloud container images list [--repository=<gcr>/<project>]   ## specfic repo

# delete container image
linux:~ # gcloud container images delete <gcr>/<project>/<image>

# describe container image
linux:~ # gcloud container images describe <gcr>/<project>/<image>
```


---

## Google Kubenetes Engine

```bash
# install kubectl
linux:~ # gcloud components install kubectl                        # create $HOME/.kube/config


# create cluster
linux:~ # gcloud container clusters create <cluster> [--num-nodes=<n>] [--zone <zone>]

# list cluster
linux:~ # gcloud container clusters list
linux:~ # gcloud compute instances list | grep gke

# delete cluster
linux:~ # gcloud container clusters delete <cluster>


# deploy service
## create pod
linux:~ # kubectl create deployment <service> --image=<gcr>/<project>/<image>
linux:~ # kubectl create deployment web --image=asia.gcr.io/myproject/app
## create service, associate pod to service
linux:~ # kubectl expose deployment <service> --type=LoadBalancer [--port <cluster_port>] [--target-port <pod_port>]
linux:~ # kubectl expose deployment web --type=LoadBalancer --port 80 --target-port 8080
## port: cluster port, target-port: container/pod port

## list pod, deployment, service
linux:~ # kubectl get pod
linux:~ # kubectl get deployment
linux:~ # kubectl get service

## scaling service
linux:~ # kubectl scale deployment <service> --replicas=<n>
linux:~ # kubectl scale deployment web --replicas=3
```
