from elasticsearch import Elasticsearch
from . import config


__ES_CLIENT = None

def get_es_connection():
    global __ES_CLIENT
    if not __ES_CLIENT:
        # TODO нужно ли создавать класс-обертку над Elasticsearch
        __ES_CLIENT = Elasticsearch(hosts=[config.ELASTIC_URL])
    return __ES_CLIENT
