# buildah

## install

```bash
[centos:~] # dnf install buildah

[centos:~] # buildah version
[centos:~] # buildah info
```

---

## build by dockerfile

```bash
[centos:~] # vi cat Dockerfile
FROM registry.access.redhat.com/ubi8-minimal
USER root
LABEL maintainer="John Doe"

RUN microdnf update --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos -y
RUN microdnf install --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos httpd -y
RUN rm -rf /var/cache/yum
RUN echo "The Web Server is Running" > /var/www/html/index.html

EXPOSE 80
CMD ["-D", "FOREGROUND"]
ENTRYPOINT ["/usr/sbin/httpd"]

[centos:~] # buildah bud -t webserver -f Dockerfile
[centos:~] # buildah images
[centos:~] # podman run -d -p 8080:80 webserver
[centos:~] # curl http://localhost:8080/index.html
```

---

## build by command

```bash
[centos:~] # buildah from registry.access.redhat.com/ubi8-minimal
[centos:~] # buildah images
[centos:~] # buildah containers
[centos:~] # buildah run --tty <container id> /bin/sh
sh-4.4# microdnf update --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos -y
sh-4.4# microdnf install --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos httpd -y
sh-4.4# rm -rf /var/cache/yum
sh-4.4# echo "The Web Server is Running" > /var/www/html/index.html
sh-4.4# exit
[centos:~] # buildah config --port 80 <image id>
[centos:~] # buildah config --cmd '-D FOREGROUND' <container id>
[centos:~] # buildah config --entrypoint '["/usr/sbin/httpd"]' <container id>
[centos:~] # buildah commit <container id> webserver
[centos:~] # curl http://localhost:8080/index.html
[centos:~] # buildah rm <container id>
```
