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

# ulimit ssh
ubuntu:~ # vi /etc/systemd/logind.conf
UserTasksMax=infinity

ubuntu:~ # vi /lib/systemd/system/ssh.service
[Service]
TasksMax=infinity

ubuntu:~ # systemctl daemon-reload
ubuntu:~ # systemctl restart ssh

ubuntu:~ # systemctl show --property DefaultTasksMax
ubuntu:~ # systemctl show -a | grep -i task
ubuntu:~ # systemctl status ssh  |grep -e Tasks
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

ubuntu:~ # curl http://localhost:8080/
```

---

## docker

```bash
ubuntu:~ # apt install docker.io
ubuntu:~ # systemctl enable docker --now

ubuntu:~ # curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
ubuntu:~ # chmod +x /usr/local/bin/docker-compose
```
