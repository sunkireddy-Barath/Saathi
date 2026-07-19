"""
Order API Router.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.order import OrderListResponse, OrderResponse
from app.repository.order_repository import OrderRepository
from app.utils.helpers import paginate

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/", response_model=OrderListResponse)
async def get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all orders for the authenticated user (as buyer or seller)."""
    repo = OrderRepository(db)
    skip = (page - 1) * page_size
    orders, total = await repo.get_user_orders(current_user.id, skip=skip, limit=page_size)
    
    meta = paginate(total, page, page_size)
    return OrderListResponse(items=orders, **meta)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get details of a specific order."""
    repo = OrderRepository(db)
    order = await repo.get_by_id(order_id)
    # Authorization logic could be added here
    return order
