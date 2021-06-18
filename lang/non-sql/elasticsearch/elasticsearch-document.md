# elasticsearch - document


```bash
[linux:~ ] # curl -s -X <command>  -H 'Content-Type:application/json' -d '{"<key>": "<value>"}' http://<es ip>:<es port>/<uri>
# -s = --silent, -X = --request, -H = --header, -d = --data
```


```sh
GET _all
GET _search
GET _cat
GET _cat/health
GET _cat/nodes
GET _cat/indices
```


---

## index

```sh
PUT <index>                # create index
GET _cat/indices           # list index
GET _cat/indices/<index>   # show index
DELETE <index>             # delete index
```


---

## document

```sh
PUT <index>/<type>/<id>        # create / full update document
{"<key>": "<value>"}

POST <index>/<type>/<id>       # create / partial update document
{"<key>": "<value>"}

GET /<index>/<type>/<id>       # read document
DELETE /<index>/<type>/<id>    # delete document

GET /<index>/<type>/_searsh    # list document
```

