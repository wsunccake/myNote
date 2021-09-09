# cri-o

## install

```bash
# var
[ubuntu:~ ] # . /etc/os-release
[ubuntu:~ ] # OS=x${NAME}_${VERSION_ID}
[ubuntu:~ ] # CRIO_VERSION=1.22

# repo
[ubuntu:~ ] # echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
[ubuntu:~ ] # echo "deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$CRIO_VERSION/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION.list
[ubuntu:~ ] # curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION/$OS/Release.key | apt-key add -
[ubuntu:~ ] # curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | apt-key add -

# package
[ubuntu:~ ] # apt-get update
[ubuntu:~ ] # apt-get install cri-o cri-o-runc cri-tools

# service
[ubuntu:~ ] # systemctl start crio
[ubuntu:~ ] # systemctl enable crio
[ubuntu:~ ] # systemctl status crio
```


---

## config

```bash
[ubuntu:~ ] # tree /etc/crio/
/etc/crio/
├── crio.conf
└── crio.conf.d
    └── 01-crio-runc.conf

[ubuntu:~ ] # cat /etc/crictl.yaml 
runtime-endpoint: "unix:///var/run/crio/crio.sock"
timeout: 0
debug: false

# for debug
[ubuntu:~ ] # cat /etc/crictl.yaml 
runtime-endpoint: "unix:///var/run/crio/crio.sock"
timeout: 10
debug: true

[ubuntu:~ ] # vi /etc/crio/
# private repo
insecure_registries = [
 "<private registry ip>:5000"
]
```


---

## usage

```bash
[ubuntu:~ ] # crictl pull <image>
[ubuntu:~ ] # crictl images

[ubuntu:~ ] # crictl ps
[ubuntu:~ ] # crictl pods
```

```bash
[ubuntu:~ ] # vi pod-config.json
{
    "metadata": {
        "name": "nginx-sandbox",
        "namespace": "default",
        "attempt": 1,
        "uid": "hdishd83djaidwnduwk28bcsb"
    },
    "logDirectory": "/tmp",
    "linux": {
    }
}
[ubuntu:~ ] # crictl runp pod-config.json

[ubuntu:~ ] # crictl pull busybox
[ubuntu:~ ] # vi container-config.json
{
  "metadata": {
      "name": "busybox"
  },
  "image":{
      "image": "busybox"
  },
  "command": [
      "top"
  ],
  "log_path":"busybox.log",
  "linux": {
  }
}

```

---

## ref

[cri-o](https://cri-o.io/)
