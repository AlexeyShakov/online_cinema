from fastapi import FastAPI

from films import MOVIE_ROUTES
from person import ACTOR_ROUTES

from src import Film, Person, global_vars
from src.utils import migrate_persons_to_elastic


migrate_persons_to_elastic(Person, "films", global_vars.BATCH_SIZE_FOR_TRANSFERRING)
migrate_persons_to_elastic(Film, "persons", global_vars.BATCH_SIZE_FOR_TRANSFERRING)

app = FastAPI()

app.include_router(MOVIE_ROUTES)
app.include_router(ACTOR_ROUTES)