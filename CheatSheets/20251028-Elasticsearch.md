# Elasticsearch Interview Cheat Sheet

## Core Concepts

**Index**: Collection of documents with similar characteristics (like a database)
**Document**: Basic unit of information (JSON object)
**Type**: Logical category within an index (deprecated in 7.x)
**Shard**: Subset of an index (horizontal scaling)
**Replica**: Copy of a shard (fault tolerance and read throughput)
**Node**: Single running instance of Elasticsearch
**Cluster**: Collection of nodes working together
**Mapping**: Schema definition for documents
**Inverted Index**: Core data structure for fast text search

## Architecture

```
Cluster
├── Node 1 (Master-eligible, Data)
│   ├── Index A (Primary Shard 0, Replica Shard 1)
│   └── Index B (Primary Shard 1)
├── Node 2 (Data)
│   ├── Index A (Replica Shard 0)
│   └── Index B (Primary Shard 0, Replica Shard 1)
└── Node 3 (Coordinating, Ingest)
```

## Index Operations

### Create Index
```bash
# Simple index
PUT /products

# With settings and mappings
PUT /products
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 2,
    "refresh_interval": "30s"
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "standard"
      },
      "price": {
        "type": "float"
      },
      "category": {
        "type": "keyword"
      },
      "description": {
        "type": "text"
      },
      "created_at": {
        "type": "date"
      },
      "tags": {
        "type": "keyword"
      },
      "in_stock": {
        "type": "boolean"
      }
    }
  }
}
```

### List Indices
```bash
GET /_cat/indices?v

# Specific index info
GET /products
```

### Delete Index
```bash
DELETE /products
```

### Update Index Settings
```bash
PUT /products/_settings
{
  "index": {
    "number_of_replicas": 1,
    "refresh_interval": "10s"
  }
}
```

## Document Operations (CRUD)

### Create Document
```bash
# With auto-generated ID
POST /products/_doc
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics",
  "in_stock": true
}

# With custom ID
PUT /products/_doc/1
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}
```

### Read Document
```bash
# Get by ID
GET /products/_doc/1

# Get multiple documents
GET /products/_mget
{
  "ids": ["1", "2", "3"]
}
```

### Update Document
```bash
# Partial update
POST /products/_update/1
{
  "doc": {
    "price": 899.99
  }
}

# Script update
POST /products/_update/1
{
  "script": {
    "source": "ctx._source.price *= params.discount",
    "params": {
      "discount": 0.9
    }
  }
}

# Upsert (update or insert)
POST /products/_update/1
{
  "doc": {
    "price": 999.99
  },
  "doc_as_upsert": true
}
```

### Delete Document
```bash
DELETE /products/_doc/1
```

### Bulk Operations
```bash
POST /_bulk
{ "index": { "_index": "products", "_id": "1" } }
{ "name": "Laptop", "price": 999.99 }
{ "index": { "_index": "products", "_id": "2" } }
{ "name": "Mouse", "price": 29.99 }
{ "update": { "_index": "products", "_id": "1" } }
{ "doc": { "price": 899.99 } }
{ "delete": { "_index": "products", "_id": "3" } }
```

## Search Operations

### Basic Search
```bash
# Search all documents
GET /products/_search

# Match query
GET /products/_search
{
  "query": {
    "match": {
      "name": "laptop"
    }
  }
}

# Multi-match query
GET /products/_search
{
  "query": {
    "multi_match": {
      "query": "gaming laptop",
      "fields": ["name", "description"]
    }
  }
}
```

### Term-level Queries
```bash
# Term query (exact match)
GET /products/_search
{
  "query": {
    "term": {
      "category.keyword": "Electronics"
    }
  }
}

# Terms query (multiple values)
GET /products/_search
{
  "query": {
    "terms": {
      "tags": ["sale", "featured"]
    }
  }
}

# Range query
GET /products/_search
{
  "query": {
    "range": {
      "price": {
        "gte": 100,
        "lte": 500
      }
    }
  }
}

# Exists query
GET /products/_search
{
  "query": {
    "exists": {
      "field": "discount"
    }
  }
}

# Wildcard query
GET /products/_search
{
  "query": {
    "wildcard": {
      "name": "lap*"
    }
  }
}
```

