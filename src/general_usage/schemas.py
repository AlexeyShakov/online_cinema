from pydantic import BaseModel


class Pagination(BaseModel):
    offset: int
    limit: int
    total: int


class Meta(BaseModel):
    pagination: Pagination
