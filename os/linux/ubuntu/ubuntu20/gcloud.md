# google-cloud-sdk

## install

```bash
[ubuntu:~ ] # echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
[ubuntu:~ ] # apt-get install apt-transport-https ca-certificates gnupg
[ubuntu:~ ] # curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
[ubuntu:~ ] # apt-get update && sudo apt-get install google-cloud-sdk
```
