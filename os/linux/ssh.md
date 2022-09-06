# ssh


## login with identity file / private key


```bash
# keygen
[client:~ ] $ ssh-keygen
[client:~ ] $ ls ~/.ssh

# copy public key by command
[client:~ ] $ ssh-copy-id [<user>@]<server>

# copy public key by
[server:~ ] $ mkdir -p ~/.ssh
[server:~ ] $ cat <public key> >> ~/.ssh/authorized_keys
```


---

## forwarding


```bash
[client:~ ] $ ssh -D<port> <server>
```


---

## keygen

```bash
[client:~ ] $ ssh-keygen -f <private key>
cat <private key>
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----


[client:~ ] $ ssh-keygen -f <private key> -m pem
cat <private key>
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```


---

## other

### Too many authentication failures

```bash
[client:~ ] $ ssh -o IdentitiesOnly=yes <server_ip>
Received disconnect from <server_ip> port 22:2: Too many authentication failures
Disconnected from <server_ip> port 22

[client:~ ] $ ssh -o IdentitiesOnly=yes <server_ip>
```


### Specified Configuration File

```bash
[client:~ ] $ cat ~/.ssh/config
...

Match all
Include  ~/.ssh/host.d/*.conf

[client:~ ] $ cat ~/.ssh/host.d/group1.conf
Host host1
    HostName     192.168.10.11
    User         user
```
