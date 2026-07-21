"""
Seller API Router.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, require_seller
from app.models.user import User
from app.schemas.seller import SellerDashboardResponse, SellerProfileResponse, SellerProfileUpdate
from app.schemas.product import ProductListResponse
from app.services.seller_service import SellerService
from app.utils.helpers import paginate

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


@router.get("/inventory", response_model=ProductListResponse)
async def get_inventory(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db)
):
    """Get all products listed by the seller."""
    service = SellerService(db)
    skip = (page - 1) * page_size
    products, total = await service.get_inventory(current_user.id, skip=skip, limit=page_size)
    meta = paginate(total, page, page_size)
    return ProductListResponse(items=products, **meta)
