from typing import TypedDict, List, Literal


class DataDict(TypedDict):
    id: str
    type: str


class MoviesRelationshipsDict(TypedDict):
    actors: dict[str, List[DataDict]]


class ActorsRelationshipsDict(TypedDict):
    movies: dict[str, List[DataDict]]


class MoviesAttributesDict(TypedDict):
    title_ru: str
    title_en: str
    description: str
    category_ids: List[str]


class ActorsAttributesDict(TypedDict):
    name_ru: str
    name_en: str


class ActorsSourceDict(TypedDict):
    type: Literal['actors']
    id: str
    attributes: ActorsAttributesDict
    relationships: ActorsRelationshipsDict


class MoviesSourceDict(TypedDict):
    type: Literal['movies']
    id: str
    attributes: MoviesAttributesDict
    relationships: MoviesRelationshipsDict


class ActorsElasticPayload(TypedDict):
    _source: ActorsSourceDict


class MoviesElasticPayload(TypedDict):
    _source: MoviesSourceDict


class TotalDict(TypedDict):
    value: int
    relation: str


class ActorsElasticMetaData(TypedDict):
    total: TotalDict
    hits: List[ActorsElasticPayload]


class MoviesElasticMetaData(TypedDict):
    total: TotalDict
    hits: List[MoviesElasticPayload]


class MoviesElasticResponse(TypedDict):
    hits: MoviesElasticMetaData


class ActorsElasticResponse(TypedDict):
    hits: ActorsElasticMetaData


class PaginationDict(TypedDict):
    offset: int
    limit: int

