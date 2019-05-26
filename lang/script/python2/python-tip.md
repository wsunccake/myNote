# Python Tip


## Parser JSON

```bash
linux:~ # curl https://registry.hub.docker.com/v2/repositories/library/python/tags/ | python -m json.tool
```

---

## Web service

```bash
# for python2
linux:~ # python -m SimpleHTTPServer 8080

# for python3
linux:~ # python3 -m http.server 8000
```
