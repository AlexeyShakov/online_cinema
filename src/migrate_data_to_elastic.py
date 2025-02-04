from typing import Sequence, Type, Union

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src import get_db_session, Base, cinema
from src.elasticsearch import send_to_elastic, get_es_connection
from sqlalchemy.ext.asyncio import AsyncSession


async def migrate_entities_to_elastic(
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
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
        async for batch in _get_batches(batch_size, session, model, related_obj_field_names):
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
        model: Type[Union[cinema.Film, cinema.Person]],
        related_obj_field_names: Sequence[str],
        ) -> Sequence[Base]:
    start = 0
    while True:
        entities = await _get_entities(
            model=model,
            related_obj_field_names=related_obj_field_names,
            batch_size=batch_size,
            start=start,
            session=session
        )
        if not entities:
            break

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


async def _form_person_objs(
        persons: Sequence[cinema.Person],
) -> Sequence[dict]:
    result = []
    for person in persons:
        person_obj = {
            "_index": cinema.PERSON_INDEX_NAME,
            "_source": {
                "type": "actors",
                "id": person.id,
                "attributes": {
                    "name": person.full_name,
                },
                "relationships": {
                    "movies": {}
                }
            }
        }
        films = person.films
        person_films = []
        for film in films:
            person_films.append({"id": film.id, "type": "string"})
        person_obj["_source"]["relationships"]["movies"]["data"] = person_films
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
                "id": film.id,
                "type": "movies",
                "attributes": {
                    "title": film.title,
                    "description": film.description,
                },
                "relationships": {
                    "actors": {}
                }
                },
        }
        genres = film.genres
        genres_for_result = []
        for genre in genres:
            genres_for_result.append(genre.id)
        film_obj["_source"]["attributes"]["category_ids"] = genres_for_result

        persons = film.persons
        persons_for_result = []
        for person in persons:
            persons_for_result.append({"id": person.id, "type": "string"})
        film_obj["_source"]["relationships"]["actors"]["data"] = persons_for_result
        result.append(film_obj)
    return result
