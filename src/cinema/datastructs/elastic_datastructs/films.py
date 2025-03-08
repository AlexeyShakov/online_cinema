from src.cinema.datastructs.elastic_datastructs import general
from typing import TypedDict, List, Literal


class MoviesRelationshipsDict(TypedDict):
    actors: dict[str, List[general.DataDict]]


class MoviesAttributesDict(TypedDict):
    title_ru: str
    title_en: str
    description: str
    category_ids: List[str]


class MoviesSourceDict(TypedDict):
    type: Literal['movies']
    id: str
    attributes: MoviesAttributesDict
    relationships: MoviesRelationshipsDict


class MoviesElasticPayload(TypedDict):
    _source: MoviesSourceDict


class MoviesElasticMetaData(TypedDict):
    total: general.TotalDict
    hits: List[MoviesElasticPayload]

class MoviesElasticResponse(TypedDict):
    hits: MoviesElasticMetaData