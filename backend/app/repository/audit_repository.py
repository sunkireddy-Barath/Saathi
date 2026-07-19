"""
Audit Log Repository.
"""

from typing import List, Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.repository.base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(AuditLog, db_session)

    async def get_logs_for_resource(
        self, resource: str, resource_id: UUID | str, skip: int = 0, limit: int = 50
    ) -> Tuple[List[AuditLog], int]:
        base_stmt = select(AuditLog).where(
            AuditLog.resource == resource,
            AuditLog.resource_id == resource_id
        )
        
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = await self.db_session.scalar(count_stmt) or 0
        
        stmt = base_stmt.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        
        return list(result.scalars().all()), total
