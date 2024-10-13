# pure-ftpd


## install

```
linux:~ # yum install -y pure-ftpd
```


---

## config

```
linux:~ # useradd -m <local_user>

# create user
# /etc/pureftpd.passwd
linux:~ # pure-pw useradd <ftp_user> -u <local_user> -g <local_group> -d <local_folder>

# update user
linux:~ # pure-pw usermod <ftp_user> -u <local_user> -g <local_group> -d <local_folder>

# generate db
# /etc/pureftpd.pdb
linux:~ # pure-pw mkdb

# update config
linux:~ # vi /etc/pure-ftpd/pure-ftpd.conf
PureDB                        /etc/pure-ftpd/pureftpd.pdb
```


---

## test

```
# upload file
linux:~ # curl --ftp-create-dirs -T <upload_file> ftp://snapshot:snapshot@<host>/<dir>/<file>

# download file
linux:~ # curl ftp://snapshot:snapshot@<host>/<dir>/<file> -o <download_file>
```
