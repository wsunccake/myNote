k0:/etc/ssl # rm -rf servercerts/
k0:/etc/ssl # mkdir /etc/ssl/demoCA
k0:/etc/ssl # touch /etc/ssl/demoCA/index.txt
k0:/etc/ssl # echo '00000000' >> /etc/ssl/demoCA/serial
k0:/etc/ssl # openssl req -new -x509 -extensions v3_ca -keyout /etc/ssl/private/cakey.pem -out /etc/ssl/cacert.pem -days 1095


k0:/etc/ssl # mkdir -p servercerts
k0:/etc/ssl # openssl req -new -nodes -out /etc/ssl/servercerts/servercert.csr -keyout /etc/ssl/servercerts/serverkey.pem


k0:/etc/ssl # openssl ca -cert /etc/ssl/cacert.pem -keyfile /etc/ssl/private/cakey.pem -out /etc/ssl/servercerts/servercert.pem -outdir /etc/ssl/servercerts -infiles /etc/ssl/servercerts/servercert.csr

