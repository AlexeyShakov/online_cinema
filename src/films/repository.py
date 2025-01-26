from typing import Sequence

from fastapi import Depends

from elasticsearch import AsyncElasticsearch

from src.elasticsearch import get_es_connection, config


class FilmRepository:
    def __init__(self, es_client: AsyncElasticsearch):
        self._search_client = es_client

    async def search_films(
            self,
            search_value: str,
            limit: int,
            offset: int
        ) -> Sequence:
        query = {
          "query": {
            "match": {
              "title": search_value
            }
          },
          "from": offset,
          "size": limit
        }
        response = await self._search_client.search(
            index=config.FILM_INDEX_NAME,
            body=query
        )
        return response["hits"]["hits"]


def get_film_repository(
    es_client: AsyncElasticsearch = Depends(get_es_connection)
) -> FilmRepository:
    return FilmRepository(es_client=es_client)
