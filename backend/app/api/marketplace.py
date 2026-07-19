"""
Marketplace API Router.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, require_seller
from app.models.user import User
from app.schemas.product import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate
from app.services.marketplace_service import MarketplaceService
from app.utils.constants import FabricType
from app.utils.helpers import paginate

router = APIRouter(prefix="/api/v1/marketplace", tags=["Marketplace"])


@router.get("/products", response_model=ProductListResponse)
async def search_products(
    search: Optional[str] = None,
    fabric_type: Optional[FabricType] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search and filter active products on the marketplace."""
    service = MarketplaceService(db)
    skip = (page - 1) * page_size
    
    fabric_val = fabric_type.value if fabric_type else None
    
    products, total = await service.search_marketplace(
        search, fabric_val, min_price, max_price, skip, page_size
    )
    
    meta = paginate(total, page, page_size)
    return ProductListResponse(items=products, **meta)


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get details of a specific product."""
    service = MarketplaceService(db)
    return await service.get_product(product_id)


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    req: ProductCreate,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db)
):
    """List a new product (Sellers only)."""
    service = MarketplaceService(db)
    return await service.create_product(current_user.id, req)


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    req: ProductUpdate,
    current_user: User = Depends(require_seller),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing product listing."""
    service = MarketplaceService(db)
    return await service.update_product(product_id, current_user.id, req)
