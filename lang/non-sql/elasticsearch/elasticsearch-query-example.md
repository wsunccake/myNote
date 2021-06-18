# Elasticsearch Query Example

## demo index

```sh
PUT employees

PUT employees/_mapping
{
  "properties": {
    "date_of_birth": {
      "type": "date",
      "format": "dd/MM/yyyy"
    }
  }
}

POST _bulk
{ "index" : { "_index" : "employees", "_id" : "1" } }
{"id":1,"name":"Huntlee Dargavel","email":"hdargavel0@japanpost.jp","gender":"male","ip_address":"58.11.89.193","date_of_birth":"11/09/1990","company":"Talane","position":"Research Associate","experience":7,"country":"China","phrase":"Multi-channelled coherent leverage","salary":180025}
{ "index" : { "_index" : "employees", "_id" : "2" } }
{"id":2,"name":"Othilia Cathel","email":"ocathel1@senate.gov","gender":"female","ip_address":"3.164.153.228","date_of_birth":"22/07/1987","company":"Edgepulse","position":"Structural Engineer","experience":11,"country":"China","phrase":"Grass-roots heuristic help-desk","salary":193530}
{ "index" : { "_index" : "employees", "_id" : "3" } }
{"id":3,"name":"Winston Waren","email":"wwaren2@4shared.com","gender":"male","ip_address":"202.37.210.94","date_of_birth":"10/11/1985","company":"Yozio","position":"Human Resources Manager","experience":12,"country":"China","phrase":"Versatile object-oriented emulation","salary":50616}
{ "index" : { "_index" : "employees", "_id" : "4" } }
{"id" : 4,"name" : "Alan Thomas","email" : "athomas2@example.com","gender" : "male","ip_address" : "200.47.210.95","date_of_birth" : "11/12/1985","company" : "Yamaha","position" : "Resources Manager","experience" : 12,"country" : "China","phrase" : "Emulation of roots heuristic coherent systems","salary" : 300000}
```


---

## match query

```sh
GET employees/_search

POST employees/_search

# match
POST employees/_search
{
  "query": {
    "match": {
      "phrase": {
        "query" : "heuristic"
      }
    }
  }
}

# or
POST employees/_search
{
  "query": {
    "match": {
      "phrase": {
        "query" : "heuristic roots help"
      }
    }
  }
}

# and
POST employees/_search
{
  "query": {
    "match": {
      "phrase": {
        "query" : "heuristic roots help",
        "operator" : "AND"
      }
    }
  }
}

# minimum should match
POST employees/_search
{
  "query": {
    "match": {
      "phrase": {
        "query" : "heuristic roots help",
        "minimum_should_match": 3
      }
    }
  }
}

# multi match
POST employees/_search
{
  "query": {
    "multi_match": {
        "query" : "research help", 
        "fields": ["position","phrase"]
    }
  }
}

# match phrase
GET employees/_search
{
  "query": {
    "match_phrase": {
      "phrase": {
        "query": "roots heuristic coherent"
      }
    }
  }
}


PUT employees/_doc/5
{
  "id": 4,
  "name": "Jennifer Lawrence",
  "email": "jlaw@example.com",
  "gender": "female",
  "ip_address": "100.37.110.59",
  "date_of_birth": "17/05/1995",
  "company": "Monsnto",
  "position": "Resources Manager",
  "experience": 10,
  "country": "Germany",
  "phrase": "Emulation of roots heuristic complete systems",
  "salary": 300000
}

# match phrase prefix
GET employees/_search
{
"_source": [ "phrase" ],
  "query": {
    "match_phrase_prefix": {
      "phrase": {
        "query": "roots heuristic co"
      }
    }
  }
}

DELETE employees/_doc/5
```


---

## term query

```sh
# term
POST employees/_search
{
  "query": {
    "term": {"gender": "female"}
    }
  }
}

POST employees/_search
{
  "query": {
    "term": {"gender": "Female"}
    }
  }
}

# terms
POST employees/_search
{
  "query": {
    "terms": {
      "gender": ["female", "male"]
    }
  }
}


PUT employees/_doc/5
{
  "id": 5,
  "name": "Michael Bordon",
  "email": "mbordon@example.com",
  "gender": "male",
  "ip_address": "10.47.210.65",
  "date_of_birth": "12/12/1995",
  "position": "Resources Manager",
  "experience": 12,
  "country": null,
  "phrase": "Emulation of roots heuristic coherent systems",
  "salary": 300000
}

# exists
GET employees/_search
{
    "query": {
        "exists": {
            "field": "company"
        }
    }
}

GET employees/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "exists": {
            "field": "company"
          }
        }
      ]
    }
  }
}

DELETE employees/_doc/5

# range
POST employees/_search
{
    "query": {
        "range" : {
            "experience" : {
                "gte" : 5,
                "lte" : 10
            }
        }
    }
}

GET employees/_search
{
    "query": {
        "range" : {
            "date_of_birth" : {
                "gte" : "01/01/1986"
            }
        }
    }
}

# ids
POST employees/_search
{
    "query": {
        "ids" : {
            "values" : ["1", "4"]
        }
    }
}

# prefix
GET employees/_search
{
  "query": {
    "prefix": {
      "name": "al"
    }
  }
}

# wildcard
GET employees/_search
{
    "query": {
        "wildcard": {
            "country": {
                "value": "c*a"
            }
        }
    }
}

# regexp
GET employees/_search
{
  "query": {
    "regexp": {
      "position": "res[a-z]*"
    }
  }
}

# fuzzy
GET employees/_search
{
  "query": {
    "fuzzy": {
      "country": {
        "value": "Chnia",
        "fuzziness": "2"
      }
    }
  }
}

POST employees/_search
{
    "query": {
        "multi_match" : {
            "query" : "heursitic reserch",
            "fields": ["phrase","position"],
            "fuzziness": 2
        }
    },
    "size": 10
}
```


