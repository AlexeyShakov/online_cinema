from typing import Sequence, Type, Union
from elasticsearch import AsyncElasticsearch

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.models import Base
from src.database import get_db_session
from src import cinema
from src.elasticsearch_app.elastic_communication import get_elastic_communicator
from sqlalchemy.ext.asyncio import AsyncSession


async def migrate_entities_to_elastic(
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
        es_connection: AsyncElasticsearch,
        batch_size: int,
) -> None:
    """
    Пример объекта на примере персоны(Person):
    {
        "person_id": "str",
        "full_name": "str",
        "films": [
            {"film_id": "str", "title": "str"},
            {...},
            {...}
        ]
    }
    """
    async for session in get_db_session():
        row_total_count = await get_row_total_count(session, model)
        elastic_communicator = await get_elastic_communicator()
        async for batch in _get_batches(batch_size, session, model, related_obj_field_names, row_total_count):
            if model is cinema.Person:
                batch_formed_for_elastic = await elastic_communicator.form_person_objs(batch)
            elif model is cinema.Film:
                batch_formed_for_elastic = await elastic_communicator.form_film_objs(batch)
            else:
                raise ValueError("Неизвестный тип сущности для отправки в Elastic!")
            await elastic_communicator.send_to_elastic(batch_formed_for_elastic, es_connection)


async def _get_batches(
        batch_size: int,
        session: AsyncSession,
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
        row_total_count: int
) -> Sequence[Base]:
    start = 0

    while start < row_total_count:
        entities = await _get_entities(
            model=model,
            related_obj_field_names=related_obj_field_names,
            batch_size=batch_size,
            start=start,
            session=session
        )
        yield entities
        start += batch_size


async def _get_entities(
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
        batch_size: int,
        start: int,
        session: AsyncSession
):
    stmt = select(model)

    for field_name in related_obj_field_names:
        stmt = stmt.options(selectinload(getattr(model, field_name)))

    stmt = stmt.offset(start).limit(batch_size)

    result = await session.scalars(stmt)
    return result.all()


async def get_row_total_count(session: AsyncSession, model: Type[Union[cinema.Film, cinema.Person]]) -> int:
    total_count_stmt = select(func.count()).select_from(model)
    result = await session.execute(total_count_stmt)
    return result.scalar_one()
