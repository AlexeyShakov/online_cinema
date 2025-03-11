from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow")

    view_sql_queries: bool = False