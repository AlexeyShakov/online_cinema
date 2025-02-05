import os
import asyncio
from elasticsearch import AsyncElasticsearch

from src.elasticsearch_app import get_es_connection, close_es_connection
from src.elasticsearch_app.migrate_data_to_elastic import migrate_entities_to_elastic
from dotenv import load_dotenv

from src.cinema import Film, Person

load_dotenv()

ALLOWED_MODELS_MAPPER = {
    "FILM": Film,
    "PERSON": Person
}

async def start_migration():
    es_connection = await get_es_connection()
    tasks = await _prepare_tasks(es_connection)
    await asyncio.gather(*tasks)
    await close_es_connection()


async def _prepare_tasks(es_connection: AsyncElasticsearch) -> list[asyncio.Task]:
    arguments = await _get_data_from_env(es_connection)
    tasks = []
    for args in arguments:
        task = asyncio.create_task(migrate_entities_to_elastic(*args))
        tasks.append(task)
    return tasks


async def _get_data_from_env(es_connection: AsyncElasticsearch):
    """
    TRANSFER_BATCH_SIZE - количество объектов, которое за раз берется из БД и посылается в Elastic
    MODELS_TO_TRANSFER_DATA_FROM - название моделей, описывающие таблицы в БД, где лежать сущности, которые нужно перегнать
                                    в Elastic из мастер базы. Пример: FILM,PERSON
    <model>_RELATED_FIELDS - здесь лежат название связанных(m2m или foreign key) полей для переданной модели. Если
                            MODELS_TO_TRANSFER_DATA_FROM=FILM,PERSON, то в .env должны быть еще такие переменные:
                            PERSON_RELATED_FIELDS и FILM_RELATED_FIELDS
    """
    arguments = [] # [(model, related_obj_fields, batch_size), (), ...]
    batch_size = int(os.getenv("TRANSFER_BATCH_SIZE", 500))
    models_to_transfer_data_from = os.getenv("MODELS_TO_TRANSFER_DATA_FROM")
    if not models_to_transfer_data_from:
        raise Exception("Отсутствует информация о моделях, откуда нужно перенести данные")
    models_to_transfer_data_from = [model.upper() for model in models_to_transfer_data_from.split(",")]
    for model_name in models_to_transfer_data_from:
        model = ALLOWED_MODELS_MAPPER.get(model_name)
        if not model:
            raise Exception(f"Вы указали неверную модель - {model_name}")
        related_fields = os.getenv(f"{model_name}_RELATED_FIELDS", [])
        if related_fields:
            related_fields = related_fields.split(",")
        arguments.append((model, related_fields, es_connection, batch_size))
    return arguments