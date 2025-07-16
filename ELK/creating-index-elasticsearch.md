### creating elastsicsearch index 
``` bash
curl -u user:pass -XPUT 'localhost:9200/myindex/?pretty'
```

### creating an index and put document directly to it

Fixed Command (Modern Elasticsearch 7.x+):
```bash
curl -u user:pass -XPUT 'localhost:9200/myindex/_doc/1?pretty' \
  -H 'Content-Type: application/json' \
  -d '{
    "book_name": "learning elk"
  }'
```
Or for older Elasticsearch versions (6.x and below):
```bash
curl -u user:pass -XPUT 'localhost:9200/myindex/elk/1?pretty' \
  -H 'Content-Type: application/json' \
  -d '{
    "book_name": "learning elk"
  }'
```
