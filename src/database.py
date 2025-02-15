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


# class DateTimeWithTZ(types.TypeDecorator):
#     impl = types.Text
#
#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return value
#         return value.isoformat()
#
#     def process_result_value(self, value, dialect):
#         """
#         Подгоняем под ISO 8601
#         """
#         if value is None:
#             return None
#         try:
#             value = value.replace(" ", "T").replace("+00", "+00:00")
#
#             if "." in value:  # Check if fractional seconds exist
#                 main_part, tz_part = value.split("+")
#                 time_part, fraction = main_part.split(".")
#                 fraction = fraction.ljust(6, "0")[:6]
#                 value = f"{time_part}.{fraction}+{tz_part}"
#             return datetime.fromisoformat(value)
#         except ValueError as e:
#             raise ValueError(f"Invalid datetime format: {e}")

class DateTimeWithTZ(types.TypeDecorator):
    """Custom DateTime type for proper ISO 8601 format and timezone handling."""
    impl = types.Text

    def process_bind_param(self, value, dialect) -> str:
        """Convert datetime object to ISO format string before inserting into DB."""
        if value is None:
            return None
        if isinstance(value, str):  # ✅ If already a string, return as is
            return value
        if isinstance(value, datetime):  # ✅ Ensure it's a datetime object
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)  # Ensure UTC timezone
            return value.strftime("%Y-%m-%d %H:%M:%S.%f+00")  # Convert to DB format
        raise TypeError("Invalid type for DateTimeWithTZ. Expected datetime or string.")

    def process_result_value(self, value, dialect) -> datetime:
        """Convert stored string back to datetime object with timezone."""
        if value is None:
            return None
        if isinstance(value, datetime):  # ✅ If already a datetime, return it
            return value
        if isinstance(value, str):  # ✅ Convert string back to datetime
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f+00").replace(tzinfo=timezone.utc)
        raise TypeError("Invalid type for DateTimeWithTZ. Expected string or datetime.")