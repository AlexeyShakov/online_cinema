from src.general_usage.config import GeneralApplicationSettings
from src.elasticsearch_app.config import ElasticSettings

general_application_settings = GeneralApplicationSettings()
elastic_settings = ElasticSettings()


def get_general_application_settings() -> GeneralApplicationSettings:
    return general_application_settings


def get_elastic_settings() -> ElasticSettings:
    return elastic_settings
