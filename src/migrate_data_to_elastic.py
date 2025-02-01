from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src import get_db_session, Base, cinema
from src.elasticsearch import config, send_to_elastic, get_es_connection
from sqlalchemy.ext.asyncio import AsyncSession


async def migrate_entities_to_elastic(
        model: Type[Base],
        related_obj_field_name: str,
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
        data_for_sending_to_elastic = []
        async for batch in _get_batches(batch_size, session, model, related_obj_field_name):
            if model is cinema.Person:
                batch_formed_for_elastic = await _form_person_objs(batch)
            elif model is cinema.Film:
                batch_formed_for_elastic = await _form_film_objs(batch)
            else:
                raise ValueError("Неизвестный тип сущности для отправки в Elastic!")
            data_for_sending_to_elastic.append(batch_formed_for_elastic)
            es_connection = await get_es_connection()
            await send_to_elastic(batch_formed_for_elastic, es_connection)


async def _get_batches(
        batch_size: int,
        session: AsyncSession,
        model: Type[Base],
        related_obj_field_name: str,
        ) -> Sequence[Base]:
    start = 0
    while True:
        entities = await _get_entities(
            model=model,
            related_obj_field_name=related_obj_field_name,
            batch_size=batch_size,
            start=start,
            session=session
        )
        if not entities:
            break

        yield entities
        start += batch_size


async def _get_entities(
        model: Type[Base],
        related_obj_field_name: str,
        batch_size: int,
        start: int,
        session: AsyncSession
):
    stmt = select(model).options(
        selectinload(getattr(model, related_obj_field_name))
    ).offset(start).limit(batch_size)
    result = await session.scalars(stmt)
    return result.all()


async def _form_person_objs(
        persons: Sequence[cinema.Person],
) -> Sequence[dict]:
    result = []
    for person in persons:
        person_obj = {
            "_index": cinema.PERSON_INDEX_NAME,
            "_source": {
                "person_id": person.id,
                "full_name": person.full_name
            }
        }
        films = person.films
        person_films = []
        for film in films:
            person_films.append({"film_id": film.id, "title": film.title})
        person_obj["_source"]["films"] = person_films
        result.append(person_obj)
    return result


async def _form_film_objs(
        films: Sequence[cinema.Film],
) -> Sequence[dict]:
    result = []
    for film in films:
        film_obj = {
            "_index": cinema.FILM_INDEX_NAME,
            "_source": {
                "film_id": film.id,
                "title": film.title
            }
        }
        persons = film.persons
        persons_for_result = []
        for person in persons:
            persons_for_result.append({"person_id": person.id, "full_name": person.full_name})
        film_obj["_source"]["persons"] = persons_for_result
        result.append(film_obj)
    return result
