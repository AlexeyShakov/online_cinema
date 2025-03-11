from pydantic import BaseModel


class BaseData(BaseModel):
    id: str
    type: str