### Boolean Queries
```bash
# Bool query (must, should, must_not, filter)
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "laptop" } }
      ],
      "filter": [
        { "range": { "price": { "lte": 1000 } } },
        { "term": { "in_stock": true } }
      ],
      "should": [
        { "term": { "tags": "featured" } }
      ],
      "must_not": [
        { "term": { "category": "Refurbished" } }
      ],
      "minimum_should_match": 1
    }
  }
}
```

### Aggregations

```bash
# Terms aggregation (grouping)
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category.keyword",
        "size": 10
      }
    }
  }
}

# Stats aggregation
GET /products/_search
{
  "size": 0,
  "aggs": {
    "price_stats": {
      "stats": {
        "field": "price"
      }
    }
  }
}

# Histogram
GET /products/_search
{
  "size": 0,
  "aggs": {
    "price_ranges": {
      "histogram": {
        "field": "price",
        "interval": 100
      }
    }
  }
}

# Date histogram
GET /logs/_search
{
  "size": 0,
  "aggs": {
    "sales_over_time": {
      "date_histogram": {
        "field": "created_at",
        "calendar_interval": "day"
      }
    }
  }
}

# Nested aggregations
GET /products/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category.keyword"
      },
      "aggs": {
        "avg_price": {
          "avg": {
            "field": "price"
          }
        }
      }
    }
  }
}
```

### Sorting and Pagination
```bash
# Sort by field
GET /products/_search
{
  "query": { "match_all": {} },
  "sort": [
    { "price": "desc" },
    { "_score": "desc" }
  ]
}

# Pagination
GET /products/_search
{
  "from": 0,
  "size": 10,
  "query": { "match_all": {} }
}

# Search after (for deep pagination)
GET /products/_search
{
  "size": 10,
  "query": { "match_all": {} },
  "sort": [
    { "price": "asc" },
    { "_id": "asc" }
  ],
  "search_after": [999.99, "product_123"]
}
```

### Highlighting
```bash
GET /products/_search
{
  "query": {
    "match": {
      "description": "gaming"
    }
  },
  "highlight": {
    "fields": {
      "description": {}
    }
  }
}
```

## Mapping

### Data Types
```bash
# Text: Full-text search
# Keyword: Exact values, aggregations, sorting
# Integer, Long, Short, Byte, Double, Float
# Boolean
# Date
# Object: Nested JSON objects
# Nested: Array of objects
# Geo-point, Geo-shape: Geographic data
```

### Define Mapping
```bash
PUT /products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "price": { "type": "float" },
      "tags": { "type": "keyword" },
      "specs": {
        "properties": {
          "cpu": { "type": "text" },
          "ram": { "type": "integer" }
        }
      },
      "location": { "type": "geo_point" }
    }
  }
}
```

### Update Mapping
```bash
# Add new field (existing fields cannot be changed)
PUT /products/_mapping
{
  "properties": {
    "sku": {
      "type": "keyword"
    }
  }
}
```

### View Mapping
```bash
GET /products/_mapping
```

## Analyzers

### Built-in Analyzers
```bash
# Standard analyzer (default)
# Whitespace analyzer
# Simple analyzer
# Stop analyzer
# Keyword analyzer (no-op)
# Pattern analyzer
# Language analyzers (english, spanish, etc.)
```

### Custom Analyzer
```bash
PUT /products
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": ["html_strip"],
          "filter": ["lowercase", "stop", "snowball"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "analyzer": "custom_analyzer"
      }
    }
  }
}
```

### Test Analyzer
```bash
POST /_analyze
{
  "analyzer": "standard",
  "text": "The Quick Brown Fox"
}
```

## Cluster Management

### Cluster Health
```bash
GET /_cluster/health
GET /_cluster/health?level=indices
GET /_cluster/health/products
```

### Node Info
```bash
GET /_cat/nodes?v
GET /_nodes
GET /_nodes/stats
```

