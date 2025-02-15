from typing import Sequence, Type
from elasticsearch.exceptions import RequestError, BadRequestError
from elasticsearch import AsyncElasticsearch

from elasticsearch.helpers import async_bulk

from src.logging_config import LOGGER
from src import cinema


class ElasticCommunicator:
    @staticmethod
    async def create_index(mapping: dict, index_name: str, es_client: AsyncElasticsearch) -> None:
        if not await es_client.indices.exists(index=index_name):
            try:
                await es_client.indices.create(index=index_name, body=mapping,
                                               headers={"Content-Type": "application/json"})
                LOGGER.info(f"Индекс '{index_name}' успешно создан")
            except RequestError as e:
                LOGGER.exception(f"Ошибка при создании индекса '{index_name}': {e}")
            except BadRequestError as e:
                LOGGER.exception(f"Ошибка в отправляемых данных '{index_name}': {e}")
        else:
            LOGGER.info(f"Индекс '{index_name}' уже существует")

    @staticmethod
    async def send_to_elastic(batch: Sequence[dict], client: AsyncElasticsearch) -> None:
        try:
            await async_bulk(client, batch)
        except Exception as e:
            LOGGER.exception(f"Ошибка при создании сущностей в Elastic: {e}")

    @staticmethod
    async def form_person_objs(persons: Sequence[cinema.Person]) -> Sequence[dict]:
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

    @staticmethod
    async def form_film_objs(films: Sequence[cinema.Film]) -> Sequence[dict]:
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


async def get_elastic_communicator() -> ElasticCommunicator:
    return ElasticCommunicator()
