# mongodb

## install

```bash
[linux:~ ] # docker pull mongo
[linux:~ ] # docker run -d \
    -p 27017:27017 \
    [-v /data/db:/data/db] \
    --name mongo \
    mongo
[linux:~ ] # docker exec -it mongo mongo
```
