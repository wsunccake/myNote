# repo

## local repo

```bash
# install package
debian:~ # apt-get install dpkg-dev
debian:~ # which dpkg-scanpackages

# create repo dir
debian:~ # mkdir -p /opt/repo/deb
debian:~ # cd /opt/repo/deb
debian:/opt/repo/dev # apt-get download wget

# generate meta data
debian:/opt/repo/dev # dpkg-scanpackages . /dev/null > Release
debian:/opt/repo/dev # dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz

# setup source
debian:~ # vi /etc/apt/sources.list
deb [trusted=yes] file:/opt/repo/deb ./
```


---

## mirror repo - debmirror

```bash
# install
debian:~ # apt-get install debmirror
debian:~ # which debmirror

# run
debian:~ # HOST=opensource.nchc.org.tw
debian:~ # METHOD=http # http, rsync, https
debian:/opt/mirror # debmirror \
  --arch=i386,amd64,armhf,arm64 \
  --dist=bullseye,buster,buster-updates,buster-backports\
  --di-arch=i386,amd64,armhf,arm64 \
  --di-dist=stable,unstable \
  --host=$HOST \
  --root=":debian" \
  --diff=none -p \
  --nosource \
  --method=$METHOD \
  --ignore-missing-release \
  --ignore-release-gpg \
  --ignore-small-errors \
  --section main,contrib,non-free \
  --i18n \
  --ignore-release-gpg /opt/mirror/debian
```


---

## mirror repo - apt-mirror

```bash
debian:~ # apt-get install apt-mirror
debian:~ # which apt-mirror
debian:~ # cat /etc/apt/mirror.list
set base_path    /var/spool/apt-mirror

set nthreads 20
set _tilde 0

deb-amd64 http://opensource.nchc.org.tw/debian bullseye main contrib non-free

debian:~ # apt-mirror
```

