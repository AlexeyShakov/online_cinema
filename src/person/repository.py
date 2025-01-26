from fastapi import Depends

from elasticsearch import AsyncElasticsearch

from src.elasticsearch import get_es_connection, config


class PersonRepository:
    def __init__(self, es_client: AsyncElasticsearch):
        self._search_client = es_client

    async def search_persons(
            self,
            search_value: str,
            limit: int,
            offset: int
        ):
        query = {
          "query": {
            "match": {
              "full_name": search_value
            }
          },
          "from": offset,
          "size": limit
        }
        response = await self._search_client.search(
            index=config.PERSON_INDEX_NAME,
            body=query
        )
        return response["hits"]["hits"]


def get_person_repository(
    es_client: AsyncElasticsearch = Depends(get_es_connection)
) -> PersonRepository:
    return PersonRepository(es_client=es_client)