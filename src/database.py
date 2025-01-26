from typing import AsyncGenerator

from sqlalchemy import types
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from datetime import datetime
import os

from src import global_vars


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"

async_engine = create_async_engine(DATABASE_URL, echo=global_vars.VIEW_SQL_QUERIES)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


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
