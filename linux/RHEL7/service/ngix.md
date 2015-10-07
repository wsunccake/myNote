# ngix #


## Package ##

	RHEL:~# yum install epel-release
	RHEL:~# yum install nginx
	RHEL:~# systemctl start nginx
	RHEL:~# systemctl enable nginx


## Configuration ##

	RHEL:~ # vi /etc/nginx/nginx.conf
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
