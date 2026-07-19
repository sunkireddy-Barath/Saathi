"""
Base generic repository.

Provides standard CRUD operations for all ORM models so we don't
have to repeat the same session.execute() boilerplate everywhere.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get_by_id(self, id: UUID | str) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db_session.add(db_obj)
        await self.db_session.flush()
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db_session.add(db_obj)
        await self.db_session.flush()
        return db_obj

    async def delete(self, id: UUID | str) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db_session.execute(stmt)
        await self.db_session.flush()
        return result.rowcount > 0
