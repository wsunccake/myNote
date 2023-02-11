# metal lb

## install

```bash
[master:~ ] # kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/namespace.yaml
[master:~ ] # kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/metallb.yaml

[master:~ ] # kubectl -n metallb-system get all
```

---

## config

```bash
[master:~ ] # cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.0.200-192.168.0.220
EOF

[master:~ ] # kubectl -n metallb-system get cm
[master:~ ] # kubectl -n metallb-system describe cm/config
```

---

## ref

[METALLB](https://metallb.universe.tf/)
