from fastapi import APIRouter, Query, Depends

from src.cinema.services import PersonsService, get_persons_service
from src.cinema.schemas import PersonDataResponse


PERSON_ROUTES = APIRouter(
    prefix="/actors",
    tags=["Actors"]
)


@PERSON_ROUTES.get("/search", response_model=PersonDataResponse, description="Search Actors")
async def search_persons(
    filter_search: str = Query(..., alias="filter[search]", description="Search term for full-text search"),
    page_number: int = Query(1, alias="page[number]", description="Page number for pagination"),
    page_size: int = Query(10, alias="page[size]", description="Number of items per page"),
    person_service: PersonsService = Depends(get_persons_service)
):
    search_result = await person_service.search_persons(filter_search, page_size, page_number)
    return search_result
