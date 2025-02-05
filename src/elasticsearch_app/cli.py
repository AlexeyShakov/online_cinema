import typer
import asyncio

from src.elasticsearch_app.cli_utils import start_migration


app = typer.Typer()


@app.command()
def migrate_data_to_elastic():
    """
    Переносит данные из мастер-базы в ElasticSearch

    Все данные для миграции берутся из .env файла. См. корунтину start_migration
    """
    asyncio.run(start_migration())

if __name__ == "__main__":
    app()
