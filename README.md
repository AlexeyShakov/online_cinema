# Онлайн кинотеатр

В данном приложении реализуется API поиска по фильмам и персоналу фильмов(актеры, режиссеры и тд).

Поиск по фильмам производится по наименованию фильмов и их описанию.
Поиск по персоналу фильмов производится по имени человека.

Документацию по API можно найти по адресу 127.0.0.1:8000/docs после запуска проекта

Также реализован процесс ETL из мастер БД(в данном случае SQLite) в ElasticSearch

## Структура приложения
src

    - cinema (находятся все сущности, связанные с поиском фильмов или персонала)

    - elastic_search_app (находятся сущности, связанные с переносом данных из мастер БД в elastic)
        - 
    - general_usage(здесь хранятся файлы, которые могут использоваться в любом месте проекта)

## Используемые технологии

* FastAPI;
* SQLAlchemy;
* ElasticSearch;
* poetry;
* mypy;
* pre-commit;
* ruff;

## Конфигурация приложения
Для успешного запуска приложения нужно заполнить .env, который должен лежать на уровне src

TRANSFER_DATA_TO_ELASTIC=true|false - если нужен перенос из мастер БД, то true
ELASTIC_URL=http://localhost:9200 - базовый адрес ElasticSearch
CREATE_ELASTIC_INDEX=true|false - для создания индексов
VIEW_SQL_QUERIES=true|false - для SQL-логов

MODELS_TO_TRANSFER_DATA_FROM=films,persons - перечисление моделей, из которых нужно перенести данные в Elastic. 
                                            Используется в cli-командах(src.elasticsearch_app)
PERSONS_RELATED_FIELDS=films - нужна для переноса данных из мастер БД в Elastic. 
                                Здесь должны лежать связанные поля(Foreign key или M2M), которые используется при переносе
                                данных
FILMS_RELATED_FIELDS=persons,genres - тоже самое, что и PERSONS_RELATED_FIELDS
TRANSFER_BATCH_SIZE=500 - количество строк из мастер БД, которое можно перенести за раз

PERSON_INDEX_NAME=persons - название индекса для ElasticSearch с информацией по персонам
FILM_INDEX_NAME=films - название индекса для ElasticSearch с информацией по фильмам
SHARD_NUMBER=1 - количество шардов ElasticSearch
REPLICA_NUMBER=1 - количество реплик ElasticSearch


## Старт приложения
Для первого запуска приложения: ```docker-compose up --build```. Для последующих запусков приложения: ```docker-compose up```
После того, как проект запустился нужно сделать миграцию данных из мастер БД в ElasticSearch:
* ```poetry run python -m src.elasticsearch_app.cli create-elastic-indices```(для создания индексов)
* ```poetry run python -m src.elasticsearch_app.cli  migrate-data-to-elastic```(миграция из SQLite)
* ```poetry run python -m src.elasticsearch_app.cli migrate_kinopoisk_data```(миграция данных на русском языке из датасета кинопоиска)

## Возможные улучшения(для разработчиков)
* добавить абстракции для классов репозиториев и сервисов;

