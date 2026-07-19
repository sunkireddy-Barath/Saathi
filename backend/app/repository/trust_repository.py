"""
Trust Repository.
"""

from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trust import TrustEvent
from app.repository.base_repository import BaseRepository


class TrustRepository(BaseRepository[TrustEvent]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(TrustEvent, db_session)

    async def get_user_events(self, user_id: UUID | str, limit: int = 50) -> List[TrustEvent]:
        stmt = select(TrustEvent).where(
            TrustEvent.user_id == user_id
        ).order_by(TrustEvent.created_at.desc()).limit(limit)
        
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())
