from typing import Generator

from sqlalchemy import create_engine, types
from sqlalchemy.orm import sessionmaker, Session

from datetime import datetime
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DateTimeWithTZ(types.TypeDecorator):
    impl = types.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return value.isoformat()

    def process_result_value(self, value, dialect):
        """
        Подгоняем под ISO 8601
        """
        if value is None:
            return None
        try:
            value = value.replace(" ", "T").replace("+00", "+00:00")

            if "." in value:  # Check if fractional seconds exist
                main_part, tz_part = value.split("+")
                time_part, fraction = main_part.split(".")
                fraction = fraction.ljust(6, "0")[:6]
                value = f"{time_part}.{fraction}+{tz_part}"
            return datetime.fromisoformat(value)
        except ValueError as e:
            raise ValueError(f"Invalid datetime format: {e}")
