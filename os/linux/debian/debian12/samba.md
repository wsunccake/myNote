# samba

## install

```bash
debian:~ # apt install samba smbclient cifs-utils
```

## mount

```bash
# method 1
debian:~ # smbclient [-U Aministrator[%password]] -L <samba_server>

# method 2
debian:~ # mount -t cifs [-o user=Administrator,pass='password'] //<samba_server>/folder /mnt/smb
```
