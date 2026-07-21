"""
Async SQLAlchemy 2.0 database engine and session factory.

Usage inside a FastAPI dependency:
    async with get_db() as session:
        result = await session.execute(...)
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uuid
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# ── Engine ─────────────────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,       # Logs all SQL when DEBUG=true
    poolclass=NullPool,        # Disable local pooling, use PgBouncer pooling
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid.uuid4()}__",
    }
)

# ── Session factory ────────────────────────────────────────────────────────────
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,    # Objects remain usable after commit
    autocommit=False,
    autoflush=False,
)


# ── Base model ─────────────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """
    Shared declarative base.  All ORM models inherit from this class.
    """
    pass


# ── Dependency helper ──────────────────────────────────────────────────────────
@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager that yields a database session and guarantees
    cleanup on exit (commit on success, rollback on exception).
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_all_tables() -> None:
    """
    Create all tables that are registered on Base.metadata.

    Called during application startup in development / testing.
    In production, always use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:
    """Drop every table. Only used in test teardown — never in production."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