---

## boost

### bool query

```sh
POST employees/_search
{
    "query": {
        "multi_match" : {
            "query" : "versatile Engineer",
            "fields": ["position", "phrase"]
        }
    }
}

# boost
POST employees/_search
{
    "query": {
        "multi_match" : {
            "query" : "versatile Engineer",
            "fields": ["position^3", "phrase"]
        }
    }
}
```


---

## sort

```sh
# default sort
GET employees/_search
{
   "_source": ["country"], 
   "query": {
      "match": {
        "country": "China"
      }
   }
}

# no sort
GET employees/_search
{
   "_source": ["country"], 
   "query": {
      "bool": {
          "filter": {
              "country": "China"
          }
      }
   }
}

# sort by field
GET employees/_search
{
   "_source": ["name","experience","salary"], 
   "sort": [
    {
      "experience": {
        "order": "desc"
      }
    }
   ],
}

# sort by multi field
GET employees/_search
{
  "_source": [
    "name",
    "experience",
    "salary"
  ],
  "sort": [
    {
      "experience": {
        "order": "desc"
      }
    },
    {
      "salary": {
        "order": "desc"
      }
    }
  ]
}

GET employees/_search
{
  "_source": [
    "name",
    "experience",
    "salary"
  ],
  "sort": [
    {
      "salary": {
        "order": "desc"
      }
    },
    {
      "experience": {
        "order": "desc"
      }
    }
  ]
}
```

---

## compound query

```sh
POST _search
{
  "query": {
    "bool" : {
      "must" : [],
      "filter": [],
      "must_not" : [],
      "should" : []
    }
  }
}

# must
POST employees/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "position": "manager"
          }
        },
        {
          "range": {
            "experience": {
              "gte": 12
            }
          }
        }
      ]
    }
  }
}

# filter
POST employees/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "match": {
            "position": "manager"
          }
        },
        {
          "range": {
            "experience": {
              "gte": 12
            }
          }
        }
      ]
    }
  }
}

# should
POST employees/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "position": "manager"
          }
        },
        {
          "range": {
            "experience": {
              "gte": 12
            }
          }
        }
      ],
    "should": [
      {
        "match": {
          "phrase": "versatile"
        }
      }
    ]
    }
  }
}

# multiple condition
# (company = Yamaha OR company = Yozio ) AND (position = manager OR position = associate ) AND (salary>=100000)
POST employees/_search
{
    "query": {
        "bool": {
            "must": [
              {
                "bool": {
                    "should": [{
                        "match": {
                            "company": "Talane"
                        }
                    }, {
                        "match": {
                            "company": "Yamaha"
                        }
                    }]
                }
            }, 
            {
                "bool": {
                    "should": [
                      {
                        "match": {
                            "position": "manager"
                        }
                    }, {
                        "match": {
                            "position": "Associate"
                        }
                    }
                    ]
                }
            }, {
                "bool": {
                    "must": [
                      {
                        "range": {
                          "salary": {
                            "gte": 100000
                          }
                        }
                      }
                      ]
                }
            }]
        }
    }
}
```


### boosting query

```sh
# positive negative
POST  employees/_search
{
    "query": {
        "boosting" : {
            "positive" : {
                "match": {
                  "country": "china"
                }
            },
            "negative" : {
                 "match": {
                  "company": "Talane"
                }
            },
            "negative_boost" : 0.5
        }
    }
}

GET employees/_search
{
  "query": {
    "boosting": {
      "positive": {
        "bool": {
          "should": [
            {
              "match": {
                "country": {
                  "query": "china"
                }
              }
            },
            {
              "range": {
                "experience": {
                  "gte": 10
                }
              }
            }
          ]
        }
      },
      "negative": {
        "match": {
          "gender": "female"
        }
      },
      "negative_boost": 0.5
    }
  }
}
```


### function score query

