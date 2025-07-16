### creating elastsicsearch index 
``` bash
curl -u user:pass -XPUT 'localhost:9200/myindex/?pretty'
```

### creating an index and put document directly to it

> Fixed Command (Modern Elasticsearch 7.x+):
```bash
curl -u user:pass -XPUT 'localhost:9200/myindex/_doc/1?pretty' \
  -H 'Content-Type: application/json' \
  -d '{
    "book_name": "learning elk"
  }'
```
> Or for older Elasticsearch versions (6.x and below):
```bash
curl -u user:pass -XPUT 'localhost:9200/myindex/elk/1?pretty' \
  -H 'Content-Type: application/json' \
  -d '{
    "book_name": "learning elk"
  }'
```
### Retrieving the document
```bash
curl -u user:pass -XGET 'localhost:9200/myindex/_doc/1?pretty'
{
  "_index" : "myindex",
  "_id" : "1",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "book_name" : "learning elk"
  }
}
```
> Deleting Document:

```bash
curl -u user:pass -XDELETE 'localhost:9200/myindex/_doc/1?pretty'
{
  "_index" : "myindex",
  "_id" : "1",
  "_version" : 2,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```
> Deleting index:
```bash
curl -u user:pass -XDELETE 'localhost:9200/myindex?pretty'
{
  "acknowledged" : true
}
``` 
