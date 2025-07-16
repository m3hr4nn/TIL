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
