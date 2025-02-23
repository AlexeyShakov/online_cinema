from typing import Sequence, Type, Union, Literal, Optional
from elasticsearch import AsyncElasticsearch

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.database import get_db_session
from src import cinema
from src.elasticsearch_app import data_types
from src.elasticsearch_app.elastic_communication import get_elastic_communicator


async def etl_films(
        model: cinema.Film,
        related_obj_field_names: Sequence[str],
        es_connection: AsyncElasticsearch,
        batch_size: int,
        language: Literal["ru", "en"],
        cursor: data_types.CursorForGettingBatches
) -> None:
    elastic_communicator = await get_elastic_communicator()
    async for batch in _get_batches(batch_size, model, related_obj_field_names, cursor):
        transformed_batch = await elastic_communicator.form_film_objs(batch, language)
        await elastic_communicator.send_to_elastic(transformed_batch, es_connection)


async def etl_persons(
        model: cinema.Person,
        related_obj_field_names: Sequence[str],
        es_connection: AsyncElasticsearch,
        batch_size: int,
        language: Literal["ru", "en"],
        cursor: data_types.CursorForGettingBatches
) -> None:
    elastic_communicator = await get_elastic_communicator()
    async for batch in _get_batches(batch_size, model, related_obj_field_names, cursor):
        transformed_batch = await elastic_communicator.form_person_objs(batch, language)
        await elastic_communicator.send_to_elastic(transformed_batch, es_connection)


async def _get_batches(
        batch_size: int,
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
        cursor: data_types.CursorForGettingBatches
) -> Sequence[Union[cinema.Film, cinema.Person]]:
    while True:
        entities = await _get_entities(
            model=model,
            related_obj_field_names=related_obj_field_names,
            batch_size=batch_size,
            cursor=cursor,
        )
        if not entities:
            break
        yield entities
        cursor["value_to_start_from"] = getattr(entities[-1], cursor["column_name"])

async def _get_entities(
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
        batch_size: int,
        cursor: data_types.CursorForGettingBatches
):
    async for session in get_db_session():
        stmt = select(model)

        for field_name in related_obj_field_names:
            stmt = stmt.options(selectinload(getattr(model, field_name)))

        if cursor["value_to_start_from"] is not None:
            stmt = stmt.where(getattr(model, cursor["column_name"]) > cursor["value_to_start_from"])

        stmt = stmt.order_by(getattr(model, cursor["column_name"]).asc()).limit(batch_size)

        result = await session.scalars(stmt)
        return result.all()


async def get_row_total_count(model: Type[Union[cinema.Film, cinema.Person]]) -> int:
    async for session in get_db_session():
        total_count_stmt = select(func.count()).select_from(model)
        result = await session.execute(total_count_stmt)
        return result.scalar_one()
