from elasticsearch import Elasticsearch, AsyncElasticsearch

from . import config
from src import LOGGER


__ES_CLIENT = None


async def get_es_connection():
    global __ES_CLIENT
    # TODO нужно ли создавать класс-обертку над Elasticsearch
    if not __ES_CLIENT:
        __ES_CLIENT = AsyncElasticsearch(hosts=[config.ELASTIC_URL])
        await _check_health(__ES_CLIENT)
    return __ES_CLIENT


async def reconnect_to_es():
    global __ES_CLIENT
    new_client = AsyncElasticsearch(hosts=[config.ELASTIC_URL])
    await _check_health(new_client)
    __ES_CLIENT = new_client
    LOGGER.info("Новое соединение к Elastic усспешно установлено")


async def _check_health(client: AsyncElasticsearch):
    health = await client.cluster.health()
    LOGGER.info(f"Успешное подключение к Elastic. Проверка health: {health['status']}")

async def close_es_connection():
    global __ES_CLIENT
    if __ES_CLIENT:
        await __ES_CLIENT.close()
        LOGGER.info("Соединение с Elastic успешно закрыто")
        __ES_CLIENT = None
    else:
        LOGGER.info("Соединение с Elastic уже закрыто")
