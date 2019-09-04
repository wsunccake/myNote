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
```

web: https://console.cloud.google.com/

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
linux:~ # gcloud compute instances list --filter="zone:asia-east AND name~<xxx>"
linux:~ # gcloud compute instances describe <instance>
## create with machine-type
linux:~ # gcloud compute instances create <instance> --zone=<zone> --image-project=<image-project> --image=<image> --machine-type=<machine-type> [--boot-disk-size=<disk-szie> --boot-disk-type=<disk-type>]
## create with custom
linux:~ # gcloud compute instances create <instance> --zone=<zone> --image-project=<image-project> --image=<image> --custom-cpu=<cpu-number> --custom-memory=<mem-size> [--boot-disk-size=<disk-size> --boot-disk-type=<disk-type>]
## delete
linux:~ # gcloud compute instances delete <instance>
## start
linux:~ # gcloud compute instances start <instance>
## stop
linux:~ # gcloud compute instances stop <instance>
## show
linux:~ # gcloud compute instances describe <instance>
```
