# postgre

## install

```bash
[linux:~ ] # docker pull postgres
[linux:~ ] # docker run -d \
    -e POSTGRES_PASSWORD=<password> \
    -p 5432:5432 \
    [-e PGDATA=/var/lib/postgresql/data/pgdata] \
    [-v /data/db:/var/lib/postgresql/data] \
    --name postgres \
    postgres

[linux:~ ] # docker exec -it postgres psql -U postgres
```
