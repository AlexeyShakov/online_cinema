from typing import Callable

from src.cinema.datastructs.elastic_datastructs import films
from src.cinema.datastructs import from_elastic_to_python


def convert_movies_to_dataclass(data: films.MoviesElasticResponse) -> from_elastic_to_python.Movies:
    meta = from_elastic_to_python.Meta(total=data["hits"]["total"]["value"])
    movies_list = []

    for item in data["hits"]["hits"]:
        source = item["_source"]

        actors = []
        for actor_data in source["relationships"]["actors"]["data"]:
            actors.append(from_elastic_to_python.BaseData(id=actor_data["id"], type=actor_data["type"]))

        attributes = from_elastic_to_python.Attributes(
            title_ru=source["attributes"]["title_ru"],
            title_en=source["attributes"]["title_en"],
            description=source["attributes"]["description"],
            category_ids=source["attributes"]["category_ids"],
            actors=actors
        )

        movie = from_elastic_to_python.Movie(
            id=source["id"],
            type=source["type"],
            attributes=attributes
        )
        movies_list.append(movie)

    return from_elastic_to_python.Movies(meta=meta, data=movies_list)


def get_serializer_films_from_elastic_to_python() -> Callable[[films.MoviesElasticResponse], from_elastic_to_python.Movies]:
    return convert_movies_to_dataclass