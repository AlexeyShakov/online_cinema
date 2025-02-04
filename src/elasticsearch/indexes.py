from . import config


settings = {
    "number_of_shards": config.SHARD_NUMBER,
    "number_of_replicas": config.REPLICA_NUMBER
}


PERSON_MAPPING = {
    "settings": settings,
    "mappings": {
    "properties": {
      "type": {"type": "keyword"},
      "id": {"type": "keyword"},
      "attributes": {
        "properties": {
          "name": {"type": "text"}
        }
      },
      "relationships": {
        "properties": {
          "movies": {
            "properties": {
              "data": {
                "type": "nested",
                "properties": {
                  "type": {
                    "type": "keyword"
                  },
                  "id": {
                    "type": "keyword"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}


FILMS_MAPPING = {
    "settings": settings,
    "mappings": {
    "properties": {
      "type": {"type": "keyword"},
      "id": {"type": "keyword"},
      "attributes": {
        "properties": {
          "title": {"type": "text"},
          "description": {"type": "text"},
          "category_ids": {"type": "keyword"}
        }
      },
      "relationships": {
        "properties": {
          "actors": {
            "properties": {
              "data": {
                "type": "nested",
                "properties": {
                  "type": {
                    "type": "keyword"
                  },
                  "id": {
                    "type": "keyword"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
