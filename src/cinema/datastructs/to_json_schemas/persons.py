from typing import List
from pydantic import BaseModel

from src.general_usage.jsonapi_schemas import ListResponse
from src.cinema.datastructs.to_json_schemas import general


class MoviesRelationship(BaseModel):
    data: List[general.BaseData]


class PersonAttributes(BaseModel):
    name_ru: str
    name_en: str


class PersonRelationships(BaseModel):
    movies: MoviesRelationship


class PersonItem(BaseModel):
    type: str
    id: str
    attributes: PersonAttributes
    relationships: PersonRelationships


class PersonDataResponse(ListResponse):
    ...
