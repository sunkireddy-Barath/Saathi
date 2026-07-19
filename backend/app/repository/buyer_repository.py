"""
Buyer Repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.buyer import BuyerProfile
from app.repository.base_repository import BaseRepository


class BuyerRepository(BaseRepository[BuyerProfile]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(BuyerProfile, db_session)

    async def get_by_user_id(self, user_id: UUID | str) -> Optional[BuyerProfile]:
        stmt = select(BuyerProfile).where(BuyerProfile.user_id == user_id).options(selectinload(BuyerProfile.user))
        result = await self.db_session.execute(stmt)
        return result.scalars().first()
