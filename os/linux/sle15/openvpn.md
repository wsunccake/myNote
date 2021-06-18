# openvpn

## install

```bash
server:~ # zypper in openvpn
```


---

## openssl

ca: Certification Authority

key: PRIVATE KEY

crt: CERTIFICATE

csr: CERTIFICATE REQUEST

pem: Privacy Enhanced Mail

```bash
# openssl command
sle:~ # openssl help
sle:~ # openssl rsa -help
sle:~ # man openssl rsa

# view/check
sle:~ # openssl req -text -noout [-verify] -in <csr>
sle:~ # openssl x509 -text -noout -in <crt>
sle:~ # openssl rsa -check -in <key>

# gen key
sle:~ # openssl genrsa -out <key>
sle:~ # openssl req \                    # gen key and csr
  [-nodes] [-utf8] [-days 3650] \
  -newkey rsa:2048 -keyout <key> \
  -new -out <csr>
sle:~ # openssl req \                    # gen key and crt
  [-nodes] [-utf8] [-days 3650] \
  -newkey rsa:2048 -keyout <key> \
  -new -x509 -out <crt>

# with key
sle:~ # openssl req \                    # gen csr with key
  [-nodes] [-utf8] [-days 3650] \
  -key <key> \
  -new -out <csr>
sle:~ # openssl req \                    # gen crt with key
  [-nodes] [-utf8] [-days 3650] \
  -key <key> \
  -new -x509 -out <crt>

# sign csr
sle~: # cat /etc/ssl/openssl.cnf
[ CA_default ]
dir             = ./demoCA
...

sle:~ # mkdir -p demoCA/{private,newcerts}
sle:~ # touch demoCA/index.txt
sle:~ # openssl rand -hex -out demoCA/serial 16
sle:~ # openssl ca [-utf8] [-days 3650] \
  -in <csr> -out <pem> \
  -cert <ca crt> -keyfile <ca key>

# gen Diffie-Hellman
sle:~ # openssl dhparam -out dh2048.pem 2048
```


---

## easy-rsa

```bash
sle:~ # zypper in rpm-build
sle:~ # rpmbuild --rebuild easy-rsa-3.0.8-33.1.noarch.rpm
sle:~ # zypper in /usr/src/packages/RPMS/noarch/easy-rsa-3.0.8-33.1.noarch.rpm

#
sle:~ # easyrsa init-pki
sle:~ # tree pki/
pki/
├── openssl-easyrsa.cnf
├── private
├── reqs
└── safessl-easyrsa.cnf

sle:~ # easyrsa gen-dh
sle:~ # tree pki/
├── dh.pem
├── openssl-easyrsa.cnf
├── private
├── reqs
└── safessl-easyrsa.cnf

sle:~ # easyrsa build-ca nopass
sle:~ # tree pki/
pki/
├── ca.crt
├── certs_by_serial
├── dh.pem
├── index.txt
├── index.txt.attr
├── issued
├── openssl-easyrsa.cnf
├── private
│   └── ca.key
├── renewed
│   ├── certs_by_serial
│   ├── private_by_serial
│   └── reqs_by_serial
├── reqs
├── revoked
│   ├── certs_by_serial
│   ├── private_by_serial
│   └── reqs_by_serial
├── safessl-easyrsa.cnf
└── serial

sle:~ # easyrsa build-server-full server nopass
sle:~ # tree pki/
pki/
├── ca.crt
├── certs_by_serial
│   └── ED07AF9875016A1942359CAFB967AD2D.pem
├── dh.pem
├── index.txt
├── index.txt.attr
├── index.txt.attr.old
├── index.txt.old
├── issued
│   └── server.crt
├── openssl-easyrsa.cnf
├── private
│   ├── ca.key
│   └── server.key
├── renewed
│   ├── certs_by_serial
│   ├── private_by_serial
│   └── reqs_by_serial
├── reqs
│   └── server.req
├── revoked
│   ├── certs_by_serial
│   ├── private_by_serial
│   └── reqs_by_serial
├── safessl-easyrsa.cnf
├── serial
└── serial.old
```


---

## server


```bash
# gen cert
server:~ # mkdir -p /etc/openvpn/easyrsa
server:~ # cd /etc/openvpn/easyrsa
server:/etc/openvpn/easyrsa # easyrsa init-pki
server:/etc/openvpn/easyrsa # easyrsa gen-dh
server:/etc/openvpn/easyrsa # easyrsa build-ca nopass
server:/etc/openvpn/easyrsa # easyrsa build-server-full server nopass

server:/etc/openvpn # cp easyrsa/pki/ca.crt .
server:/etc/openvpn # cp easyrsa/pki/dh.pem .
server:/etc/openvpn # cp easyrsa/pki/private/server.key .
server:/etc/openvpn # cp easyrsa/pki/issued/server.crt .

# config
server:~ # cp /usr/share/doc/packages/openvpn/sample-config-files/server.conf /etc/openvpn/.
server:~ # grep -vE '^#|^$|^;' /etc/openvpn/server.conf
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key  # This file should be kept secret
dh dh2048.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
keepalive 10 120
tls-auth ta.key 0 # This file is secret
cipher AES-256-CBC
persist-key
persist-tun
status openvpn-status.log
verb 3
explicit-exit-notify 1


server:~ # vi /etc/openvpn/server.conf
port 1194
proto tcp
dev tun

# security
ca ca.crt
cert server.crt
key server.key

# ns-cert-type server 
remote-cert-tls client 
dh   server/dh.pem

# ns-cert-type server
server 192.168.1.0 255.255.255.0 
ifconfig-pool-persist /var/run/openvpn/ipp.txt

# privilege
user nobody
group nobody

# other
keepalive 10 120
comp-lzo
persist-key
persist-tun
status      /var/log/openvpn-status.tun0.log 
log-append  /var/log/openvpn-server.log 
verb 4

# service
server:~ # systemctl enable openvpn@server.service   # openvpn@server.service <--> /etc/openvpn/server.conf
server:~ # systemctl start openvpn@server.service
server:~ # systemctl status openvpn@server.service

# nic
server:~ # ip link show dev tun0
server:~ # wicked show tun0

# firewall
server:~ # firewall-cmd --list-services
server:~ # firewall-cmd --add-service openvpn
server:~ # firewall-cmd --permanent --add-service openvpn
```


---

## client

