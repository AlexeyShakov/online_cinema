from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.cinema.schemas import PersonDataResponse, MoviesResponse
from src import cinema
from src.elasticsearch_app import get_es_connection
from src.cinema.config import PERSON_INDEX_NAME, FILM_INDEX_NAME

FILMS = Sequence[cinema.Film]
PERSONS = Sequence[cinema.Person]


async def prepare_data_after_elastic(data: dict, pagination_data: dict) -> dict:
    """
    Избавляемся от лишней вложенности(_source) и добавляем информацию о метаданных
    """
    result = {"meta": {"pagination": pagination_data}}
    if data:
        result["data"] = [el["_source"] for el in data]
    else:
        result["data"] = []
    return result


class FilmRepository:
    @staticmethod
    async def search_films(
            search_value: str,
            limit: int,
            offset: int
    ) -> MoviesResponse:
        elastic_client = await get_es_connection()
        query = {
            "query": {
                "multi_match": {
                    "query": search_value,
                    "type": "best_fields",
                    "fields": ["attributes.title_ru", "attributes.title_en"]
                }
            },
            "from": offset,
            "size": limit
        }
        response = await elastic_client.search(
            index=FILM_INDEX_NAME,
            body=query,
            filter_path="hits.hits._source,hits.total"
        )
        result = await prepare_data_after_elastic(
            data=response["hits"].get("hits"),
            pagination_data={
                "offset": offset,
                "limit": limit,
                "total": response["hits"]["total"]["value"]

            }
        )
        return MoviesResponse(**result)

    @staticmethod
    async def bulk_create(films: FILMS, session: AsyncSession) -> FILMS:
        session.add_all(films)
        await session.commit()
        return films

    @classmethod
    async def create_film_genre_relations(cls, films: FILMS, session: AsyncSession) -> None:
        genre = await cls._get_genre(session)
        today_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)
        today_datetime = today_datetime.strftime("%Y-%m-%d %H:%M:%S.%f+00")
        relations = [
            cinema.MovieGenreRelation(
                film_work_id=film.id,
                genre_id=genre.id,
                created_at=today_datetime,
            )
            for film in films
        ]
        session.add_all(relations)
        await session.commit()

    @staticmethod
    async def _get_genre(session: AsyncSession) -> cinema.Genre:
        # Для учебных целях возьмем только один жанр
        stmt = select(cinema.Genre).limit(1)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def create_film_person_relations(relations: Sequence[cinema.PersonFilmRelation],
                                           session: AsyncSession) -> None:
        session.add_all(relations)
        await session.commit()

    @staticmethod
    async def fetch_with_related_fields(films: FILMS, related_fields: Sequence[str], session: AsyncSession) -> FILMS:
        film_ids = [film.id for film in films]
        options = [selectinload(getattr(cinema.Film, field)) for field in related_fields]
        stmt = (
            select(cinema.Film)
            .options(*options)
            .where(cinema.Film.id.in_(film_ids))
        )
        result = await session.execute(stmt)
        return result.scalars().all()


class PersonRepository:
    @staticmethod
    async def search_persons(
            search_value: str,
            limit: int,
            offset: int
    ) -> PersonDataResponse:
        elastic_client = await get_es_connection()
        query = {
            "query": {
                "multi_match": {
                    "query": search_value,
                    "type": "best_fields",
                    "fields": ["attributes.name_ru", "attributes.name_en"]
                }
            },
            "from": offset,
            "size": limit,
        }
        response = await elastic_client.search(
            index=PERSON_INDEX_NAME,
            body=query,
            filter_path="hits.hits._source,hits.total"
        )
        result = await prepare_data_after_elastic(
            data=response["hits"].get("hits"),
            pagination_data={
                "offset": offset,
                "limit": limit,
                "total": response["hits"]["total"]["value"]

            }
        )
        return PersonDataResponse(**result)

    @staticmethod
    async def bulk_create(persons: PERSONS, session: AsyncSession) -> PERSONS:
        session.add_all(persons)
        await session.commit()
        return persons

    @staticmethod
    async def fetch_with_related_fields(persons: PERSONS, related_fields: Sequence[str], session: AsyncSession) -> PERSONS:
        person_ids = [person.id for person in persons]
        options = [selectinload(getattr(cinema.Person, field)) for field in related_fields]
        stmt = (
            select(cinema.Person)
            .options(*options)
            .where(cinema.Person.id.in_(person_ids))
        )
        result = await session.execute(stmt)
        return result.scalars().all()


def get_person_repository() -> PersonRepository:
    return PersonRepository()


def get_film_repository() -> FilmRepository:
    return FilmRepository()
