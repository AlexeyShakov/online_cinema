from typing import List, Annotated, Optional
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow")

    elastic_url: str = "http://localhost:9200"
    person_index_name: str
    film_index_name: str
    shard_number: int = 1
    replica_number: int = 1
    transfer_batch_size: int = 500
    movie_title_weight: int = 10
    movie_description_weight: int = 1
    persons_related_fields: Annotated[List[str], NoDecode] = Field(default_factory=list)
    films_related_fields: Annotated[List[str], NoDecode] = Field(default_factory=list)
    models_to_transfer_data_from: Annotated[List[str], NoDecode] = Field(default_factory=list)

    @field_validator('persons_related_fields', mode='before')
    @classmethod
    def decode_persons_related_fields(cls, v: str) -> List[str]:
        return [x.strip() for x in v.split(',')]

    @field_validator('films_related_fields', mode='before')
    @classmethod
    def decode_films_related_fields(cls, v: str) -> List[str]:
        return [x.strip() for x in v.split(',')]

    @field_validator('models_to_transfer_data_from', mode='before')
    @classmethod
    def decode_models_to_transfer_data_from(cls, v: str) -> List[str]:
        return [x.strip() for x in v.split(',')]
