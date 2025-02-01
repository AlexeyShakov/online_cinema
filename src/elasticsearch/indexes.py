from . import config


settings = {
    "number_of_shards": config.SHARD_NUMBER,
    "number_of_replicas": config.REPLICA_NUMBER
}

PERSON_MAPPING = {
    "settings": settings,
    "mappings": {
        "properties": {
            "person_id": { "type": "keyword" },
            "full_name": { "type": "text" },
            "films": {
                "type": "nested",
                "properties": {
                    "film_id": { "type": "keyword" },
                    "title": { "type": "text" }
                }
            }
        }
    }
}

FILMS_MAPPING = {
    "settings": settings,
    "mappings": {
        "properties": {
            "film_id": { "type": "keyword" },
            "title": { "type": "text" },
            "persons": {
                "type": "nested",
                "properties": {
                    "person_id": { "type": "keyword" },
                    "full_name": { "type": "text" }
                }
            }
        }
    }
}
