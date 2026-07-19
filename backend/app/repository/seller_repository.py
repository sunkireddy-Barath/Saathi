"""
Seller Repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.seller import SellerProfile
from app.repository.base_repository import BaseRepository


class SellerRepository(BaseRepository[SellerProfile]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(SellerProfile, db_session)

    async def get_by_user_id(self, user_id: UUID | str) -> Optional[SellerProfile]:
        stmt = select(SellerProfile).where(SellerProfile.user_id == user_id).options(selectinload(SellerProfile.user))
        result = await self.db_session.execute(stmt)
        return result.scalars().first()
