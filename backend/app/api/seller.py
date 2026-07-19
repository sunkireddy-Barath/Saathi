"""
Seller API Router.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, require_seller
from app.models.user import User
from app.schemas.seller import SellerDashboardResponse, SellerProfileResponse, SellerProfileUpdate
from app.services.seller_service import SellerService

router = APIRouter(prefix="/api/v1/seller", tags=["Seller"])


@router.get("/dashboard", response_model=SellerDashboardResponse)
async def get_dashboard(
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db)
):
    """Get aggregated dashboard stats for the authenticated seller."""
    service = SellerService(db)
    return await service.get_dashboard_stats(current_user)


@router.put("/profile", response_model=SellerProfileResponse)
async def update_profile(
    req: SellerProfileUpdate,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db)
):
    """Update seller profile details."""
    service = SellerService(db)
    return await service.update_profile(current_user.id, req)
