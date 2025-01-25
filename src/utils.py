from typing import List, Sequence, Type, Union

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.person import Person
from src.films import Film
from src import get_db_session, Base


def migrate_persons_to_elastic(
        model: Type[Base],
        related_obj_field_name: str,
        batch_size: int,
) -> None:
    session_generator = get_db_session()
    session = next(session_generator)
    try:
        result = []
        for batch in _get_batches(batch_size, session, model, related_obj_field_name):
            if model is Person:
                _form_person_objs(batch, result)
            elif model is Film:
                _form_film_objs(batch, result)
            else:
                raise ValueError("Неизвестный тип сущности для отправки в Elastic!")
    finally:
        next(session_generator, None)


def _get_batches(
        batch_size: int,
        session: Session,
        model: Type[Base],
        related_field: str,
        ) -> Sequence[Base]:
    start = 0
    while True:
        stmt = select(model).options(
            selectinload(getattr(model, related_field))
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
        result: List,
) -> None:
    for person in persons:
        person_obj = {"person_sql_id": person.id, "full_name": person.full_name}
        films = person.films
        person_films = []
        for film in films:
            person_films.append({"film_sql_id": film.id, "title": film.title})
        person_obj["films"] = person_films
        result.append(person_obj)


def _form_film_objs(
        films: Sequence[Film],
        result: List
) -> None:
    for film in films:
        film_obj = {"film_sql_id": film.id, "title": film.title}
        persons = film.persons
        persons_for_result = []
        for person in persons:
            persons_for_result.append({"person_sql_id": person.id, "full_name": person.full_name})
        film_obj["persons"] = persons_for_result
        result.append(film_obj)
