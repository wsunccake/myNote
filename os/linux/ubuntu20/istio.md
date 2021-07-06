# istio

## install

### minikube

install [minikube](./minikube.md)

```bash
[ubuntu:~ ] $ minikube status
[ubuntu:~ ] $ minikube delete --all
[ubuntu:~ ] $ minikube config set driver kvm2
[ubuntu:~ ] $ minikube start --memory=16384 --cpus=4 --kubernetes-version=v1.20.2
[ubuntu:~ ] $ minikube tunnel --cleanup
```


### istio

```bash
[ubuntu:~ ] $ curl -L https://istio.io/downloadIstio | sh -
[ubuntu:~ ] $ curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.10.0 TARGET_ARCH=x86_64 sh -
[ubuntu:~ ] $ export PATH=$HOME/istio-1.10.0/bin:$PATH
[ubuntu:~ ] $ istioctl install --set profile=demo -y

[ubuntu:~ ] $ kubectl label namespace default istio-injection=enabled   # automatic sidecar injection
[ubuntu:~ ] $ kubectl describe namespace default
[ubuntu:~ ] $ kubectl label namespace default istio-injection-          # remove sidecar injection
```


---

## command

### istio

```bash
[ubuntu:~ ] $ istioctl --help

[ubuntu:~ ] $ istioctl profile list
[ubuntu:~ ] $ istioctl profile dump demo
[ubuntu:~ ] $ istioctl profile dump --config-path components.pilot demo
[ubuntu:~ ] $ istioctl profile diff default demo
[ubuntu:~ ] $ istioctl uninstall --purge
```


### kubectl

```bash
[ubuntu:~ ] $ kubectl --help
[ubuntu:~ ] $ kubectl api-resources
[ubuntu:~ ] $ kubectl api-versions

# default
[ubuntu:~ ] $ kubectl get nodes|no -A -o wide
[ubuntu:~ ] $ kubectl get pods|po -A -o wide
[ubuntu:~ ] $ kubectl get deployments|deploy -A -o wide
[ubuntu:~ ] $ kubectl get services|svc -A -o wide
[ubuntu:~ ] $ kubectl get all -A -o wide

# for istio
[ubuntu:~ ] $ kubectl get gateways|gw -A -o wide
[ubuntu:~ ] $ kubectl get virtualservices|vs -A -o wide
```

```bash
[ubuntu:~ ] $ istioctl proxy-status|ps
[ubuntu:~ ] $ istioctl proxy-status <pod>

[ubuntu:~ ] $ istioctl proxy-config|pc all <pod>
[ubuntu:~ ] $ istioctl proxy-config|pc cluster <pod>

[ubuntu:~ ] $ istioctl analyze

[ubuntu:~ ] $ kubectl get po -n istio-system
```


---

## helloworld

### without istio

```bash
# start service
[ubuntu:~ ] $ cd istio-1.10.0/samples/helloworld
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml

# start service by lable
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml -l service=helloworld
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml -l version=v1
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml -l version=v2

# hpa
[ubuntu:~ ] $ kubectl autoscale deployment helloworld-v1 --cpu-percent=50 --min=1 --max=10
[ubuntu:~ ] $ kubectl autoscale deployment helloworld-v2 --cpu-percent=50 --min=1 --max=10
[ubuntu:~ ] $ kubectl get hpa

# test
[ubuntu:~ ] $ kubectl get svc helloworld -o wide
[ubuntu:~ ] $ kubectl get svc helloworld -o jsonpath='{.spec.clusterIP}'
[ubuntu:~ ] $ export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
[ubuntu:~ ] $ curl http://<cluster ip or external ip of service>:5000/hello
[ubuntu:~ ] $ seq 10 | xargs -i curl http://<cluster ip or external ip of service>:5000/hello
```


### with istio

```bash
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld-gateway.yaml

# test
[ubuntu:~ ] $ kubectl -n istio-system get svc istio-ingressgateway -o wide
[ubuntu:~ ] $ kubectl -n istio-system get svc istio-ingressgateway helloworld -o jsonpath='{.spec.clusterIP}'
[ubuntu:~ ] $ curl http://<cluster ip or external ip of service>:80/hello
[ubuntu:~ ] $ seq 10 | xargs -i curl http://<cluster ip or external ip of service>:80/hello
```


### with istio canary

```bash
[ubuntu:~ ] $ kubectl delete -f istio-1.10.0/samples/helloworld/helloworld-gateway.yaml
[ubuntu:~ ] $ kubectl apply -f - << EOF
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: helloworld-gateway
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
---

apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: helloworld
spec:
  hosts:
  - "*"
  gateways:
  - helloworld-gateway
  http:
  - match:
    - uri:
        exact: /hello
    route:
    - destination:
        host: helloworld
        subset: v1
        port:
          number: 5000
      weight: 10
    - destination:
        host: helloworld
        subset: v2
        port:
          number: 5000
      weight: 90
---

apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: helloworld
spec:
  host: helloworld
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
EOF

[ubuntu:~ ] $ seq 10 | xargs -i curl http://<cluster ip or external ip of service>:80/hello
```


### env var

```bash
[ubuntu:~ ] $ kubectl -n istio-system get svc istio-ingressgateway

# for external load balancer
[ubuntu:~ ] $ export INGRESS_HOST=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
[ubuntu:~ ] $ export INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
[ubuntu:~ ] $ export SECURE_INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].port}')
[ubuntu:~ ] $ export TCP_INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="tcp")].port}')

# for minikube
[ubuntu:~ ] $ minikube service istio-ingressgateway -n istio-system
[ubuntu:~ ] $ export INGRESS_HOST=$(minikube ip)
```

