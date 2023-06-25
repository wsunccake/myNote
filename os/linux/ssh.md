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

# sshd config
[server:~ ] # cat /etc/ssh/sshd_config
#LoginGraceTime 2m
PermitRootLogin no

# To disable tunneled clear text passwords, change to no here!
#PermitEmptyPasswords no
PasswordAuthentication no

# Change to no to disable s/key passwords
ChallengeResponseAuthentication no
...

# sshd service
[server:~ ] # systemctl restart sshd
```

---

## local forwarding

```
client          ssh tunnel          server
ssh client      ---------------     ssh server
                                    web server
localhost:8080                      localhost:80
  ^
  |
curl localhost:8080
```

```bash
[client:~ ] $ ssh -f -N -L 8080:localhost:80 <user>@<server ip>
[client:~ ] $ curl localhost:8080
# -f: background
# -N: do not execute remote command
# -L: local port forwarding
#     [local_addr:]local_port:remote_addr:remote_port [user@]sshd_addr
```

---

## local forwarding with bastion

```
                                +------ private network
client          ssh tunnel      |   bastion             server
ssh client      --------------- |   ssh server    ->    web server
localhost:8080                  +------                 0.0.0.0:80
  ^
  |
curl localhost:8080
```

```bash
[client:~ ] $ ssh -f -N -L 8080:<server>:80 <user>@<bastion ip>
[client:~ ] $ curl localhost:8080
```

---

## remote port forwarding

```
client          ssh tunnel          gateway
ssh client      ---------------     ssh server
web server
localhost:80                        0.0.0.0:8080
                                      ^
                                      |
                                    curl gateway:8080
```

```bash
[gateway:~ ] # sed -i '/AllowTcpForwarding/d' /etc/ssh/sshd_config
[gateway:~ ] # sed -i '/PermitOpen/d' /etc/ssh/sshd_config
[gateway:~ ] # sed -i '/GatewayPorts/d' /etc/ssh/sshd_config
[gateway:~ ] # echo 'GatewayPorts yes' >> /etc/ssh/sshd_config
[gateway:~ ] # systemctl restart sshd

[client:~ ] $ ssh -f -N -R 0.0.0.0:8080:localhost:80 <user>@<gateway ip>
[client:~ ] $ curl <gateway ip>:8080
# -R: remote port forwarding
#     [remote_addr:]remote_port:local_addr:local_port [user@]sshd_addr
```

---

## remote port forwarding from a private network

```
        private network ----+
server          client      |   ssh tunnel          gateway
web server  <-  ssh client  |   ---------------     ssh server
server:80               ----+                       0.0.0.0:8080
                                                      ^
                                                      |
                                                    curl gateway:8080
```

```bash
[gateway:~ ] # sed -i '/AllowTcpForwarding/d' /etc/ssh/sshd_config
[gateway:~ ] # sed -i '/PermitOpen/d' /etc/ssh/sshd_config
[gateway:~ ] # sed -i '/GatewayPorts/d' /etc/ssh/sshd_config
[gateway:~ ] # echo 'GatewayPorts yes' >> /etc/ssh/sshd_config
[gateway:~ ] # systemctl restart sshd

[client:~ ] $ ssh -f -N -R 0.0.0.0:8080:<server ip>:80 <user>@<gateway ip>
[client:~ ] $ curl <gateway ip>:8080
```

---

## dynamic forwarding

```
                                +------ private network
client          ssh tunnel      |   server
ssh client      --------------- |   ssh server
:port                           +-- sock proxy
```

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

---

## ref

[A Visual Guide to SSH Tunnels: Local and Remote Port Forwarding](https://iximiuz.com/en/posts/ssh-tunnels/?fbclid=IwAR1Cy0oJ09KopfTANtFbeoknuZ4fXRp-UeypuOewWRDU0ShYMf_bq6VeFq8)

[SSH Tunneling (Port Forwarding) 詳解](https://johnliu55.tw/ssh-tunnel.html)
