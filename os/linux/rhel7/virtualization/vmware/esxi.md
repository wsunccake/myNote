# ESXi

```bash
~ # vmware -vl
```

http://<esxi_ip>/ui

---

## tip

```bash
# change prompt
esxi: ~ # echo 'PS1="\w # "' >> /etc/profile.local

# change password policy
esxi: ~ # vi /etc/pam.d/passwd

#password   requisite    /lib/security/$ISA/pam_passwdqc.so retry=3 min=disabled,disabled,disabled,7,7
#password   sufficient   /lib/security/$ISA/pam_unix.so use_authtok nullok shadow sha512
password   sufficient   /lib/security/$ISA/pam_unix.so nullok shadow sha512
password   required     /lib/security/$ISA/pam_deny.so

# ssh public key
esxi: ~ # cat /etc/ssh/keys-root/authorized_keys

# network
esxi: ~ # esxcli network nic list
esxi: ~ # esxcli network ip interface ipv4 get
```

---

## ovftool

```bash
# update ova
linux:~ # ovftool --acceptAllEulas --noSSLVerify --diskMode=thin --name=<vm_name> --datastore=<data_store> --network=<vm_network> <vm>.ova vi://root:<password>@<esxi_ip>

# the provided manifest file is invalid
linux:~ # tar xf <xxx>.ova
linux:~ # ovftool <xxx>.ovf <new_xxx>.ova
```

---

## usage

```bash
# list vm
esxi:~ # vim-cmd vmsvc/getallvms

# power state
esxi:~ # vim-cmd vmsvc/power.getstate <vm_id>

# update vm config
esxi:~ # ls /vmfs/volumes/<data_store>/<vm_name>
esxi:~ # vi /vmfs/volumes/<data_store>/<vm_name>/<vm_name>.vmx
# setup cpu
numvcpus = "1"
sched.cpu.affinity = "all"
sched.cpu.htsharing = "any"

# setup mem
sched.mem.min = "1024"
sched.mem.affinity = "all"
sched.mem.shares = "normal"

# setup nic
ethernet0.address = "00:11:22:33:44:55"
ethernet0.checkMACAddress = "FALSE"
ethernet0.addressType = "static"         # generated, vpx, static
# ethernet0.generatedAddress

# enable svm or vmx
vhv.enable = "TRUE"

# lauch vm
esxi:~ # vim-cmd vmsvc/power.on <vm_id>

# delete vm
esxi:~ # vim-cmd vmsvc/power.off <vm_id>
esxi:~ # vim-cmd vmsvc/destroy <vm_id>
esxi:~ # ls /vmfs/volumes/<data_store>/<vm_name>

# other
esxi: ~ # vim-cmd hostsvc/net/info | grep "mac ="
```

---

## clone vm

```bash
esxi:~ # cd /vmfs/volumes/datastore1
esxi:~/vmfs/volumes/datastore1 # mkdir new_vm
esxi:~/vmfs/volumes/datastore1 # vmkfstools -i ./origin/origin.vmdk ./new_vm/new_vm.vmdk -d thin -a buslogic
```

```text
Click "Create / Register VM" show "New virtual machine" on web ui

1. Select create type => Create a new virtual machine

...

4 Customize settings  => Add hard disk => Existing hard disk
(Select new_vm.vmdk)
```
