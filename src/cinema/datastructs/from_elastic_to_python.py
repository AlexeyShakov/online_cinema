from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class BaseData:
    id: str
    type: str


@dataclass(frozen=True)
class Attributes:
    title_ru: str
    title_en: str
    description: str
    category_ids: List[str]
    actors: List[BaseData]


@dataclass(frozen=True)
class Movie:
    id: str
    type: str
    attributes: Attributes


@dataclass(frozen=True)
class Meta:
    total: int


@dataclass(frozen=True)
class Movies:
    meta: Meta
    data: List[Movie]
