from src.cinema.datastructs.elastic_datastructs import general
from src.cinema.datastructs import from_elastic_to_python
from src.cinema.datastructs.to_json_schemas import persons as person_to_json_schemas, films, \
    general as general_schemas_to_json
from src.general_usage import jsonapi_schemas

from typing import Type, Callable


def convert_movies_to_pydantic(response_scheme: Type[films.MoviesResponse], movies: from_elastic_to_python.Movies,
                               pagination_data: jsonapi_schemas.Pagination) -> films.MoviesResponse:
    pagination = jsonapi_schemas.PaginationWithTotal(total=movies.meta.total, limit=pagination_data.limit,
                                                     offset=pagination_data.offset)
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
                    data=[general_schemas_to_json.BaseData(id=actor.id, type=actor.type) for actor in
                          movie.attributes.actors]
                )
            )
        )
        for movie in movies.data
    ]
    return response_scheme(meta=meta, data=pydantic_movies)


def convert_persons_to_pydantic(response_scheme: Type[person_to_json_schemas.PersonDataResponse],
                                persons: from_elastic_to_python.Persons,
                                pagination_data: jsonapi_schemas.Pagination) -> person_to_json_schemas.PersonDataResponse:
    pagination = jsonapi_schemas.PaginationWithTotal(total=persons.meta.total, limit=pagination_data.limit,
                                                     offset=pagination_data.offset)
    meta = jsonapi_schemas.Meta(pagination=pagination)
    pydantic_persons = [
        person_to_json_schemas.PersonItem(
            type=person.type,
            id=person.id,
            attributes=person_to_json_schemas.PersonAttributes(
                name_ru=person.attributes.title_ru,
                name_en=person.attributes.title_en
            ),
            relationships=person_to_json_schemas.PersonRelationships(
                movies=person_to_json_schemas.MoviesRelationship(
                    data=[general_schemas_to_json.BaseData(id=movie.id, type=movie.type) for movie in
                          person.attributes.movies]
                )
            )
        )
        for person in persons.data
    ]
    return response_scheme(meta=meta, data=pydantic_persons)


def get_films_to_json_serializer() -> Callable[
    [Type[films.MoviesResponse], from_elastic_to_python.Movies, jsonapi_schemas.Pagination], films.MoviesResponse]:
    return convert_movies_to_pydantic


def get_persons_to_json_serializer() -> Callable[
    [Type[person_to_json_schemas.PersonDataResponse], from_elastic_to_python.Persons,
     jsonapi_schemas.Pagination], person_to_json_schemas.PersonDataResponse]:
    return convert_persons_to_pydantic
