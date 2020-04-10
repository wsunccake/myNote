```bash
SLES:/etc/ssl # rm -rf servercerts/
SLES:/etc/ssl # mkdir /etc/ssl/demoCA
SLES:/etc/ssl # touch /etc/ssl/demoCA/index.txt
SLES:/etc/ssl # echo '00000000' >> /etc/ssl/demoCA/serial
SLES:/etc/ssl # openssl req -new -x509 -extensions v3_ca -keyout /etc/ssl/private/cakey.pem -out /etc/ssl/cacert.pem -days 1095


SLES:/etc/ssl # mkdir -p servercerts
SLES:/etc/ssl # openssl req -new -nodes -out /etc/ssl/servercerts/servercert.csr -keyout /etc/ssl/servercerts/serverkey.pem


SLES:/etc/ssl # openssl ca -cert /etc/ssl/cacert.pem -keyfile /etc/ssl/private/cakey.pem -out /etc/ssl/servercerts/servercert.pem -outdir /etc/ssl/servercerts -infiles /etc/ssl/servercerts/servercert.csr
```


## certificate

```bash
# generate cert
SLES:~ # openssl req -new > my.csr
SLES:~ # openssl rsa -in privkey.pem -out my.key
SLES:~ # openssl x509 -in my.csr -req -signkey my.key -days 300 -out my.cert

# copy to ssl
SLES:~ # cp my.cert /etc/ssl/certs/server.crt
SLES:~ # cp my.key /etc/ssl/private/server.key
```