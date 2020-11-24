# istio

## install

```bash
master:~ # curl -L https://github.com/istio/istio/releases/download/1.4.2/istio-1.4.2-linux.tar.gz -o istio-1.4.2-linux.tar.gz
master:~ # tar zxf istio-1.4.2-linux.tar.gz
master:~ # mv istio-1.4.2/bin/istioctl /usr/local/bin/

master:~ # for psp in $(kubectl get psp -o jsonpath="{range .items[*]}{@.metadata.name}{'\n'}{end}"); do
  if [ $(kubectl auth can-i use psp/$psp --as=system:serviceaccount:default:default) = yes ]; then
    kubectl get psp/$psp --no-headers -o=custom-columns=NAME:.metadata.name,CAPS:.spec.allowedCapabilities
  fi
done
```


---

## usage

```bash
# create config
master:~ # istioctl manifest apply --set profile=demo
master:~ # kubectl -n istio-system get pods
master:~ # kubectl -n istio-system get services

# deploy app
master:~ # kubectl label namespace <namespace> istio-injection=enabled      # auto inject
master:~ # kubectl create -n <namespace> -f <app>.yaml
master:~ # istioctl kube-inject -f <app>.yaml | kubectl apply -f -          # manual inject

# ie
master:~ # kubectl create namespace bookinfo
master:~ # kubectl label namespace bookinfo istio-injection=enabled
master:~ # kubectl describe namespace bookinfo
master:~ # kubectl -n bookinfo apply -f istio-1.4.2/samples/bookinfo/platform/kube/bookinfo.yaml
master:~ # kubectl -n bookinfo get services
master:~ # kubectl -n bookinfo get pods

master:~ # kubectl -n bookinfo exec -it $(kubectl -n bookinfo get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}') -c ratings -- curl productpage:9080/productpage | grep -o "<title>.*</title>"

master:~ # kubectl -n bookinfo apply -f istio-1.4.2/samples/bookinfo/networking/bookinfo-gateway.yaml
master:~ # kubectl -n bookinfo get gateway

master:~ # kubectl -n istio-system get services istio-ingressgateway -o wide
master:~ # kubectl -n istio-system get services istio-ingressgateway -o json

master:~ # export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
master:~ # export INGRESS_HOST=<master_ip>
master:~ # curl -s http://$INGRESS_HOST:$INGRESS_PORT/productpage
```
