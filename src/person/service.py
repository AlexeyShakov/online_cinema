from fastapi import Depends

from src.person.repository import PersonRepository, get_person_repository


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
