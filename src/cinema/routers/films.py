from fastapi import APIRouter, Query, Depends

from src.cinema.services import FilmService, get_films_service
from src.cinema.schemas import MoviesResponse


MOVIE_ROUTES = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@MOVIE_ROUTES.get("/search", response_model=MoviesResponse, description="Search Movies")
async def search_movies(
    filter_search: str = Query(..., alias="filter[search]", description="Search term for full-text search"),
    page_number: int = Query(1, alias="page[number]", description="Page number for pagination"),
    page_size: int = Query(10, alias="page[size]", description="Number of items per page"),
    film_service: FilmService = Depends(get_films_service)
):
    search_result = await film_service.search_films(filter_search, page_size, page_number)
    return search_result
