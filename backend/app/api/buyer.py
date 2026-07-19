"""
Buyer API Router.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, require_buyer
from app.models.user import User
from app.schemas.buyer import BuyerProfileResponse, BuyerProfileUpdate
from app.services.buyer_service import BuyerService

router = APIRouter(prefix="/api/v1/buyer", tags=["Buyer"])


@router.get("/profile", response_model=BuyerProfileResponse)
async def get_profile(
    current_user: User = Depends(require_buyer),
    db: AsyncSession = Depends(get_db)
):
    """Get profile details for the authenticated buyer."""
    service = BuyerService(db)
    return await service.get_profile(current_user.id)


@router.put("/profile", response_model=BuyerProfileResponse)
async def update_profile(
    req: BuyerProfileUpdate,
    current_user: User = Depends(require_buyer),
    db: AsyncSession = Depends(get_db)
):
    """Update buyer profile details."""
    service = BuyerService(db)
    return await service.update_profile(current_user.id, req)
