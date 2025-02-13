from fastapi import Depends

from elasticsearch import AsyncElasticsearch

from src.cinema.schemas import PersonDataResponse, MoviesResponse
from src.elasticsearch_app import get_es_connection
from src.cinema.config import PERSON_INDEX_NAME, FILM_INDEX_NAME


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
    def __init__(self, es_client: AsyncElasticsearch):
        self._search_client = es_client

    async def search_films(self,
                           search_value: str,
                           limit: int,
                           offset: int
                           ) -> MoviesResponse:
        query = {
            "query": {
                "match": {
                    "attributes.title": search_value
                }
            },
            "from": offset,
            "size": limit
        }
        response = await self._search_client.search(
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


class PersonRepository:
    def __init__(self, es_client: AsyncElasticsearch):
        self._search_client = es_client

    async def search_persons(
            self,
            search_value: str,
            limit: int,
            offset: int
    ) -> PersonDataResponse:
        query = {
            "query": {
                "match": {
                    "attributes.name": search_value
                }
            },
            "from": offset,
            "size": limit
        }
        response = await self._search_client.search(
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


def get_person_repository(
        es_client: AsyncElasticsearch = Depends(get_es_connection)
) -> PersonRepository:
    return PersonRepository(es_client=es_client)


def get_film_repository(
        es_client: AsyncElasticsearch = Depends(get_es_connection)
) -> FilmRepository:
    return FilmRepository(es_client=es_client)
