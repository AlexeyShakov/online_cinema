from src.cinema.datastructs.elastic_datastructs import general

from typing import List, TypedDict, Literal


class ActorsRelationshipsDict(TypedDict):
    movies: dict[str, List[general.DataDict]]


class ActorsAttributesDict(TypedDict):
    name_ru: str
    name_en: str


class ActorsSourceDict(TypedDict):
    type: Literal['actors']
    id: str
    attributes: ActorsAttributesDict
    relationships: ActorsRelationshipsDict


class ActorsElasticPayload(TypedDict):
    _source: ActorsSourceDict


class ActorsElasticMetaData(TypedDict):
    total: general.TotalDict
    hits: List[ActorsElasticPayload]

class ActorsElasticResponse(TypedDict):
    hits: ActorsElasticMetaData