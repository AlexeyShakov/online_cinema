from .models import Base
from .database import DateTimeWithTZ, get_db_session
from . import global_vars

# Два импорта снизу нужны, чтобы мы могли избавиться от цикличного импорта в
# person.models и filmds.models. Модели Person и Film ссылаются друг на друга из-за связи M2M
# подробнее читать здесь: https://stackoverflow.com/questions/79258512/sqlalchmey-circular-import-whit-many-to-many-relationship
from src.films import Film
from src.person import Person

from .logging import LOGGER
