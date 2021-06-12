# elasticsearch tutorial

## populate

```sh
# create index
PUT school

# add data
POST school/_doc/10
{
   "name":"Saint Paul School", "description":"ICSE Afiliation",
   "street":"Dawarka", "city":"Delhi", "state":"Delhi", "zip":"110075",
   "location":[28.5733056, 77.0122136], "fees":5000,
   "tags":["Good Faculty", "Great Sports"], "rating":"4.5"
}

POST school/_doc/16
{
   "name":"Crescent School", "description":"State Board Affiliation",
   "street":"Tonk Road",
   "city":"Jaipur", "state":"RJ", "zip":"176114","location":[26.8535922,75.7923988],
   "fees":2500, "tags":["Well equipped labs"], "rating":"4.5"
}
```


---

## api onvention

```sh
# multiple Index
POST /index1,index2,index3/_search
{
   "query":{
      "query_string":{
         "query":"any_string"
      }
   }
}

# _all keyword for all index
POST /_all/_search
{
   "query":{
      "query_string":{
         "query":"any_string"
      }
   }
}

# wildcards *, +, -
POST /school*/_search
{
   "query":{
      "query_string":{
         "query":"CBSE"
      }
   }
}

POST /school*,-schools_gov /_search
{
   "query":{
      "query_string":{
         "query":"CBSE"
      }
   }
}

POST /school*,book_shops/_search
{
   "query":{
      "query_string":{
         "query":"CBSE"
      }
   }
}

POST /school*,book_shops/_search?ignore_unavailable=true
{
   "query":{
      "query_string":{
         "query":"CBSE"
      }
   }
}

# allow_no_indices index
POST /schools_pri*/_search?allow_no_indices=true
{
   "query":{
      "match_all":{}
   }
}

# expand_wildcard
POST /schools/_close

POST /school*/_search?expand_wildcards=closed
{
   "query":{
      "match_all":{}
   }
}
# date math support in index Name
## if today date is 30th December 2015
## expression                       resolve
<accountdetail-{now-d}>             accountdetail-2015.12.29
<accountdetail-{now-M}>	            accountdetail-2015.11.30
<accountdetail-{now{YYYY.MM}}>	    accountdetail-2015.12

# pretty result
POST /schools/_search?pretty=true
{
   "query":{
      "match_all":{}
   }
}

# response filter
POST /schools/_search?filter_path = hits.total
{
   "query":{
      "match_all":{}
   }
}
```


---

## document api

```sh
# index api
PUT schools/_doc/5
{
   "name":"City School", "description":"ICSE", "street":"West End",
   "city":"Meerut",
   "state":"UP", "zip":"250002", "location":[28.9926174, 77.692485],
   "fees":3500,
   "tags":["fully computerized"], "rating":"4.5"
}

## versioning
PUT schools/_doc/5?version=7&version_type=external
{
   "name":"Central School", "description":"CBSE Affiliation", "street":"Nagan",
   "city":"paprola", "state":"HP", "zip":"176115", "location":[31.8955385, 76.8380405],
   "fees":2200, "tags":["Senior Secondary", "beautiful campus"], "rating":"3.3"
}

## operation type
PUT chapter/_doc/1?op_type=create
{
   "Text":"this is chapter one"
}

## automatic id generation
POST chapter/_doc/
{
   "user" : "tpoint",
   "post_date" : "2018-12-25T14:12:12",
   "message" : "Elasticsearch Tutorial"
}

# get api
pre class="prettyprint notranslate" > GET schools/_doc/5

GET schools/_doc/5?_source_includes=name,fees 

GET schools/_doc/5?_source 

# delete api
DELETE schools/_doc/4  

# update api
POST schools/_update/4
{
   "script" : {
      "source": "ctx._source.name = params.sname",
      "lang": "painless",
      "params" : {
         "sname" : "City Wise School"
      }
   }
}
```

```bash
# automatic index creation
[centos:~ ] # vi /etc/elasticsearch/elasticsearch.yml
...
action.auto_create_index:false
index.mapper.dynamic:false
-->
action.auto_create_index:+acc*,-bank*
```


---

## search api