```sh
# match query
POST employees/_search
{
  "_source": ["position"],
  "query": {
    "match": {
      "position": "manager"
      }
    }
  }
}

# match query with functio_score
POST employees/_search
{
  "_source": ["position"],
  "query": {
    "function_score": {
      "query": {
        "match": {
          "position": "manager"
        }
      },
      "boost": "5",
      "boost_mode": "multiply"
    }
  }
}

# function_score: weight
GET employees/_search
{
"_source": ["position","phrase"], 
  "query": {
    "function_score": {
      "query": {
        "match": {
          "position": "manager"
        }
      },
      "functions": [
        {
          "filter": {
            "match": {
              "phrase": "coherent"
            }
          },
          "weight": 2
        },
        {
          "filter": {
            "match": {
              "phrase": "emulation"
            }
          },
          "weight": 10
        }
      ],
      "score_mode": "multiply", 
      "boost": "5",
      "boost_mode": "multiply"
    }
  }
}

# function_score: script_score
GET employees/_search
{
  "_source": [
    "name",
    "experience",
    "salary"
  ],
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "functions": [
        {
          "script_score": {
            "script": {
              "source": "(doc['salary'].value/doc['experience'].value)/1000"
            }
          }
        }
      ],
      "boost_mode": "replace"
    }
  }
}

# function_score: field_value_factor
GET employees/_search
{
  "_source": ["name","experience"], 
    "query": {
        "function_score": {
            "field_value_factor": {
                "field": "experience",      
                 "factor": 0.5,
                "modifier": "square",
                "missing": 1
            }
        }
    }
}

# function_score: decay function
GET employees/_search
{
  "_source": [
    "name",
    "salary"
  ],
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "functions": [
       {
         "gauss": {
           "salary": {
             "origin": 200000,
             "scale": 30000
           }
         }
       }
      ],
      "boost_mode": "replace"
    }
  }
}
```


---

## parent-child query

```sh
PUT post-comments
{
  "mappings": {
    "properties": {
      "document_type": { 
        "type": "join",
        "relations": {
          "post": "comment" 
        }
      }
    }
  }
}

PUT post-comments/_doc/1
{
"document_type": {
    "name": "post" 
  },
"post_title" : "Angel Has Fallen"
}

PUT post-comments/_doc/2
{
"document_type": {
    "name": "post" 
  },
"post_title" : "Beauty and the beast - a nice movie"
}

PPUT post-comments/_doc/A?routing=1
{
"document_type": {
    "name": "comment",
    "parent": "1"
  },
"comment_author": "Neil Soans",
"comment_description": "'Angel has Fallen' has some redeeming qualities, but they're too few and far in between to justify its existence"
}

PUT post-comments/_doc/B?routing=1
{
"document_type": {
    "name": "comment",
    "parent": "1"
  },
"comment_author": "Exiled Universe",
"comment_description": "Best in the trilogy! This movie wasn't better than the Rambo movie but it was very very close."
}

PUT post-comments/_doc/D?routing=1
{
"document_type": {
    "name": "comment",
    "parent": "2"
  },
"comment_author": "Emma Cochrane",
"comment_description": "There's the sublime beauty of a forgotten world and the promise of happily-ever-after to draw you to one of your favourite fairy tales, once again. Give it an encore."
}

PUT post-comments/_doc/E?routing=1
{
"document_type": {
    "name": "comment",
    "parent": "2"
  },
"comment_author": "Common Sense Media Editors",
"comment_description": "Stellar music, brisk storytelling, delightful animation, and compelling characters make this both a great animated feature for kids and a great movie for anyone"
}
```

```sh
# has_child
GET post-comments/_search
{
  "query": {
    "has_child": {
      "type": "comment",
      "query": {
        "match": {
          "comment_description": "music"
        }
      }
    }
  }
}

# has_parent
GET post-comments/_search
{
  "query": {
    "has_parent": {
      "parent_type": "post",
      "query": {
        "match": {
          "post_title": "Beauty"
        }
      }
    }
  }
}
```


---

## other query

```sh
# query_string 
POST employees/_search
{
  "query": {
    "query_string": {
      "query": "(roots heuristic systems) OR (enigneer~) OR (salary:(>=10000 AND <=52000)) ",
      "fields": [
        "position",
        "phrase^3"
      ]
    }
  }
}

# simple_query_string
POST employees/_search
{
  "query": {
    "simple_query_string": {
      "query": "(roots) | (resources manager) + (male) ",
      "fields": [
        "gender",
        "position",
        "phrase^3"
      ]
    }
  }
}

# name query
POST employees/_search
{
  "query": {
    "match": {
      "phrase": {
          "query": "roots",
          "_name": "phrase_field_name"
      }
    }
  }
}

POST employees/_search
{
  "query": {
    "bool": {
      "should": [
          {
            "match": {
              "phrase": {
                "query": "roots",
                "_name": "phrase_field_name"
              }
            }
          },
          {
            "match": {
               "gender": {
                "query": "female",
                "_name": "phrase_field_name"
              }               
            }
          }
      ]    
    }
  }
}

```