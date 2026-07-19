"""
Dispute Service.
Handles raising disputes and admin resolution.
"""

from typing import List, Tuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dispute import Dispute
from app.models.user import User
from app.repository.dispute_repository import DisputeRepository
from app.repository.order_repository import OrderRepository
from app.schemas.dispute import RaiseDisputeRequest, ResolveDisputeRequest
from app.utils.exceptions import NotFoundException, ForbiddenException, ConflictException
from app.utils.constants import DisputeStatus, OrderStatus


class DisputeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.dispute_repo = DisputeRepository(db)
        self.order_repo = OrderRepository(db)

    async def raise_dispute(self, user_id: UUID, req: RaiseDisputeRequest) -> Dispute:
        order = await self.order_repo.get_by_id(req.order_id)
        if not order:
            raise NotFoundException(detail="Order not found.")
            
        if order.buyer_id != user_id and order.seller_id != user_id:
            raise ForbiddenException(detail="You are not a party to this order.")
            
        existing = await self.dispute_repo.get_user_disputes(user_id, limit=100) # Simple check
        if any(d.order_id == order.id for d in existing[0]):
            raise ConflictException(detail="Dispute already exists for this order.")

        defendant_id = order.seller_id if user_id == order.buyer_id else order.buyer_id

        dispute_data = {
            "order_id": order.id,
            "raised_by_id": user_id,
            "defendant_id": defendant_id,
            "reason": req.reason,
            "description": req.description,
            "evidence_urls": req.evidence_urls,
            "status": DisputeStatus.OPEN.value
        }
        
        return await self.dispute_repo.create(dispute_data)

    async def get_dispute(self, dispute_id: UUID) -> Dispute:
        dispute = await self.dispute_repo.get_by_id(dispute_id)
        if not dispute:
            raise NotFoundException(detail="Dispute not found.")
        return dispute

    async def resolve_dispute(self, dispute_id: UUID, admin_user: User, req: ResolveDisputeRequest) -> Dispute:
        dispute = await self.get_dispute(dispute_id)
        if dispute.status == DisputeStatus.RESOLVED.value:
            raise ConflictException(detail="Dispute is already resolved.")
            
        update_data = {
            "status": DisputeStatus.RESOLVED.value,
            "winner": req.winner.value,
            "admin_notes": req.admin_notes,
            "resolved_by_id": admin_user.id
        }
        
        return await self.dispute_repo.update(dispute, update_data)
