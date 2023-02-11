# OpenSSL

## Intro

X.509 是 ITU-T 制定的公開憑證標準，其定義了憑證的架構與規範，詳記內容定義在 RFC 5280。

編碼方式:

    * DER: 以 Binary 存放
    * PEM: 以 ASCII(base64) 存放，第一行為 "---BEGIN", 結尾為"-----END"

DER/Distinguished Encoding Rules

PEM/Privacy Enhanced Mail

CER/CRT/Certificate

CSR/Certificate Signing Request

PFX/P12/Predecessor of PKCS#12

JKS/Java Key Storage

```bash
# show pem/der text
linux:~ # openssl x509 -in cert.pem -text -noout
linux:~ # openssl x509 -in cert.der -inform der -text -noout

# show crt text
linux:~ # openssl x509 -in cert.crt -outform der -out cert.der
linux:~ # openssl x509 -in cert.crt -inform der -outform pem -out cert.pem
```

副檔名(extension)：

    * CER/CRT: 兩種均常用於憑證 (不含私鑰)
    * KEY: 常用於公鑰與私鑰

```bash
linux:~ # openssl x509 -in cert.cer -text -noout
linux:~ # openssl x509 -in cert.crt -text -noout
```

---

## CA side

產生 CA

```bash
# create CA (Private Key & PEM)
ca:~ # openssl req -new -x509 -keyout ca.key -out ca.pem
ca:~ # openssl req -new -x509 -keyout ca.key -out ca.pem -config /etc/raddb/certs/ca.cnf
```

簽核 CSR

```bash
# sign CSR
ca:~ # openssl ca -in server.csr -out server.pem -cert ca.pem -keyfile ca.key
ca:~ # openssl ca -in server.csr -out server.pem -cert ca.pem -keyfile ca.key -config /etc/raddb/certs/ca.cnf
```

產生 PEM 表示簽核完成, 將 PEM 傳回 server/client

---

## Server/Client side

產生 CSR

```bash
# create Private Key & CSR
linux:~ # openssl req -new -key server.key -out server.csr
linux:~ # openssl req -new -key server.key -out server.csr -config /etc/raddb/certs/server.cnf
```

將 CSR 傳給 ca, 待 ca sign CSR 後會發 PEM, 收到 PEM 表示簽核完成

## Other

self-signed CA/自我簽核

```bash
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.pem
```

```bash
linux:~ # openssl req -newkey rsa:2048 -new -nodes -keyout my.key -out my.csr
linux:~ # openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
```

openssl pkcs12 -in for-iis.pfx -out for-iis.pem -nodes

grep -vE '^$|^\s+?#' eap.conf

## Ref

[Freeradius 與 OpenSSL 憑證](http://www.shunze.info/forum/thread.php?threadid=1899&boardid=3&sid=4c808a6520ccf3e4f1452780ce6734ad&page=1)

[The Most Common OpenSSL Commands](https://www.sslshopper.com/article-most-common-openssl-commands.html)