### Shard Allocation
```bash
GET /_cat/shards?v
GET /_cat/shards/products?v

# Explain allocation
GET /_cluster/allocation/explain
```

### Cluster Settings
```bash
# Get settings
GET /_cluster/settings

# Update settings
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}
```

## Index Templates

### Create Template
```bash
PUT /_index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "timestamp": { "type": "date" },
        "message": { "type": "text" },
        "level": { "type": "keyword" }
      }
    }
  }
}
```

## Snapshots and Restore

### Register Repository
```bash
PUT /_snapshot/my_backup
{
  "type": "fs",
  "settings": {
    "location": "/mount/backups/elasticsearch"
  }
}
```

### Create Snapshot
```bash
PUT /_snapshot/my_backup/snapshot_1
{
  "indices": "products,orders",
  "ignore_unavailable": true,
  "include_global_state": false
}
```

### Restore Snapshot
```bash
POST /_snapshot/my_backup/snapshot_1/_restore
{
  "indices": "products",
  "ignore_unavailable": true
}
```

## Performance Tuning

### Refresh Interval
```bash
# Increase for better indexing performance
PUT /products/_settings
{
  "index.refresh_interval": "30s"
}

# Disable during bulk indexing
PUT /products/_settings
{
  "index.refresh_interval": "-1"
}
```

### Bulk Indexing
```bash
# Optimal bulk size: 5-15 MB
# Use multiple threads
# Disable replicas during initial load
PUT /products/_settings
{
  "number_of_replicas": 0
}
```

### Force Merge
```bash
# Reduce segment count (after bulk indexing)
POST /products/_forcemerge?max_num_segments=1
```

### Cache Control
```bash
# Clear cache
POST /products/_cache/clear
POST /_cache/clear
```

## Monitoring

### Index Stats
```bash
GET /products/_stats
GET /_stats
```

### Task Management
```bash
# List tasks
GET /_tasks

# Cancel task
POST /_tasks/TASK_ID/_cancel
```

### Hot Threads
```bash
GET /_nodes/hot_threads
```

## Common Interview Questions

**Q: What is Elasticsearch?**
- Distributed search and analytics engine
- Built on Apache Lucene
- RESTful API
- Real-time search and analytics
- Horizontally scalable

**Q: Explain shards and replicas**
- Shard: Subset of index data (horizontal scaling)
- Primary shard: Original copy
- Replica shard: Copy of primary (redundancy, read performance)
- Number of primary shards fixed at creation

**Q: Difference between text and keyword?**
- Text: Analyzed, full-text search, not for aggregations
- Keyword: Not analyzed, exact match, aggregations, sorting

**Q: What is inverted index?**
- Maps terms to documents containing them
- Core data structure for fast text search
- Terms → Document IDs + positions

**Q: Explain bool query**
- must: Must match (affects score)
- should: Optional match (affects score)
- filter: Must match (no score, cached)
- must_not: Must not match

**Q: What are analyzers?**
- Process text during indexing and search
- Tokenizer: Splits text into tokens
- Filters: Transform tokens (lowercase, stop words)
- Char filters: Preprocess text

**Q: How to achieve high availability?**
- Multiple nodes
- Replica shards
- Master-eligible nodes (quorum)
- Cross-cluster replication

**Q: Difference between match and term query?**
- match: Analyzed, full-text search
- term: Exact match, not analyzed

**Q: What is refresh interval?**
- How often index becomes searchable
- Default: 1 second
- Trade-off: freshness vs performance

**Q: Explain CAP theorem in ES**
- Prioritizes Availability and Partition tolerance
- Eventually consistent
- Can tune with write consistency

**Q: How to optimize search performance?**
- Use filters (cached)
- Appropriate shard size
- Use keyword for aggregations
- Disable _source if not needed
- Use search_after for pagination

**Q: What is cluster split brain?**
- Network partition causes multiple masters
- Prevented by minimum_master_nodes setting
- Use odd number of master-eligible nodes

**Q: Explain document routing**
- shard = hash(routing) % number_of_primary_shards
- Default routing: document ID
- Custom routing for data locality
