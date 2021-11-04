# elasticsearch - api

## curl command

```bash
[linux:~ ] # curl -s [-I] -X <command>  -H 'Content-Type:application/json' [-d '{"<key>": "<value>"}'] http://<es ip>:<es port>/<uri>
# -s = --silent, -I = --head, -X = --request, -H = --header, -d = --data
```


---

## es map rdbms

```
Elasticsearch       RDBMS
----------------------------
Cluster             Database
Shard               Shard
Index               Table
Field               Column
Document            Row
```


---

## index api

### index management

```sh
PUT /<target>           # create index api
DELETE /<target>        # delete index api
GET /<target>           # get index api
HEAD <target>           # exist api
POST /<index>/_close    # close index api
POST /<target>/_open    # open index api

POST /<index>/_shrink/<target-index>  # shrink index api
PUT /<index>/_shrink/<target-index>
POST /<index>/_split/<target-index>   # split index api
PUT /<index>/_split/<target-index>
POST /<index>/_clone/<target-index>   # clone index api
PUT /<index>/_clone/<target-index>
POST /<rollover-target>/_rollover/    # rollover api
POST /<rollover-target>/_rollover/<target-index>
```

```sh
# create index api
PUT /my-index-000001

# delete index api
DELETE /my-index-000001

# get index api
GET /my-index-000001

# exist api
HEAD my-data-stream

# close index api
POST /my-index-000001/_close

# open index api
POST /my-index-000001/_open

# shrink index api
POST /my-index-000001/_shrink/shrunk-my-index-000001
{
  "settings": {
    "index.routing.allocation.require._name": null, 
    "index.blocks.write": null 
  }
}

# split index api
POST /my-index-000001/_split/split-my-index-000001
{
  "settings": {
    "index.number_of_shards": 2
  }
}

# clone index api
POST /my-index-000001/_clone/cloned-my-index-000001

# rollover api
POST my-data-stream/_rollover
```


### mapping management

```sh
PUT /<target>/_mapping           # update mapping api
GET /_mapping                    # get mapping api
GET /<target>/_mapping
GET /_mapping/field/<field>      # get field mapping api
GET /<target>/_mapping/field/<field>
```

```sh
# update mapping api
PUT /publications

PUT /publications/_mapping
{
  "properties": {
    "title":  { "type": "text"}
  }
}

# get mapping api
GET /my-index-000001,my-index-000002/_mapping

GET /*/_mapping

GET /_all/_mapping

GET /_mapping

# get field mapping api
PUT /publications
{
  "mappings": {
    "properties": {
      "id": { "type": "text" },
      "title": { "type": "text" },
      "abstract": { "type": "text" },
      "author": {
        "properties": {
          "id": { "type": "text" },
          "name": { "type": "text" }
        }
      }
    }
  }
}

GET publications/_mapping/field/title

GET publications/_mapping/field/author.id,abstract,name
```


### alias management

```sh
POST /_aliases                      # alias api
PUT /<index>/_alias/<alias>         # create / update index alias api
POST /<index>/_alias/<alias>
PUT /<index>/_aliases/<alias>
POST /<index>/_aliases/<alias>
GET /_alias                         # get index alias api
GET /_alias/<alias>
GET /<index>/_alias/<alias>
HEAD /_alias/<alias>                # index alias exist api
HEAD /<index>/_alias/<alias>
DELETE /<index>/_alias/<alias>      # delete index alias api
DELETE /<index>/_aliases/<alias>
```

```sh
# add alias api
POST /_aliases
{
  "actions" : [
    { "add" : { "index" : "test1", "alias" : "alias1" } }
  ]
}

# remove  alias api
POST /_aliases
{
  "actions" : [
    { "remove" : { "index" : "test1", "alias" : "alias1" } }
  ]
}

# create / update index alias api
PUT /my-index-000001/_alias/alias1

# get index alias api
GET /my-index-000001/_alias/alias1

# index alias exist api
HEAD /_alias/alias1

# delete index alias api
DELETE /my-index-000001/_alias/alias1
```


### index setting

