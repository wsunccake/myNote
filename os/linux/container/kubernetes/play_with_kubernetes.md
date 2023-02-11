# play with kubernetes

[play with kubernetes](http://labs.play-with-k8s.com/)

## master

```bash
master:~ # kubeadm init --apiserver-advertise-address $(hostname -i) --pod-network-cidr 10.5.0.0/16
master:~ # kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
```

---

## node

```bash
node:~ # kubeadm join 192.168.0.13:6443 --token wz0ps2.qipln143khf9hzmc --discovery-token-ca-cert-hash sha256:cdb430a0ff44a3099ee7e89734897d958e4ea3eb371cdecfd3c31e3f6dd7f6f5
```

---

## example

```bash
master:~ # kubectl get node
master:~ # kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/application/nginx-app.yaml

master:~ # kubectl get pod
master:~ # kubectl get deployment
master:~ # kubectl get service
master:~ # kubectl get endpoints -o wide
```
