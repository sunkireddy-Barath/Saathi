"""
Negotiation Repository.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.negotiation import Message, Negotiation
from app.repository.base_repository import BaseRepository
from app.utils.constants import NegotiationStatus


class NegotiationRepository(BaseRepository[Negotiation]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Negotiation, db_session)

    async def get_with_messages(self, negotiation_id: UUID | str) -> Optional[Negotiation]:
        stmt = select(Negotiation).where(Negotiation.id == negotiation_id).options(
            selectinload(Negotiation.messages)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_active_for_product(self, product_id: UUID | str) -> Optional[Negotiation]:
        stmt = select(Negotiation).where(
            and_(
                Negotiation.product_id == product_id,
                Negotiation.status.in_([
                    NegotiationStatus.PENDING.value,
                    NegotiationStatus.OFFER_MADE.value,
                    NegotiationStatus.COUNTERED.value
                ])
            )
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_user_negotiations(self, user_id: UUID | str) -> List[Negotiation]:
        stmt = select(Negotiation).where(
            or_(
                Negotiation.buyer_id == user_id,
                Negotiation.seller_id == user_id
            )
        ).order_by(Negotiation.created_at.desc())
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Message, db_session)

    async def get_messages_by_negotiation(self, negotiation_id: UUID | str) -> List[Message]:
        stmt = select(Message).where(Message.negotiation_id == negotiation_id).order_by(Message.created_at.asc())
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())
