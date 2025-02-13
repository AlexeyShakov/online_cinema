from pydantic import BaseModel
from typing import List, Optional

from src.schemas import Meta


class ActorData(BaseModel):
    id: str
    type: str

class ActorsRelationship(BaseModel):
    data: List[ActorData]

class Relationships(BaseModel):
    actors: ActorsRelationship

class Attributes(BaseModel):
    title: str
    description: Optional[str]
    category_ids: List[str]

class Movie(BaseModel):
    id: str
    type: str
    attributes: Attributes
    relationships: Relationships

class MoviesResponse(BaseModel):
    meta: Meta
    data: List[Movie]
