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
[ubuntu:~ ] $ kubectl label namespace default istio-injection=enabled
```


---

## command

### istio

```bash
[ubuntu:~ ] $ istioctl profile list
[ubuntu:~ ] $ istioctl profile dump demo
[ubuntu:~ ] $ istioctl profile dump --config-path components.pilot demo
[ubuntu:~ ] $ istioctl profile diff default demo
[ubuntu:~ ] $ istioctl x uninstall --purge
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

#  for istio
[ubuntu:~ ] $ kubectl get gateways|gw -A -o wide
[ubuntu:~ ] $ kubectl get virtualservices|vs -A -o wide
```

```bash
istioctl proxy-status
kubectl get po -n istio-system
```

---

## helloworld

### without istio

```bash
[ubuntu:~ ] $ cd istio-1.10.0/samples/helloworld
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml

# same above 
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml -l service=helloworld
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml -l version=v1
[ubuntu:~ ] $ kubectl apply -f istio-1.10.0/samples/helloworld/helloworld.yaml -l version=v2

# test
[ubuntu:~ ] $ kubectl get svc helloworld -o wide
[ubuntu:~ ] $ kubectl get svc helloworld -o jsonpath='{.spec.clusterIP}'
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


### var

```bash
[ubuntu:~ ] $ export INGRESS_HOST=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
[ubuntu:~ ] $ export INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
[ubuntu:~ ] $ export SECURE_INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].port}')
[ubuntu:~ ] $ export TCP_INGRESS_PORT=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="tcp")].port}')
```

### clean

```bash
[ubuntu:~ ] $ kubectl delete -f istio-1.10.0/samples/helloworld/helloworld.yaml
[ubuntu:~ ] $ kubectl delete -f istio-1.10.0/samples/helloworld/helloworld-gateway.yaml
```


---

## bookinfo

```bash
[ubuntu:~ ] $ kubectl apply -f <(istioctl kube-inject -f istio-1.10.0/samples/bookinfo/platform/kube/bookinfo.yaml)

[ubuntu:~ ] $ kubectl get po
[ubuntu:~ ] $ kubectl get deploy
[ubuntu:~ ] $ kubectl get svc

[ubuntu:~ ] $ kubectl get pod -l app=ratings
[ubuntu:~ ] $ kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}'
[ubuntu:~ ] $ kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
```