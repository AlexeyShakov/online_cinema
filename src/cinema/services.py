from fastapi import Depends

from src.cinema import FilmRepository, get_film_repository
from src.cinema import PersonRepository, get_person_repository


class FilmService:
    # TODO может сделать Generic класс для Person и Film?
    def __init__(self, repository: FilmRepository) -> None:
        self._repository = repository

    async def search_films(
            self,
            search_value: str,
            limit: int,
            offset: int
    ):
        return await self._repository.search_films(search_value, limit, offset)


class PersonsService:
    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    async def search_persons(
            self,
            search_value: str,
            limit: int,
            offset: int
    ):
        return await self._repository.search_persons(search_value, limit, offset)


def get_persons_service(
    repository: PersonRepository = Depends(get_person_repository)
) -> PersonsService:
    return PersonsService(repository=repository)


def get_films_service(
    repository: FilmRepository = Depends(get_film_repository)
) -> FilmService:
    return FilmService(repository=repository)

