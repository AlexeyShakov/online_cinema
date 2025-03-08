from fastapi import Depends

from src.cinema import FilmRepository, get_film_repository, PersonRepository, get_person_repository
from src.cinema.datastructs.elastic_datastructs import persons
from src.cinema.serializers import from_elastic_to_python as from_elastic_to_python_serializers
from src.cinema.datastructs import from_elastic_to_python


class FilmService:
    def __init__(self, repository: FilmRepository) -> None:
        self._repository = repository

    async def search_films(
            self,
            search_value: str,
            limit: int,
            offset: int
    ) -> from_elastic_to_python.Movies:
        from_elastic_to_python_serializer = from_elastic_to_python_serializers.get_serializer_films_from_elastic_to_python()
        return await self._repository.search_films(search_value, limit, offset, from_elastic_to_python_serializer)


class PersonsService:
    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    async def search_persons(
            self,
            search_value: str,
            limit: int,
            offset: int
    ) -> persons.ActorsElasticResponse:
        return await self._repository.search_persons(search_value, limit, offset)


def get_persons_service(
    repository: PersonRepository = Depends(get_person_repository)
) -> PersonsService:
    return PersonsService(repository=repository)


def get_films_service(
    repository: FilmRepository = Depends(get_film_repository)
) -> FilmService:
    return FilmService(repository=repository)

