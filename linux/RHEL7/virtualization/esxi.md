# ESXi


```bash
~ # vmware -vl


```


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
```


---

## ovftool

```bash
linux:~ # ovftool --acceptAllEulas --noSSLVerify --diskMode=thin --name=<vm_name> --datastore=<data_store> --network=<vm_network> <vm>.ova vi://root:<password>@<esxi_ip>

# the provided manifest file is invalid
linux:~ # tar xf <xxx>.ova
linux:~ # ovftool <xxx>.ovf <new_xxx>.ova
```


---

## usage

```bash
esxi: ~ # vim-vmd vmsvc/getallvms
esxi: ~ # vim-vmd vmsvc/destroy <vm_id>
esxi: ~ # vim-vmd vmsvc/reload <vm_id>

esxi: ~ # vim-vmd vmsvc/power.shutdown <vm_id>
esxi: ~ # vim-vmd vmsvc/power.getstate <vm_id>
esxi: ~ # vim-vmd vmsvc/power.on <vm_id>


esxi: ~ # cat /vmfs/volumes/<data_store>/<vm_name>/<vm_name>.vmx


esxi: ~ # vim-cmd hostsvc/net/info | grep "mac ="
```
