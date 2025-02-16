import asyncio
import os
from typing import Set, Dict, List, Literal, Sequence
from datetime import datetime, timezone
from elasticsearch import AsyncElasticsearch

import pandas as pd

from src import cinema
from src.database import get_db_session
from src.elasticsearch_app.connection import get_es_connection, close_es_connection
from src.elasticsearch_app.elastic_communication import get_elastic_communicator
from src.logging_config import LOGGER

FILMS = Sequence[cinema.Film]
PERSONS = Sequence[cinema.Person]
FILM_PERSON_RELATION = Dict[str, Dict[str, List[str]]]


class KinopoiskDataMigrator:
    def __init__(self, df: pd.DataFrame, es_connection: AsyncElasticsearch) -> None:
        self._df = df
        self._es_connection = es_connection

        self._unique_persons: Set[str] = set()
        self._films: List[str] = []
        self._films_persons_relation: FILM_PERSON_RELATION = {}  # {"movie_title": {"actor_name": [roles]}

        self._for_creating_persons: List[cinema.Person] = []
        self._for_creating_movies: List[cinema.Film] = []

    async def process(self):
        today_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)
        today_datetime = today_datetime.strftime("%Y-%m-%d %H:%M:%S.%f+00")

        await self._prepare_data_for_creating(self._df, today_datetime)
        films, persons = await asyncio.gather(
            asyncio.Task(self._create_films(self._for_creating_movies)),
            asyncio.Task(self._create_persons(self._for_creating_persons))
        )
        LOGGER.info("Создали фильмы и персоны в мастер БД")
        await asyncio.gather(
            asyncio.Task(self._create_film_genre_relations(films)),
            asyncio.Task(
                self._create_film_person_relation(films, persons, self._films_persons_relation, today_datetime))
        )
        films, persons = await asyncio.gather(
            asyncio.Task(self._get_films_with_related_data(films)),
            asyncio.Task(self._get_persons_with_related_data(persons)),
        )
        LOGGER.info("Создали связи фильмов с жанрами и персонами")
        await self._send_to_elastic(films, persons, self._es_connection)
        LOGGER.info("Отправили данные в эластик")

    async def _prepare_data_for_creating(self, df: pd.DataFrame, today_datetime: str) -> None:
        for index, row in df.iterrows():
            await self._prepare_films(row, today_datetime)
            await self._prepare_all_persons_types(row, today_datetime)

    async def _prepare_films(self, row, current_datetime: str):
        movie_title = row["movie"]
        self._films_persons_relation[movie_title] = {}
        movie = cinema.Film(
            title=movie_title,
            description=row["overview"],
            creation_date=None,
            file_path=None,
            rating=row["rating_ball"],
            type="movie",
            created_at=current_datetime,
            updated_at=current_datetime
        )
        self._for_creating_movies.append(movie)
        self._films.append(movie_title)

    async def _prepare_all_persons_types(self, row, current_datetime: str) -> None:
        movie = row["movie"]
        await self._prepare_persons(row["director"].split(";"), current_datetime, movie, "director")
        await self._prepare_persons(row["screenwriter"].split(";"), current_datetime, movie, "writer")
        await self._prepare_persons(row["actors"].split(";"), current_datetime, movie, "actor")

    async def _prepare_persons(self, persons: List[str], current_datetime: str, movie: str,
                               role: Literal["actor", "director", "writer"]) -> None:
        for person in persons:
            person = person.strip()
            if person not in self._unique_persons:
                self._unique_persons.add(person)
                person_obj = cinema.Person(
                    full_name=person,
                    created_at=current_datetime,
                    updated_at=current_datetime
                )
                self._for_creating_persons.append(person_obj)
            if person in self._films_persons_relation[movie]:
                self._films_persons_relation[movie][person].append(role)
            else:
                self._films_persons_relation[movie][person] = [role]

    async def _create_films(self, films: FILMS) -> FILMS:
        async for session in get_db_session():
            films = await cinema.FilmRepository.bulk_create(films, session)
            return films

    async def _create_persons(self, persons: PERSONS) -> PERSONS:
        async for session in get_db_session():
            persons = await cinema.PersonRepository.bulk_create(persons, session)
            return persons

    async def _create_film_genre_relations(self, films: FILMS) -> None:
        async for session in get_db_session():
            await cinema.FilmRepository.create_film_genre_relations(films, session)

    async def _create_film_person_relation(self, films: FILMS, persons: PERSONS,
                                           film_person_relation: FILM_PERSON_RELATION,
                                           today_datetime: str) -> None:
        persons_by_full_name = {person.full_name: person for person in persons}
        for_bulk_creation = []
        for film in films:
            film_person_info = film_person_relation.get(film.title)
            for person, roles in film_person_info.items():
                person_obj = persons_by_full_name.get(person)
                for role in roles:
                    relation_obj = cinema.PersonFilmRelation(
                        film_work_id=film.id,
                        person_id=person_obj.id,
                        role=role,
                        created_at=today_datetime
                    )
                    for_bulk_creation.append(relation_obj)
        async for session in get_db_session():
            await cinema.FilmRepository.create_film_person_relations(for_bulk_creation, session)

    async def _send_to_elastic(self, films: FILMS, persons: PERSONS, es_connection: AsyncElasticsearch) -> None:
        elastic_communicator = await get_elastic_communicator()
        films_data = await elastic_communicator.form_film_objs(films)
        persons_data = await elastic_communicator.form_person_objs(persons)
        await asyncio.gather(
            asyncio.Task(elastic_communicator.send_to_elastic(films_data, es_connection)),
            asyncio.Task(elastic_communicator.send_to_elastic(persons_data, es_connection)),
        )

    async def _get_films_with_related_data(self, films: FILMS) -> FILMS:
        async for session in get_db_session():
            return await cinema.FilmRepository.fetch_with_related_fields(films, ("genres", "persons"), session)

    async def _get_persons_with_related_data(self, persons: PERSONS) -> PERSONS:
        async for session in get_db_session():
            return await cinema.PersonRepository.fetch_with_related_fields(persons, ("films", ), session)


async def process_kinopoisk_data():
    es_connection = await get_es_connection()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'kinopoisk-top250.csv')
    df = pd.read_csv(file_path, usecols=('rating_ball', 'movie', "overview", "director", "actors", "screenwriter"))
    migrator = KinopoiskDataMigrator(df, es_connection)
    await migrator.process()
    await close_es_connection()
