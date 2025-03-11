from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class BaseData:
    id: str
    type: str


@dataclass(frozen=True)
class MovieAttributes:
    title_ru: str
    title_en: str
    description: str
    category_ids: List[str]
    actors: List[BaseData]


@dataclass(frozen=True)
class PersonAttributes:
    title_ru: str
    title_en: str
    movies: List[BaseData]


@dataclass(frozen=True)
class Movie:
    id: str
    type: str
    attributes: MovieAttributes


@dataclass(frozen=True)
class Person:
    id: str
    type: str
    attributes: PersonAttributes


@dataclass(frozen=True)
class Meta:
    total: int


@dataclass(frozen=True)
class Persons:
    meta: Meta
    data: List[Person]


@dataclass(frozen=True)
class Movies:
    meta: Meta
    data: List[Movie]
