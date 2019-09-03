# Google Cloud SDK


## install

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


## usage

```bash
gcloud init
gcloud init --skip-diagnostics
gcloud init --console-only
```
