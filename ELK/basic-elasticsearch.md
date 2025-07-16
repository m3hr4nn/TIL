### basic posts to elasticsearch API
``` bash
curl -X<VERB> '<PROTOCOL>:<HOST>:<PORT>/<PATH>/<OPERATION_STRING>?<QUERY_STRING>' -d '<BODY>'
```
I started an elasticsearch and kibana for local testing, these were my practice:

* checking all available indices:
``` bash
curl -u user:pass -XGET 'localhost:9200/_cat/indices?v'
```

* listing nodes in a cluster:
``` bash
  curl -u user:pass -XGET 'localhost:9200/_cat/nodes?v'
```

* health of the cluster:
``` bash
curl -u user:pass -XGET 'localhost:9200/_cluster/health?pretty=true'
```
* creating an index:

Elasticsearch has specific naming rules and conventions:
Required Rules:
0) Must be lowercase
1) Cannot contain: \, /, *, ?, ", <, >, |,   (space), ,, #
2) Cannot start with -, _, or +
3) Cannot be . or ..
4) Cannot be longer than 255 bytes

Follow **kebab-case** **or **snake_case** if the index naming is long.

Wrong example
```bash
$ curl -u user:pass -XPUT 'localhost:9200/MyIndex/?pretty'
```
``` JSON
{
  "error" : {
    "root_cause" : [
      {
        "type" : "invalid_index_name_exception",
        "reason" : "Invalid index name [MyIndex], must be lowercase",
        "index_uuid" : "_na_",
        "index" : "MyIndex"
      }
    ],
    "type" : "invalid_index_name_exception",
    "reason" : "Invalid index name [MyIndex], must be lowercase",
    "index_uuid" : "_na_",
    "index" : "MyIndex"
  },
  "status" : 400
}
```
Correct example
``` bash
$ curl -u user:pass -XPUT 'localhost:9200/myindex/?pretty'
```
Result: 
``` JSON
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "myindex"
}
```
