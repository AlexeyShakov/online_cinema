from src.cinema import schemas, data_types

from typing import Union, TypeVar, Type

S = TypeVar("S", bound=Union[data_types.MoviesElasticResponse, data_types.ActorsElasticResponse])
ER = TypeVar("ER", bound=Union[schemas.MoviesResponse, schemas.PersonDataResponse])


def prepare_data_after_elastic(response_scheme: Type[S], data: ER,
                                     pagination_data: data_types.PaginationDict) -> S:
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