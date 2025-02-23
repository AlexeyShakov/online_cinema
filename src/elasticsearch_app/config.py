import os
from dotenv import load_dotenv



load_dotenv()

from pydantic_settings import BaseSettings, SettingsConfigDict

class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    elastic_url: str = "http://localhost:9200"
    person_index_name: str
    film_index_name: str
    shard_number: int = 1
    replica_number: int = 1


SHARD_NUMBER = 1
REPLICA_NUMBER = 1
ELASTIC_URL = os.getenv("ELASTIC_URL")
PERSON_INDEX_NAME = "persons"
FILM_INDEX_NAME = "films"
