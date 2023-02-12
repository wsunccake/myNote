# dvwa

```bash
# pull image
[linux:~ ] # docker pull vulnerables/web-dvwa

[linux:~ ] # docker run \
  -p 80:80 \
  --rm \
  --name dvwa \
  vulnerables/web-dvwa
# -p = --publish, -u = --user, --rm
```
