from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.general_usage.settings import get_general_application_settings

import os

from src import global_vars

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"
settings = get_general_application_settings()

# async_engine = create_async_engine(DATABASE_URL, echo=global_vars.VIEW_SQL_QUERIES)
async_engine = create_async_engine(DATABASE_URL, echo=settings.view_sql_queries)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