```sh
PUT /<target>/_settings         # update index setting api
GET /<target>/_settings         # get index setting api
GET /<target>/_settings/<setting>
GET /_analyze                   # analyze api
POST /_analyze
GET /<index>/_analyze
POST /<index>/_analyze
```

```sh
# update index setting api
PUT /my-index-000001/_settings
{
  "index" : {
    "number_of_replicas" : 2
  }
}

# get index setting api
GET /my-index-000001/_settings

# analyze api
GET /_analyze
{
  "analyzer" : "standard",
  "text" : "Quick Brown Foxes!"
}
```


---

## document api


### single document api

```sh
# index api
PUT /<target>/_doc/<_id>
POST /<target>/_doc/
PUT /<target>/_create/<_id>
POST /<target>/_create/<_id>

# get api
GET <index>/_doc/<_id>
HEAD <index>/_doc/<_id>
GET <index>/_source/<_id>
HEAD <index>/_source/<_id>

# delete api
DELETE /<index>/_doc/<_id>

# update api
POST /<index>/_update/<_id>
```

```sh
# index api
POST my-index-000001/_doc/
{
    "user": {
        "id": "es1"
    }
}

POST my-index-000001/_doc?routing=kimchy
{
    "user": {
        "id": "es2"
    }
}

PUT my-index-000001/_doc/1
{
    "user": {
        "id": "es3"
    }
}

PUT my-index-000001/_create/2
{
    "user": {
        "id": "es4"
    }
}

# get api
GET my-index-000001/_doc/0

# delete api
DELETE /my-index-000001/_doc/1

# update api
PUT test/_doc/1
{
    "counter": 1,
    "tags": [
        "red"
    ]
}

POST test/_update/1
{
    "script": {
        "source": "ctx._source.counter += params.count",
        "lang": "painless",
        "params": {
            "count": 4
        }
    }
}

POST test/_update/1
{
    "script": {
        "source": "ctx._source.tags.add(params.tag)",
        "lang": "painless",
        "params": {
            "tag": "blue"
        }
    }
}

POST test/_update/1
{
    "script": {
        "source": "if (ctx._source.tags.contains(params.tag)) { ctx._source.tags.remove(ctx._source.tags.indexOf(params.tag)) }",
        "lang": "painless",
        "params": {
            "tag": "blue"
        }
    }
}

POST test/_update/1
{
    "doc": {
        "name": "new_name"
    }
}
```


### multi document api

```sh
# mget api
GET /_mget
GET /<target>/_mget

# bulk api
POST /_bulk
POST /<target>/_bulk

# delete by query api
POST /<target>/_delete_by_query

# update by query api
POST /<target>/_update_by_query

# reindex
POST /_reindex
```

```sh
GET /my-index-000001/_mget
{
    "docs": [
        {
            "_type": "_doc",
            "_id": "1"
        },
        {
            "_type": "_doc",
            "_id": "2"
        }
    ]
}

GET /my-index-000001/_mget
{
    "ids": [
        "1",
        "2"
    ]
}

GET /_mget
{
    "docs": [
        {
            "_index": "test",
            "_type": "_doc",
            "_id": "1",
            "routing": "key2"
        },
        {
            "_index": "test",
            "_type": "_doc",
            "_id": "2"
        }
    ]
}

# bulk api
POST _bulk
{"index": { "_index": "test", "_id": "1"}}
{ "delete" : { "_index" : "test", "_id" : "2" } }
{ "create" : { "_index" : "test", "_id" : "3" } }

# delete by query api
POST /my-index-000001,my-index-000002/_delete_by_query
{
    "query": {
        "match_all": {}
    }
}

POST my-index-000001/_delete_by_query
{
    "query": {
        "term": {
            "user.id": "kimchy"
        }
    }
}

# update by query api
POST my-index-000001/_update_by_query?conflicts=proceed
{
    "query": {
        "term": {
            "user.id": "kimchy"
        }
    }
}

# reindex
POST _reindex
{
  "source": {
    "index": "my-index-000001"
  },
  "dest": {
    "index": "my-new-index-000001"
  }
}
```

