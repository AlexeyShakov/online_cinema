from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.person import Person
from src.films import Film
from src import get_db_session, Base
from src.elasticsearch import config, send_to_elastic, get_es_connection


def migrate_entities_to_elastic(
        model: Type[Base],
        related_obj_field_name: str,
        batch_size: int,
) -> None:
    """
    Пример объекта на примере персоны(Person):
    {
        "person_sql_id": "str",
        "full_name": "str",
        "films": [
            {"film_sql_id": "str", "title": "str"},
            {...},
            {...}
        ]
    }
    """
    session_generator = get_db_session()
    session = next(session_generator)
    try:
        for batch in _get_batches(batch_size, session, model, related_obj_field_name):
            if model is Person:
                batch_formed_for_elastic = _form_person_objs(batch)
            elif model is Film:
                batch_formed_for_elastic = _form_film_objs(batch)
            else:
                raise ValueError("Неизвестный тип сущности для отправки в Elastic!")
            send_to_elastic(batch_formed_for_elastic, get_es_connection())
    finally:
        next(session_generator, None)


def _get_batches(
        batch_size: int,
        session: Session,
        model: Type[Base],
        related_obj_field_name: str,
        ) -> Sequence[Base]:
    start = 0
    while True:
        stmt = select(model).options(
            selectinload(getattr(model, related_obj_field_name))
        ).offset(start).limit(batch_size)

        # Если бы использовал PostgreSQL, можно было бы оптимизировать получение персон
        # с помощью server-side cursor - yield_per(batch_size) вместо all()
        persons = session.scalars(stmt).all()
        if not persons:
            break

        yield persons
        start += batch_size


def _form_person_objs(
        persons: Sequence[Person],
) -> Sequence[dict]:
    result = []
    for person in persons:
        person_obj = {
            "_index": config.PERSON_INDEX_NAME,
            "_source": {
                "person_sql_id": person.id,
                "full_name": person.full_name
            }
        }
        films = person.films
        person_films = []
        for film in films:
            person_films.append({"film_sql_id": film.id, "title": film.title})
        person_obj["_source"]["films"] = person_films
        result.append(person_obj)
    return result


def _form_film_objs(
        films: Sequence[Film],
) -> Sequence[dict]:
    result = []
    for film in films:
        film_obj = {
            "_index": config.FILM_INDEX_NAME,
            "_source": {
                "film_sql_id": film.id,
                "title": film.title
            }
        }
        persons = film.persons
        persons_for_result = []
        for person in persons:
            persons_for_result.append({"person_sql_id": person.id, "full_name": person.full_name})
        film_obj["_source"]["persons"] = persons_for_result
        result.append(film_obj)
    return result
