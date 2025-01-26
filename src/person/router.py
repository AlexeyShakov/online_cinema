from fastapi import APIRouter, Query, Depends

from src.person.service import PersonsService, get_persons_service


ACTOR_ROUTES = APIRouter(
    prefix="/person",
    tags=["Actors"]
)


@ACTOR_ROUTES.get("/search")
async def search_persons(
    filter_search: str = Query(..., alias="filter[search]", description="Search term for full-text search"),
    page_number: int = Query(1, alias="page[number]", description="Page number for pagination"),
    page_size: int = Query(10, alias="page[size]", description="Number of items per page"),
    person_service: PersonsService = Depends(get_persons_service)
):
    search_result = await person_service.search_persons(filter_search, page_size, page_number)
    return {"message": search_result}
