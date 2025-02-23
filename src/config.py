from typing import Type

from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralAppliSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    view_sql_queries: bool = False


def get_general_application_settings() -> Type[GeneralAppliSettings]:
    return GeneralAppliSettings
