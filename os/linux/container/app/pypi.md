# PyPI server

## install

```bash
# pull image
[linux:~ ] # docker pull pypiserver/pypiserver


# run container
[linux:~ ] # export PACKAGES=<path>
[linux:~ ] # mkdir -p PACKAGES
[linux:~ ] # docker run -d \
  -v $PACKAGES:/data/packages \
  -p 8080:8080 \
  --name pypiserver \
  [-u <uid>[:<gid>]] \
  [--restart always] \
  pypiserver/pypiserver [\ -P . -a . -o]

# docker parameter
# -d = -detach, -v = --volume, -p = --publish, -u = --user

# pypiserver parameter
# -P . -a .  allow unauthorized access
# -P <PASSWORD_FILE>
# -o overwrite file

# gunicorn config
# /data/gunicorn.conf.py
```
