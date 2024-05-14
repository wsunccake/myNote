# nginx

## install

```bash
# install
debian:~ # apt install nginx

# service
debian:~ # systemctl status nginx.service
debian:~ # systemctl enable nginx.service
debian:~ # systemctl start nginx.service

# test
debian:~ # curl http://localhost
```

---

## conf

```bash
debian:~ # cat /etc/nginx/nginx.conf

# default
debian:~ # grep -Ev '#|^$' /etc/nginx/sites-available/default
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name _;
	location / {
		try_files $uri $uri/ =404;
	}
}

debian:~ # vi /etc/nginx/sites-available/default
		try_files $uri $uri/ =404;
->
		autoindex on; # 瀏覽目錄

debian:~ # systemctl restart nginx.service
```
