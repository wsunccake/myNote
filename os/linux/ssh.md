# ssh

## introduction

從早期的 rsh (remote shell) 和 rlogin 到現在廣泛使用的 SSH (Secure Shell)，這段演進史是網路安全協定發展的縮影。這個過程清晰地反映出，隨著網際網路的普及和對安全性的需求日益增加，協定如何從簡單、不安全的設計，轉變為強大、加密的現代標準。

## history

1. 早期遠端登入工具：`rsh` 和 `rlogin`

   在網路發展的早期，rsh 和 rlogin 是非常流行的工具，主要用於在區域網路（LAN）內進行遠端登入和執行指令。

   - rsh（Remote Shell）：允許使用者在遠端伺服器上執行單一指令，並將結果返回到本機。
   - rlogin（Remote Login）：提供一個互動式的遠端終端機連線，讓使用者像直接坐在遠端伺服器前一樣操作。

   這兩個協定的主要優點是使用簡單、效率高。然而，它們存在著一個致命的缺陷：所有資料（包括使用者名稱和密碼）都是以明文形式在網路上傳輸。這意味著，任何能夠監聽網路流量的人，都能輕易地截取這些敏感資訊，造成嚴重的安全隱患。因此，rsh 和 rlogin 主要被限制在信任度較高的區域網路環境中使用，而不是廣泛的網際網路。

2. 通用遠端登入工具：`Telnet`

   Telnet 是比 rsh 和 rlogin 更通用的遠端登入協定，是當時網際網路上最常見的遠端終端機協定。它提供了一個標準化的方式來建立遠端會話，讓使用者可以跨越不同的作業系統和網路環境進行遠端操作。
   Telnet 的核心優勢在於它的通用性和跨平台能力。然而，和 rsh/rlogin 一樣，Telnet 的最大問題也是安全性不足。它同樣以明文傳輸所有資料，包括登入密碼和所有操作指令。在網際網路逐漸普及並充滿各種威脅的環境下，使用 Telnet 進行遠端管理變得極其危險。

3. 革命性的安全協定：`SSH`

   面對 rsh、rlogin 和 Telnet 的安全漏洞，SSH（Secure Shell）在 1995 年被開發出來，旨在徹底解決這些問題。SSH 的出現標誌著遠端管理協定的一次重大革命，它將加密引入了遠端連線。
   SSH 的主要特點包括：

   - 強大加密：SSH 會對所有傳輸的資料進行加密，包括使用者名稱、密碼、指令和所有傳輸內容。即使網路流量被截取，攻擊者也無法讀取其內容。
   - 身分驗證：SSH 提供了多種強大的身分驗證方法，例如基於密碼的驗證和更安全的公鑰/私鑰對驗證。公鑰驗證讓使用者無需在網路上傳輸密碼，大大降低了密碼被盜的風險。
   - 完整性保護：SSH 協定會檢查資料的完整性，確保傳輸過程中沒有被篡改。

   SSH 迅速取代了 rsh、rlogin 和 Telnet，成為了遠端管理、檔案傳輸（SFTP - SSH File Transfer Protocol）和埠轉發等用途的標準協定。它不僅提供了強大的安全性，還能實現更多功能，如在單一連線上建立多個通道、自動化腳本執行等。

- rsh/rlogin (1980 年代): 簡單、快速，但極不安全，僅限於信任環境。
- Telnet (1969 年): 通用、跨平台，但同樣極不安全，所有資料均為明文。
- SSH (1995 年): 安全、功能強大，採用加密技術，成為現代網路管理的標準。

---

## content

- [login with identity file / private key](#login-with-identity-file--private-key)
- [local forwarding](#local-forwarding)
- [local forwarding with bastion](#local-forwarding-with-bastion)
- [remote port forwarding](#remote-port-forwarding)
- [remote port forwarding from a private network](#remote-port-forwarding-from-a-private-network)
- [dynamic forwarding](#dynamic-forwarding)
- [keygen](#keygen)
- [other](#other)
  - [Too many authentication failures](#too-many-authentication-failures)
  - [Specified Configuration File](#specified-configuration-file)
  - [sign_and_send_pubkey: no mutual signature supported](#sign_and_send_pubkey-no-mutual-signature-supported)
- [ref](#ref)

---

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

### sign_and_send_pubkey: no mutual signature supported

```bash
[client:~ ] $ cat ~/.ssh/config
Host *
    PubkeyAcceptedKeyTypes=+ssh-rsa
    HostKeyAlgorithms=+ssh-rsa

[client:~ ] $ ssh <server_ip>
```

---

## ref

- [A Visual Guide to SSH Tunnels: Local and Remote Port Forwarding](https://iximiuz.com/en/posts/ssh-tunnels/?fbclid=IwAR1Cy0oJ09KopfTANtFbeoknuZ4fXRp-UeypuOewWRDU0ShYMf_bq6VeFq8)
- [SSH Tunneling (Port Forwarding) 詳解](https://johnliu55.tw/ssh-tunnel.html)
