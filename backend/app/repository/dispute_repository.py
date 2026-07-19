"""
Dispute Repository.
"""

from typing import List, Tuple
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dispute import Dispute
from app.repository.base_repository import BaseRepository


class DisputeRepository(BaseRepository[Dispute]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Dispute, db_session)

    async def get_user_disputes(
        self, user_id: UUID | str, skip: int = 0, limit: int = 20
    ) -> Tuple[List[Dispute], int]:
        base_stmt = select(Dispute).where(
            or_(
                Dispute.raised_by_id == user_id,
                Dispute.defendant_id == user_id
            )
        )
        
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = await self.db_session.scalar(count_stmt) or 0
        
        stmt = base_stmt.order_by(Dispute.created_at.desc()).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        
        return list(result.scalars().all()), total
