from typing import Sequence

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError,BadRequestError
from elasticsearch.helpers import bulk

import logging


def create_index(mapping: dict, index_name: str, es_client: Elasticsearch) -> None:
    if not es_client.indices.exists(index=index_name):
        try:
            es_client.indices.create(index=index_name, body=mapping)
            logging.info(f"Индекс '{index_name}' успешно создан")
        except RequestError as e:
            logging.exception(f"Ошибка при создании индекса '{index_name}': {e}")
        except BadRequestError as e:
            logging.exception(f"Ошибка в отправляемых данных '{index_name}': {e}")
    else:
        logging.info(f"Индекс '{index_name}' уже существует")


def send_to_elastic(batch: Sequence[dict], client: Elasticsearch) -> None:
    print("Я ТУТ")
    try:
        bulk(client, batch)
    except Exception as e:
        logging.exception(f"Ошибка при создании сущностей в Elastic: {e}")
