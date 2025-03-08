from src.cinema import to_json_schemas
from src.cinema.datastructs.elastic_datastructs import general, persons, films

from typing import Union, TypeVar, Type


S = TypeVar("S", bound=Union[films.MoviesElasticResponse, persons.ActorsElasticResponse])
ER = TypeVar("ER", bound=Union[to_json_schemas.MoviesResponse, to_json_schemas.PersonDataResponse])


def prepare_data_after_elastic(response_scheme: Type[S], data: ER,
                                     pagination_data: general.PaginationDict) -> S:
    """
    Избавляемся от лишней вложенности(_source) и добавляем информацию о метаданных
    """
    payload = data["hits"].get("hits")
    pagination_data["total"] = data["hits"]["total"]["value"]
    result = {"meta": {"pagination": pagination_data}}
    if payload:
        result["data"] = [el["_source"] for el in payload]
    else:
        result["data"] = []
    return response_scheme(**result)


def get_elastic_serializer():
    return prepare_data_after_elastic