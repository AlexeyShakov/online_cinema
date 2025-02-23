from fastapi import FastAPI

from src import cinema
from src.elasticsearch_app import close_es_connection
# from src.config import get_general_application_settings


app = FastAPI()

app.include_router(cinema.movie_routes)
app.include_router(cinema.person_routes)

# general_application_settings = get_general_application_settings()()


@app.on_event("shutdown")
async def shutdown_event():
    await close_es_connection()
