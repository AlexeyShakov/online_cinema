from typing import AsyncGenerator
import re

from sqlalchemy import types
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


from datetime import datetime, timezone
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
    """Custom DateTime type for proper ISO 8601 format and timezone handling."""
    impl = types.Text

    def process_bind_param(self, value, dialect) -> str:
        """Convert datetime object to ISO format string before inserting into DB."""
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)  # Ensure UTC timezone
            return value.strftime("%Y-%m-%d %H:%M:%S.%f+00")  # Convert to DB format
        raise TypeError("Invalid type for DateTimeWithTZ. Expected datetime or string.")

    def process_result_value(self, value, dialect) -> datetime:
        """Convert stored string back to datetime object with timezone."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f+00").replace(tzinfo=timezone.utc)
        raise TypeError("Invalid type for DateTimeWithTZ. Expected string or datetime.")