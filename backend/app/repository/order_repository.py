"""
Order Repository.
"""

from typing import List, Tuple
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.repository.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Order, db_session)

    async def get_user_orders(
        self, user_id: UUID | str, skip: int = 0, limit: int = 20
    ) -> Tuple[List[Order], int]:
        base_stmt = select(Order).where(
            or_(
                Order.buyer_id == user_id,
                Order.seller_id == user_id
            )
        )
        
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = await self.db_session.scalar(count_stmt) or 0
        
        stmt = base_stmt.options(selectinload(Order.product)).order_by(Order.created_at.desc()).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        
        return list(result.scalars().all()), total
