from fastapi import FastAPI

from src.films import MOVIE_ROUTES
from src.person import ACTOR_ROUTES

from src import Film, Person, global_vars
from src.logging_config import LOGGER
from src.utils import migrate_entities_to_elastic
from src.elasticsearch import (
    create_index,
    PERSON_MAPPING,
    FILMS_MAPPING,
    config,
    get_es_connection,
    close_es_connection
)

import asyncio


app = FastAPI()

app.include_router(MOVIE_ROUTES)
app.include_router(ACTOR_ROUTES)


@app.on_event("startup")
async def startup_event():
    if global_vars.CREATE_ELASTIC_INDEX:
        es_client = await get_es_connection()
        index_tasks = (
            asyncio.Task(create_index(PERSON_MAPPING, config.PERSON_INDEX_NAME, es_client)),
            asyncio.Task(create_index(FILMS_MAPPING, config.FILM_INDEX_NAME, es_client))
        )
        await asyncio.gather(*index_tasks)
    if global_vars.TRANSFER_DATA_TO_ELASTIC:
        transfer_tasks = (
            asyncio.Task(
                migrate_entities_to_elastic(Person, config.FILM_INDEX_NAME, global_vars.BATCH_SIZE_FOR_TRANSFERRING)
            ),
            asyncio.Task(
                migrate_entities_to_elastic(Film, config.PERSON_INDEX_NAME, global_vars.BATCH_SIZE_FOR_TRANSFERRING)
            )

        )
        await asyncio.gather(*transfer_tasks)
    LOGGER.info("startup_event отработала")


@app.on_event("shutdown")
async def shutdown_event():
    await close_es_connection()