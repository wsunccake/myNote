# nginx #


## Package ##

	RHEL:~# yum install epel-release
	RHEL:~# yum install nginx
	RHEL:~# systemctl start nginx
	RHEL:~# systemctl enable nginx


## Configuration ##

```bash
RHEL:~ # vi /etc/nginx/nginx.conf
...
http {
	...

	server {
		listen       80 default_server;
		listen       [::]:80 default_server;
		server_name  _;
		root         /usr/share/nginx/html;
	
		...

		location / {
			autoindex on; # 新增此行, 可以瀏覽目錄
		}
		...
	}
```

`proxy forwarding`

```bash
server {
    listen       80;
    server_name  jenkins.mydomain;

    location / {
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;

        proxy_pass http://192.168.0.1:8080;
        # proxy_redirect      http://localhost:8080 https://jenkins.domain.com;
    }
}
```

`HA`

```bash
upstream 192.168.0.2 {
			server 172.19.19.11:80;
			server 172.19.19.12:80;
			server 172.19.19.13:80;
}

server {
	server_name 192.168.0.2;
	listen 80 ;
	access_log /var/log/nginx/access.log vhost;
	location / {
		proxy_pass http://192.168.0.2;
	}
}

```