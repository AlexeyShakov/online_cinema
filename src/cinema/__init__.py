from .models import Film, Person, Genre, MovieGenreRelation, PersonFilmRelation
from .repositories import PersonRepository, FilmRepository, get_film_repository, get_person_repository
from .routers import movie_routes, person_routes
from .config import PERSON_INDEX_NAME, FILM_INDEX_NAME
