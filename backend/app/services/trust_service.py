"""
Trust Service.
Handles trust score calculation based on event sourcing.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trust import TrustEvent
from app.repository.trust_repository import TrustRepository
from app.repository.user_repository import UserRepository
from app.utils.constants import TrustEventType, TRUST_DELTA, TrustThreshold
from app.utils.exceptions import NotFoundException


class TrustService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.trust_repo = TrustRepository(db)
        self.user_repo = UserRepository(db)

    async def _add_event(
        self,
        user_id: UUID,
        event_type: TrustEventType,
        delta: int,
        reason: Optional[str] = None,
        reference_id: Optional[UUID] = None,
        performed_by_id: Optional[UUID] = None,
    ) -> TrustEvent:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail="User not found.")

        score_before = user.trust_score
        score_after = max(0, score_before + delta) # Floor at 0

        event_data = {
            "user_id": user.id,
            "event_type": event_type.value,
            "delta": delta,
            "score_before": score_before,
            "score_after": score_after,
            "reason": reason,
            "reference_id": reference_id,
            "performed_by_id": performed_by_id,
        }

        # Save event
        event = await self.trust_repo.create(event_data)

        # Update running total on user
        await self.user_repo.update(user, {"trust_score": score_after})
        
        # Suspend account if score drops too low
        if score_after < TrustThreshold.ACCOUNT_SUSPENDED:
            await self.user_repo.update(user, {"is_active": False})

        return event

    async def log_transaction_complete(self, user_id: UUID, order_id: UUID) -> TrustEvent:
        return await self._add_event(
            user_id, 
            TrustEventType.TRANSACTION_COMPLETE, 
            TRUST_DELTA[TrustEventType.TRANSACTION_COMPLETE],
            reference_id=order_id
        )

    async def log_positive_rating(self, user_id: UUID, order_id: UUID) -> TrustEvent:
        return await self._add_event(
            user_id, 
            TrustEventType.POSITIVE_RATING, 
            TRUST_DELTA[TrustEventType.POSITIVE_RATING],
            reference_id=order_id
        )

    async def log_fraud(self, user_id: UUID, reason: str, admin_id: UUID) -> TrustEvent:
        return await self._add_event(
            user_id, 
            TrustEventType.FRAUD_DETECTED, 
            TRUST_DELTA[TrustEventType.FRAUD_DETECTED],
            reason=reason,
            performed_by_id=admin_id
        )

    async def custom_admin_adjustment(
        self, user_id: UUID, delta: int, reason: str, admin_id: UUID
    ) -> TrustEvent:
        return await self._add_event(
            user_id, 
            TrustEventType.ADMIN_ADJUSTMENT, 
            delta,
            reason=reason,
            performed_by_id=admin_id
        )
