from fastapi import FastAPI

from src import cinema
from src.elasticsearch_app import close_es_connection


app = FastAPI()

app.include_router(cinema.movie_routes)
app.include_router(cinema.person_routes)


@app.on_event("shutdown")
async def shutdown_event():
    await close_es_connection()
