"""
Seller Service.
Handles seller profile management and dashboard aggregation.
"""

from typing import Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.seller import SellerProfile
from app.models.user import User
from app.repository.seller_repository import SellerRepository
from app.repository.product_repository import ProductRepository
from app.repository.order_repository import OrderRepository
from app.repository.negotiation_repository import NegotiationRepository
from app.schemas.seller import SellerProfileUpdate, SellerDashboardResponse
from app.utils.exceptions import NotFoundException, ForbiddenException
from app.utils.constants import ProductStatus, OrderStatus


class SellerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.seller_repo = SellerRepository(db)
        self.product_repo = ProductRepository(db)
        self.order_repo = OrderRepository(db)
        self.negotiation_repo = NegotiationRepository(db)

    async def get_profile(self, user_id: UUID) -> SellerProfile:
        profile = await self.seller_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundException(detail="Seller profile not found.")
        return profile

    async def update_profile(self, user_id: UUID, req: SellerProfileUpdate) -> SellerProfile:
        profile = await self.get_profile(user_id)
        update_data = req.model_dump(exclude_unset=True)
        return await self.seller_repo.update(profile, update_data)

    async def get_dashboard_stats(self, user: User) -> SellerDashboardResponse:
        profile = await self.get_profile(user.id)
        
        products, _ = await self.product_repo.get_seller_products(profile.id, skip=0, limit=1000)
        active_products = sum(1 for p in products if p.status == ProductStatus.ACTIVE.value)
        
        orders, _ = await self.order_repo.get_user_orders(user.id, skip=0, limit=1000)
        pending_orders = sum(1 for o in orders if o.status in [OrderStatus.CONFIRMED.value, OrderStatus.PROCESSING.value])
        
        negotiations = await self.negotiation_repo.get_user_negotiations(user.id)
        recent_negotiations = len(negotiations) # Simplify to all active/recent
        
        return SellerDashboardResponse(
            profile=profile, # Handled by from_attributes
            trust_score=user.trust_score,
            active_products=active_products,
            pending_orders=pending_orders,
            total_revenue=profile.total_revenue,
            avg_rating=profile.avg_rating,
            recent_negotiations=recent_negotiations,
        )

    async def get_inventory(self, user_id: UUID, skip: int = 0, limit: int = 20) -> tuple[list[Any], int]:
        profile = await self.get_profile(user_id)
        products, total = await self.product_repo.get_seller_products(profile.id, skip=skip, limit=limit)
        return products, total
