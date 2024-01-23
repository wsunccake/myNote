```bash
linux:~ # docker pull ubuntu:24.04
linux:~ # docker run -itd --name u24 ubuntu:24.04
linux:~ # docker exec -it u24 bash --
u22:~ # apt update
u22:~ # apt install mysql-server

linux:~ # docker pull debian:bookworm
linux:~ # docker run -itd --name d12 debian:bookworm
linux:~ # docker exec -it d12 bash --
d12:~ # apt update
d12:~ # apt install mysql-server

linux:~ # docker pull fedora:39
linux:~ # docker run -itd --name f39 fedora:39
linux:~ # docker exec -it f39 bash --
f39:~ # dnf update
f39:~ # dnf install community-mysql-server | mariadb

# similar rhel9
linux:~ # docker pull rockylinux:9.3 | almalinux:9.3
linux:~ # docker run -itd --name ubi9 rockylinux:9.3
linux:~ # docker exec -it ubi9 bash --
ubi9:~ # dnf update
ubi9:~ # dnf install epel-release
ubi9:~ # dnf install mysql-server | mariadb-server
```
