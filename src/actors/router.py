from fastapi import APIRouter, Query


ACTOR_ROUTES = APIRouter(
    prefix="/actors",
    tags=["Actors"]
)


@ACTOR_ROUTES.get("/search")
async def search_actors(
    filter_search: str = Query(..., alias="filter[search]", description="Search term for full-text search"),
    page_number: int = Query(1, alias="page[number]", description="Page number for pagination"),
    page_size: int = Query(10, alias="page[size]", description="Number of items per page")
):
    return {"message": "Hello actors"}