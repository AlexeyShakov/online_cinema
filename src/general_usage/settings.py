from src.general_usage.config import GeneralApplicationSettings
from src.elasticsearch_app.config import ElasticSettings

general_application_settings = GeneralApplicationSettings()
elastic_settings = ElasticSettings()


def get_general_application_settings():
    return general_application_settings


def get_elastic_settings():
    return elastic_settings
