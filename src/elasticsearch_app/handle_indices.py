from elasticsearch.exceptions import RequestError,BadRequestError
from elasticsearch import AsyncElasticsearch

from src.logging_config import LOGGER


async def create_index(mapping: dict, index_name: str, es_client: AsyncElasticsearch) -> None:
    if not await es_client.indices.exists(index=index_name):
        try:
            await es_client.indices.create(index=index_name, body=mapping, headers={"Content-Type": "application/json"})
            LOGGER.info(f"Индекс '{index_name}' успешно создан")
        except RequestError as e:
            LOGGER.exception(f"Ошибка при создании индекса '{index_name}': {e}")
        except BadRequestError as e:
            LOGGER.exception(f"Ошибка в отправляемых данных '{index_name}': {e}")
    else:
        LOGGER.info(f"Индекс '{index_name}' уже существует")