### clean

```bash
[ubuntu:~ ] $ kubectl delete -f istio-1.10.0/samples/helloworld/helloworld.yaml
[ubuntu:~ ] $ kubectl delete -f istio-1.10.0/samples/helloworld/helloworld-gateway.yaml
```


---

## httpbin

```bash
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/httpbin/httpbin.yaml
[ubuntu:~ ] $ curl -s -I -HHost:httpbin.example.com http://<cluster ip or external ip of service>:8000/status/200
[ubuntu:~ ] $ curl -s -I -HHost:httpbin.example.com http://<cluster ip or external ip of service>:8000/headers
[ubuntu:~ ] $ curl -s http://<cluster ip or external ip of service>:8000/status/200
[ubuntu:~ ] $ curl -s http://<cluster ip or external ip of service>:8000/headers

[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/httpbin/httpbin-gateway.yaml
[ubuntu:~ ] $ curl -s -I -HHost:httpbin.example.com http://://$INGRESS_HOST:$INGRESS_PORT/status/200
[ubuntu:~ ] $ curl -s -I -HHost:httpbin.example.com http://://$INGRESS_HOST:$INGRESS_PORT/headers
[ubuntu:~ ] $ curl -s http://$INGRESS_HOST:$INGRESS_PORT/status/200
[ubuntu:~ ] $ curl -s http://://$INGRESS_HOST:$INGRESS_PORT/headers
```


---

## bookinfo

### without istio

```bash
[ubuntu:~ ] $ kubectl apply -f <(istioctl kube-inject -f istio-1.10.0/samples/bookinfo/platform/kube/bookinfo.yaml)

[ubuntu:~ ] $ kubectl get po
[ubuntu:~ ] $ kubectl get deploy
[ubuntu:~ ] $ kubectl get svc

[ubuntu:~ ] $ kubectl get pod -l app=ratings
[ubuntu:~ ] $ kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}'
[ubuntu:~ ] $ kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"

# test
[ubuntu:~ ] $ curl http://<cluster ip or external ip of productpage>:9080/productpage
[ubuntu:~ ] $ curl http://<cluster ip or external ip of productpage>:9080
```


### with istio

```bash
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/bookinfo/networking/bookinfo-gateway.yaml
[ubuntu:~ ] $ kubectl get gw

# test
[ubuntu:~ ] $ curl http://$INGRESS_HOST:$INGRESS_PORT/productpage
```


### prometheus

```bash
[ubuntu:~ ] $ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/prometheus.yaml
[ubuntu:~ ] $ kubectl -n istio-system get svc prometheus
[ubuntu:~ ] $ istioctl dashboard prometheus

# test
[ubuntu:~ ] $ watch curl http://<cluster ip or external ip of productpage>:9080/productpage
[ubuntu:~ ] $ curl http://<cluster ip or external ip of prometheus>:9090
```

istio_requests_total

istio_requests_total{destination_service="productpage.default.svc.cluster.local"}

istio_requests_total{destination_service="reviews.default.svc.cluster.local", destination_version="v3"}

rate(istio_requests_total{destination_service=~"productpage.*", response_code="200"}[5m])


### grafana

```bash
[ubuntu:~ ] $ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/grafana.yaml
[ubuntu:~ ] $ kubectl -n istio-system get svc grafana

# test
[ubuntu:~ ] $ watch curl http://<cluster ip or external ip of productpage>:9080/productpage
[ubuntu:~ ] $ curl http://<cluster ip or external ip of service>:3000
```


### jaeger

```bash
[ubuntu:~ ] $ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/jaeger.yaml
[ubuntu:~ ] $ kubectl -n istio-system get svc tracing zipkin jaeger-collector
[ubuntu:~ ] $ istioctl dashboard jaeger

# test
[ubuntu:~ ] $ watch curl http://<cluster ip or external ip of productpage>:9080/productpage
[ubuntu:~ ] $ curl http://<cluster ip or external ip of tracing>:80
```


### kiali

```bash
# for bash
[ubuntu:~ ] $ KIALI_USERNAME=$(read -p 'Kiali Username: ' uval && echo -n $uval | base64)
[ubuntu:~ ] $ KIALI_PASSPHRASE=$(read -sp 'Kiali Passphrase: ' pval && echo -n $pval | base64)

# for zsh
[ubuntu:~ ] $ KIALI_USERNAME=$(read '?Kiali Username: ' uval && echo -n $uval | base64)
[ubuntu:~ ] $ KIALI_PASSPHRASE=$(read -s "?Kiali Passphrase: " pval && echo -n $pval | base64)

[ubuntu:~ ] $ NAMESPACE=istio-system
[ubuntu:~ ] $ kubectl create namespace $NAMESPACE
[ubuntu:~ ] $ cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: kiali
  namespace: $NAMESPACE
  labels:
    app: kiali
type: Opaque
data:
  username: $KIALI_USERNAME
  passphrase: $KIALI_PASSPHRASE
EOF

[ubuntu:~ ] $ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/kiali.yaml
[ubuntu:~ ] $ kubectl -n istio-system get svc kiali

# test
[ubuntu:~ ] $ watch curl http://<cluster ip or external ip of productpage>:9080/productpage
[ubuntu:~ ] $ curl http://<cluster ip or external ip of kiali>:20001
```


---
