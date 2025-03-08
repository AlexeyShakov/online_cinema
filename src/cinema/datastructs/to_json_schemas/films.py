from pydantic import BaseModel
from typing import List, Optional

from src.general_usage.jsonapi_schemas import ListResponse
from src.cinema.datastructs.to_json_schemas import general


class ActorsRelationship(BaseModel):
    data: List[general.BaseData]


class Relationships(BaseModel):
    actors: ActorsRelationship


class Attributes(BaseModel):
    title_ru: str
    title_en: str
    description: Optional[str]
    category_ids: List[str]


class Movie(BaseModel):
    id: str
    type: str
    attributes: Attributes
    relationships: Relationships


class MoviesResponse(ListResponse[Movie]):
    ...
