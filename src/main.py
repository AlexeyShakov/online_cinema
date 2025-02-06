from fastapi import FastAPI

from src import global_vars, cinema
from src.logging_config import LOGGER
from src.elasticsearch_app.migrate_data_to_elastic import migrate_entities_to_elastic
from src.elasticsearch_app import (
    create_index,
    PERSON_MAPPING,
    FILMS_MAPPING,
    get_es_connection,
    close_es_connection
)

import asyncio


app = FastAPI()

app.include_router(cinema.MOVIE_ROUTES)
app.include_router(cinema.PERSON_ROUTES)


# @app.on_event("startup")
# async def startup_event():
#     if global_vars.CREATE_ELASTIC_INDEX:
#         es_client = await get_es_connection()
#         index_tasks = (
#             asyncio.Task(create_index(PERSON_MAPPING, cinema.PERSON_INDEX_NAME, es_client)),
#             asyncio.Task(create_index(FILMS_MAPPING, cinema.FILM_INDEX_NAME, es_client))
#         )
#         await asyncio.gather(*index_tasks)
#     if global_vars.TRANSFER_DATA_TO_ELASTIC:
#         es_connection = await get_es_connection()
#         transfer_tasks = (
#             asyncio.Task(
#                 migrate_entities_to_elastic(
#                     model=cinema.Person,
#                     related_obj_field_names=(cinema.FILM_INDEX_NAME, ),
#                     es_connection=es_connection,
#                     batch_size=global_vars.BATCH_SIZE_FOR_TRANSFERRING)
#             ),
#             asyncio.Task(
#                 migrate_entities_to_elastic(
#                     model=cinema.Film,
#                     related_obj_field_names=(cinema.PERSON_INDEX_NAME, "genres"),
#                     es_connection=es_connection,
#                     batch_size=global_vars.BATCH_SIZE_FOR_TRANSFERRING)
#             )
#         )
#         await asyncio.gather(*transfer_tasks)
#     LOGGER.info("startup_event отработала")


@app.on_event("shutdown")
async def shutdown_event():
    await close_es_connection()