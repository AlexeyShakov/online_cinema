import os
import asyncio
from typing import Dict, Literal

from elasticsearch import AsyncElasticsearch

from src.elasticsearch_app import get_es_connection, close_es_connection, indices
from src.elasticsearch_app.elastic_communication import get_elastic_communicator
from src.elasticsearch_app.migrate_data_to_elastic import etl_films, etl_persons
from src import cinema
from src.settings import get_elastic_settings

from dotenv import load_dotenv


load_dotenv()

ELASTIC_SETTINGS = get_elastic_settings()


ALLOWED_MODELS_MAPPER = {
    "films": cinema.Film,
    "persons": cinema.Person
}

async def start_migration() -> None:
    es_connection = await get_es_connection()
    tasks = await _prepare_tasks(es_connection)
    await asyncio.gather(*tasks)
    await close_es_connection()


async def _prepare_tasks(es_connection: AsyncElasticsearch) -> list[asyncio.Task]:
    arguments = await _get_data_from_env(es_connection)
    tasks = []
    tasks.append(asyncio.create_task(etl_films(*arguments.get("films"))))
    tasks.append(asyncio.create_task(etl_persons(*arguments.get("persons"))))
    return tasks


async def _get_data_from_env(es_connection: AsyncElasticsearch) -> Dict[Literal["FILMS", "PERSONS"], tuple]:
    """
    TRANSFER_BATCH_SIZE - количество объектов, которое за раз берется из БД и посылается в Elastic
    MODELS_TO_TRANSFER_DATA_FROM - название моделей, описывающие таблицы в БД, где лежать сущности, которые нужно перегнать
                                    в Elastic из мастер базы. Пример: FILM,PERSON
    <model>_RELATED_FIELDS - здесь лежат название связанных(m2m или foreign key) полей для переданной модели. Если
                            MODELS_TO_TRANSFER_DATA_FROM=FILM,PERSON, то в .env должны быть еще такие переменные:
                            PERSON_RELATED_FIELDS и FILM_RELATED_FIELDS
    """
    arguments = {}
    language = "en"
    batch_size = ELASTIC_SETTINGS.transfer_batch_size
    models_to_transfer_data_from = ELASTIC_SETTINGS.models_to_transfer_data_from
    cursor = {"column_name": "id", "value_to_start_from": None}
    if not models_to_transfer_data_from:
        raise Exception("Отсутствует информация о моделях, откуда нужно перенести данные")
    for model_name in models_to_transfer_data_from:
        model = ALLOWED_MODELS_MAPPER.get(model_name)
        if not model:
            raise Exception(f"Вы указали неверную модель - {model_name}")
        related_fields = getattr(ELASTIC_SETTINGS, f"{model_name}_related_fields")
        arguments[model_name] = (model, related_fields, es_connection, batch_size, language, cursor)
    return arguments

async def create_indices() -> None:
    es_connection = await get_es_connection()
    elastic_communicator = await get_elastic_communicator()
    tasks = (
        asyncio.Task(elastic_communicator.create_index(indices.PERSON_MAPPING, ELASTIC_SETTINGS.person_index_name, es_connection)),
        asyncio.Task(elastic_communicator.create_index(indices.FILMS_MAPPING, ELASTIC_SETTINGS.film_index_name, es_connection))
    )
    try:
        await asyncio.gather(*tasks)
    finally:
        await close_es_connection()
