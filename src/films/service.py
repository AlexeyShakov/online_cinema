from fastapi import Depends

from .repository import FilmRepository, get_film_repository


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


def get_films_service(
    repository: FilmRepository = Depends(get_film_repository)
) -> FilmService:
    return FilmService(repository=repository)
