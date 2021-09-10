# cri-o

## prepare

```bash
# module
[ubuntu:~ ] # cat << EOF | tee /etc/modules-load.d/crio.conf
overlay
br_netfilter
EOF

[ubuntu:~ ] # modprobe overlay
[ubuntu:~ ] # modprobe br_netfilter

# sysctl param
[ubuntu:~ ] # cat << EOF | tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

[ubuntu:~ ] # sysctl --system
```


---

## install

```bash
# var
[ubuntu:~ ] # . /etc/os-release
[ubuntu:~ ] # OS=x${NAME}_${VERSION_ID}
[ubuntu:~ ] # CRIO_VERSION=1.21

# repo
[ubuntu:~ ] # echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
[ubuntu:~ ] # echo "deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$CRIO_VERSION/$OS/ /" > /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION.list
[ubuntu:~ ] # curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION/$OS/Release.key | apt-key add -
[ubuntu:~ ] # curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | apt-key add -

# package
[ubuntu:~ ] # apt-get update
[ubuntu:~ ] # apt-get install cri-o cri-o-runc cri-tools

# service
[ubuntu:~ ] # systemctl daemon-reload
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

[ubuntu:~ ] # vi /etc/crio/crio.conf
# cgroup driver
[crio.runtime]
conmon_cgroup = "pod"
cgroup_manager = "cgroupfs"

# private repo
insecure_registries = [
 "<private registry ip>:5000"
]
```


---

## usage

```bash
[ubuntu:~ ] # crictl help
[ubuntu:~ ] # crictl version
[ubuntu:~ ] # crictl info           # check status
[ubuntu:~ ] # ls /etc/cni/net.d/    # cni

# pod
[ubuntu:~ ] # crictl pods
[ubuntu:~ ] # crictl runp pod-config.json
[ubuntu:~ ] # crictl stopp <pod>
[ubuntu:~ ] # crictl rmp <pod>

# image
[ubuntu:~ ] # crictl images
[ubuntu:~ ] # crictl pull <image>
[ubuntu:~ ] # crictl rmi <image>

[ubuntu:~ ] # crictl iamgeinfo <image>
[ubuntu:~ ] # crictl inspecti <image>


# container
[ubuntu:~ ] # crictl ps [-a]
[ubuntu:~ ] # crictl create <pod> pod-config.json container-config.json
[ubuntu:~ ] # crictl start <container>
[ubuntu:~ ] # crictl stop <container>
[ubuntu:~ ] # crictl rm <container>

[ubuntu:~ ] # crictl exec -it <container> <command>
[ubuntu:~ ] # crictl logs <container>
[ubuntu:~ ] # crictl inspect <container>

# ie
[ubuntu:~ ] # cat > pod-config.json <<EOF 
{
  "metadata": {
    "name": "networking",
    "uid": "networking-pod-uid",
    "namespace": "default",
    "attempt": 1
  },
  "hostname": "networking",
  "port_mappings": [
    {
      "container_port": 80
    }
  ],
  "log_directory": "/tmp/net-pod",
  "linux": {}
}
EOF
[ubuntu:~ ] # crictl runp pod-config.json

[ubuntu:~ ] # crictl pull ngnix
[ubuntu:~ ] # cat > container-config.json <<EOF
{
  "metadata": {
    "name": "nginx-container",
    "attempt": 1
  },
  "image": {
    "image": "nginx"
  },
  "log_path": "nginx.log",
  "linux": {
    "security_context": {
      "namespace_options": {}
    }
  }
}
EOF
[ubuntu:~ ] # crictl 09f2f4ecf0afc pod-config.json container-config.json <<EOF
[ubuntu:~ ] # crictl ps -a
[ubuntu:~ ] # crictl start 92accc24c3449
[ubuntu:~ ] # crictl exec -it 92accc24c3449 hostname
[ubuntu:~ ] # crictl stop 92accc24c3449
[ubuntu:~ ] # crictl rm 92accc24c3449
```

---

## ref

[cri-o](https://cri-o.io/)
