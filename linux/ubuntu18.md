# ubuntu 18 lts


## apt

```bash
ubuntu:~ # apt update
ubuntu:~ # apt search <pkg>
ubuntu:~ # apt install <pkg>

ubuntu:~ # apt install vim curl
ubuntu:~ # apt install python3-pip
```


---

## ssh

```bash
ubuntu:~ # apt install openssh-server
ubuntu:~ # systemctl enable sshd
ubuntu:~ # systemctl start sshd
```

---

## nginx

```bash
ubuntu:~ # apt install nginx
ubuntu:~ # systemctl enable nginx
ubuntu:~ # systemctl start nginx

ubuntu:~ # vi /etc/nginx/conf/dir.conf
server {
        listen 8080;
        listen [::]:8080;

        server_name .example.com;

        root /tmp;

        location / {
                autoindex on;
        }
}

curl http://localhost:8080/
```


