from typing import TypeVar, Generic

from pydantic import BaseModel

DataT = TypeVar("DataT")


class Pagination(BaseModel):
    offset: int
    limit: int


class PaginationWithTotal(BaseModel):
    offset: int
    limit: int
    total: int


class Meta(BaseModel):
    pagination: PaginationWithTotal


class ListResponse(BaseModel, Generic[DataT]):
    data: list[DataT]
    meta: Meta
