from . import config

settings = {
    "number_of_shards": config.SHARD_NUMBER,
    "number_of_replicas": config.REPLICA_NUMBER,
}


PERSON_MAPPING = {
    "settings": {
        "analysis": {
            "filter": {
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_keywords": {
                    "type": "keyword_marker",
                    "keywords": ["пример"]
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                },
                "russian_ngram_filter": {
                    "type": "ngram",
                    "min_gram": 2,
                    "max_gram": 3
                },
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_ngram_filter": {
                    "type": "ngram",
                    "min_gram": 2,
                    "max_gram": 3
                }
            },
            "analyzer": {
                "rebuilt_russian": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_keywords",
                        "russian_stemmer",
                        "russian_ngram_filter"
                    ]
                },
                "english_ngram": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_ngram_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "type": {"type": "keyword"},
            "id": {"type": "keyword"},
            "attributes": {
                "properties": {
                    "name_en": {"type": "text", "analyzer": "english_ngram"},
                    "name_ru": {"type": "text", "analyzer": "rebuilt_russian"}
                }
            },
            "relationships": {
                "properties": {
                    "movies": {
                        "properties": {
                            "data": {
                                "type": "nested",
                                "properties": {
                                    "type": {"type": "keyword"},
                                    "id": {"type": "keyword"}
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
