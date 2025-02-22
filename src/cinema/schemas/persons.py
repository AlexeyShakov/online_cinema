from typing import List
from pydantic import BaseModel

from src.schemas import Meta


class MovieData(BaseModel):
    id: str
    type: str

class MoviesRelationship(BaseModel):
    data: List[MovieData]

class ActorAttributes(BaseModel):
    name_ru: str
    name_en: str

class ActorRelationships(BaseModel):
    movies: MoviesRelationship

class ActorItem(BaseModel):
    type: str
    id: str
    attributes: ActorAttributes
    relationships: ActorRelationships


class PersonDataResponse(BaseModel):
    meta: Meta
    data: List[ActorItem]
