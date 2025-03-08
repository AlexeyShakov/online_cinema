from typing import Callable

from fastapi import APIRouter, Query, Depends

from src.cinema.services import FilmService, get_films_service
from src.cinema.to_json_schemas import MoviesResponse
from src.cinema.serializers import from_python_to_json


movie_routes = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@movie_routes.get("/search", response_model=MoviesResponse, description="Search Movies")
async def search_movies(
    filter_search: str = Query(..., alias="filter[search]", description="Search term for full-text search"),
    page_size: int = Query(10, alias="page[size]", description="Number of items per page"),
    page_number: int = Query(1, alias="page[number]", description="Page number for pagination"),
    film_service: FilmService = Depends(get_films_service),
    serializer: Callable = Depends(from_python_to_json.get_films_to_json_serializer)
):
    search_result = await film_service.search_films(filter_search, page_size, page_number)
    response = serializer(MoviesResponse, search_result, {"limit": page_size, "offset": page_number})
    return response
