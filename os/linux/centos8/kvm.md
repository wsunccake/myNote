# kvm

## install

```bash
[centos:~ ] # grep -E 'svm|vmx' /proc/cpuinfo
[centos:~ ] # lsmod | grep kvm

[centos:~ ] # dnf module install virt 
[centos:~ ] # dnf install virt-install virt-viewer
[centos:~ ] # virt-host-validate

[centos:~ ] # systemctl enable libvirtd --now
[centos:~ ] # systemctl restart libvirtd
[centos:~ ] # systemctl status libvirtd
```


---

## cockpit - machine

```bash
[centos:~ ] # dnf install cockpit cockpit-machines

[centos:~ ] # systemctl enable cockpit --now
[centos:~ ] # systemctl restart cockpit
[centos:~ ] # systemctl status cockpit

[centos:~ ] # firewall-cmd --add-service=cockpit --permanent
[centos:~ ] # firewall-cmd --reload
```

https://<host>:9090/


---

##

```bash
[centos:~ ] # cat /sys/module/kvm_intel/parameters/nested
[centos:~ ] # lsmod | grep kvm

# for intel
[centos:~ ] # modprobe -r kvm_intel
[centos:~ ] # modprobe kvm_intel nested=1
[centos:~ ] # echo "options kvm_intel nested=1" > /etc/modprobe.d/kvm.conf

# for amd
[centos:~ ] # modprobe -r kvm_amd
[centos:~ ] # modprobe kvm_amd nested=1
[centos:~ ] # echo "options kvm_amd nested=1" > /etc/modprobe.d/kvm.conf
```
