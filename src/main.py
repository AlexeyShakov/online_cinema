from fastapi import FastAPI

from movies import MOVIE_ROUTES
from actors import ACTOR_ROUTES

app = FastAPI()

app.include_router(MOVIE_ROUTES)
app.include_router(ACTOR_ROUTES)