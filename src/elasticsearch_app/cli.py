import typer
import asyncio

from src.elasticsearch_app.cli_utils import start_migration, create_indices
from src.logging_config import LOGGER
from src.elasticsearch_app.kinopoisk import process_kinopoisk_data



app = typer.Typer()


@app.command()
def create_elastic_indices():
    """
    Команда для взаимодействия с индексами ElasticSearch
    """
    LOGGER.info("Команда запущена")
    asyncio.run(create_indices())
    LOGGER.info("Elastic индексы созданы")


@app.command()
def migrate_data_to_elastic():
    """
    Переносит данные из мастер-базы в ElasticSearch

    Все данные для миграции берутся из .env файла. См. корунтину start_migration
    """
    LOGGER.info("Команда запущена")
    asyncio.run(start_migration())
    LOGGER.info("Данные перенесены из мастер базы в Elastic")


@app.command(name="migrate_kinopoisk_data")
def migrate_kinopoisk_data():
    """
    Переносит данные о фильмах из кинопоиска в мастер БД и в эластик
    """
    LOGGER.info("Команда запущена")
    asyncio.run(process_kinopoisk_data())
    LOGGER.info("Данные перенесены из мастер базы в Elastic")


if __name__ == "__main__":
    app()
