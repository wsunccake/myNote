# helm 3.x

## install

```bash
[ubuntu:~ ] # curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
[ubuntu:~ ] # apt-get install apt-transport-https --yes
[ubuntu:~ ] # echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list
[ubuntu:~ ] # apt-get update
[ubuntu:~ ] # apt-get install helm
```
