# istio

## install

```bash
[linux:~ ] # curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.10.2 TARGET_ARCH=x86_64 sh -
[linux:~ ] # install -m 755 istio-1.10.2/bin/istioctl /usr/local/bin/.
[linux:~ ] # istioctl install --set profile=demo -y
[linux:~ ] # kubectl label namespace default istio-injection=enabled 
```


---

## usage

```bash
[linux:~ ] # istioctl profile list
[linux:~ ] # istioctl profile dump [<profile>]
[linux:~ ] # istioctl profile diff default demo

[linux:~ ] # istioctl uninstall --purge

[linux:~ ] # istioctl proxy-status|ps
[linux:~ ] # istioctl proxy-status <pod>

[linux:~ ] # istioctl proxy-config|pc all <pod>
[linux:~ ] # istioctl proxy-config|pc cluster <pod>

[linux:~ ] # istioctl analyze
```


---

## kube

```bash
[linux:~ ] # kubectl api-resources | grep istio
[linux:~ ] # kubectl get namespace | grep istio

# for istio resource
[linux:~ ] # kubectl get gateways|gw -A -o wide
[linux:~ ] # kubectl get virtualservices|vs -A -o wide

# for istio namespace
[linux:~ ] # kubectl get po|pods -n istio-system
```
