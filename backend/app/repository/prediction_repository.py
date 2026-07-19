"""
Prediction Repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction import Prediction
from app.repository.base_repository import BaseRepository


class PredictionRepository(BaseRepository[Prediction]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Prediction, db_session)

    async def get_latest_for_product(self, product_id: UUID | str) -> Optional[Prediction]:
        stmt = select(Prediction).where(
            Prediction.product_id == product_id
        ).order_by(Prediction.created_at.desc())
        
        result = await self.db_session.execute(stmt)
        return result.scalars().first()
