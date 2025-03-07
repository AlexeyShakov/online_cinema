from typing import Optional
import backoff
from dataclasses import asdict

from elasticsearch import AsyncElasticsearch

from src.elasticsearch_app.data_types import ESConnectionSettings
from src.general_usage.logging_config import LOGGER
from src.settings import get_elastic_settings

ELASTIC_SETTINGS = get_elastic_settings()


class ElasticConnectionHandler:
    __instance = None

    def __new__(cls, *args, **kwargs) -> None:
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, connection_params: ESConnectionSettings) -> None:
        self.__connection_params = connection_params
        self.__connection: Optional[AsyncElasticsearch] = None

    async def get_connection(self) -> AsyncElasticsearch:
        if not self.__connection:
            await self._initialize_connection(self.__connection_params)
        else:
            await self._check_existing_connection(self.__connection)
        return self.__connection

    @backoff.on_predicate(backoff.constant, lambda x: x is False, interval=0.5, max_tries=3)
    @backoff.on_exception(backoff.constant, Exception, interval=0.5, max_tries=3)
    async def _initialize_connection(self, connection_params: ESConnectionSettings) -> bool:
        connection = AsyncElasticsearch(**asdict(connection_params))
        if not await self._check_cluster_health(connection):
            await connection.close()
            return False
        else:
            self.__connection = connection
            return True

    async def _check_cluster_health(self, connection: AsyncElasticsearch) -> bool:
        try:
            health = await connection.cluster.health()
            status = health.get("status", "unknown")

            if status in {"green", "yellow"}:
                LOGGER.info(f"Соединение с Elastic установлено. Статус: {status}")
                return True
            else:
                LOGGER.warning(f"Соединение с Elastic не установлено: {status}")
                return False
        except Exception as e:
            LOGGER.exception(f"Elastic не доступен: {e}")
            return False

    async def _check_existing_connection(self, connection: AsyncElasticsearch) -> None:
        try:
            is_alive = await self._is_connection_alive(connection)
        except Exception:
            is_alive = False
        if not is_alive:
            await self._initialize_connection(self.__connection_params)

    @backoff.on_predicate(backoff.constant, lambda x: x is False, interval=0.5, max_tries=3)
    @backoff.on_exception(backoff.constant, Exception, interval=0.5, max_tries=3)
    async def _is_connection_alive(self, connection: AsyncElasticsearch) -> bool:
        try:
            return await connection.ping()
        except Exception as e:
            LOGGER.exception(f"Соединение с Elastic потеряно: {e}")
            return False

    async def close_es_connection(self) -> None:
        try:
            if await self._is_connection_alive(self.__connection):
                await self.__connection.close()
                LOGGER.info("Соединение с Elastic успешно закрыто")
            else:
                LOGGER.info("Соединение с Elastic уже было закрыто")
        except Exception as e:
            LOGGER.exception(f"Ошибка при проверки Elastic соединения: {e}")


__ES_CONNECTION_HANDLER = ElasticConnectionHandler(ESConnectionSettings(hosts=[ELASTIC_SETTINGS.elastic_url]))


async def get_es_connection() -> AsyncElasticsearch:
    return await __ES_CONNECTION_HANDLER.get_connection()


async def close_es_connection() -> None:
    await __ES_CONNECTION_HANDLER.close_es_connection()
