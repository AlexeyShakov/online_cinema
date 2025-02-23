from fastapi import Depends

from src.cinema import FilmRepository, get_film_repository
from src.cinema import PersonRepository, get_person_repository
from src.cinema import data_types


class FilmService:
    def __init__(self, repository: FilmRepository) -> None:
        self._repository = repository

    async def search_films(
            self,
            search_value: str,
            limit: int,
            offset: int
    ) -> data_types.MoviesElasticResponse:
        return await self._repository.search_films(search_value, limit, offset)


class PersonsService:
    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    async def search_persons(
            self,
            search_value: str,
            limit: int,
            offset: int
    ) -> data_types.ActorsElasticResponse:
        return await self._repository.search_persons(search_value, limit, offset)


def get_persons_service(
    repository: PersonRepository = Depends(get_person_repository)
) -> PersonsService:
    return PersonsService(repository=repository)


def get_films_service(
    repository: FilmRepository = Depends(get_film_repository)
) -> FilmService:
    return FilmService(repository=repository)

