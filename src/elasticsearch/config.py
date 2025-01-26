import os
from dotenv import load_dotenv

load_dotenv()


SHARD_NUMBER = 1
REPLICA_NUMBER = 1
ELASTIC_URL = os.getenv("ELASTIC_URL")

PERSON_INDEX_NAME = "persons"
FILM_INDEX_NAME = "films"
