from fastapi import APIRouter, Query, Depends
from elasticsearch import AsyncElasticsearch

from src.elasticsearch import get_es_connection

MOVIE_ROUTES = APIRouter(
    prefix="/films",
    tags=["Movies"]
)


@MOVIE_ROUTES.get("/search")
async def search_movies(
    filter_search: str = Query(..., alias="filter[search]", description="Search term for full-text search"),
    page_number: int = Query(1, alias="page[number]", description="Page number for pagination"),
    page_size: int = Query(10, alias="page[size]", description="Number of items per page"),
    es_client: AsyncElasticsearch = Depends(get_es_connection)
):
    return {"message": "Hello films"}
