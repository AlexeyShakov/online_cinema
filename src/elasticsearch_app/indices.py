from src.general_usage.settings import get_elastic_settings

elastic_settings = get_elastic_settings()

settings = {
    "number_of_shards": elastic_settings.shard_number,
    "number_of_replicas": elastic_settings.replica_number,
}

PERSON_MAPPING = {
    "settings": settings,
    "mappings": {
        "properties": {
            "type": {"type": "keyword"},
            "id": {"type": "keyword"},
            "attributes": {
                "properties": {
                    "name_en": {"type": "text", "analyzer": "english"},
                    "name_ru": {"type": "text", "analyzer": "russian"},
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
                    "title_en": {"type": "text", "analyzer": "english"},
                    "title_ru": {"type": "text", "analyzer": "russian"},
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
