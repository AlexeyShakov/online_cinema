from typing import TypedDict


class DataDict(TypedDict):
    id: str
    type: str


class TotalDict(TypedDict):
    value: int
    relation: str


class PaginationDict(TypedDict):
    offset: int
    limit: int