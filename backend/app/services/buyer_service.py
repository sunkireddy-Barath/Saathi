"""
Buyer Service.
Handles buyer profile management.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.buyer import BuyerProfile
from app.repository.buyer_repository import BuyerRepository
from app.schemas.buyer import BuyerProfileUpdate
from app.utils.exceptions import NotFoundException


class BuyerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.buyer_repo = BuyerRepository(db)

    async def get_profile(self, user_id: UUID) -> BuyerProfile:
        profile = await self.buyer_repo.get_by_user_id(user_id)
        if not profile:
            raise NotFoundException(detail="Buyer profile not found.")
        return profile

    async def update_profile(self, user_id: UUID, req: BuyerProfileUpdate) -> BuyerProfile:
        profile = await self.get_profile(user_id)
        update_data = req.model_dump(exclude_unset=True)
        return await self.buyer_repo.update(profile, update_data)
