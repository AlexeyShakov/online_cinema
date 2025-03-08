from src.cinema.datastructs.elastic_datastructs import general
from src.cinema.datastructs import from_elastic_to_python
from src.cinema.to_json_schemas import films
from src.general_usage import jsonapi_schemas

from typing import Type, Callable


def convert_dataclass_to_pydantic(response_scheme: Type[films.MoviesResponse], movies: from_elastic_to_python.Movies,
                                  pagination_data: general.PaginationDict) -> films.MoviesResponse:
    pagination = jsonapi_schemas.Pagination(total=movies.meta.total, **pagination_data)
    meta = jsonapi_schemas.Meta(pagination=pagination)
    pydantic_movies = [
        films.Movie(
            id=movie.id,
            type=movie.type,
            attributes=films.Attributes(
                title_ru=movie.attributes.title_ru,
                title_en=movie.attributes.title_en,
                description=movie.attributes.description,
                category_ids=movie.attributes.category_ids
            ),
            relationships=films.Relationships(
                actors=films.ActorsRelationship(
                    data=[films.ActorData(id=actor.id, type=actor.type) for actor in movie.attributes.actors]
                )
            )
        )
        for movie in movies.data
    ]
    return response_scheme(meta=meta, data=pydantic_movies)


def get_films_to_json_serializer() -> Callable[
    [Type[films.MoviesResponse], from_elastic_to_python.Movies, general.PaginationDict], films.MoviesResponse]:
    return convert_dataclass_to_pydantic
