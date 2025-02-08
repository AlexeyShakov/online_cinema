from fastapi import FastAPI

from src import global_vars, cinema
from src.elasticsearch_app import close_es_connection, get_es_connection


app = FastAPI()

app.include_router(cinema.MOVIE_ROUTES)
app.include_router(cinema.PERSON_ROUTES)


@app.on_event("shutdown")
async def shutdown_event():
    await close_es_connection()
