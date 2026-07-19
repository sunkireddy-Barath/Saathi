"""
Negotiation API Router.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, require_buyer
from app.models.user import User
from app.schemas.negotiation import LockDealRequest, NegotiationResponse
from app.models.negotiation import Negotiation
from app.repository.negotiation_repository import NegotiationRepository
from app.repository.product_repository import ProductRepository
from app.utils.constants import NegotiationStatus, ProductStatus
from app.utils.exceptions import ConflictException, NotFoundException

router = APIRouter(prefix="/api/v1/negotiation", tags=["Negotiation"])


@router.post("/lock", response_model=NegotiationResponse, status_code=status.HTTP_201_CREATED)
async def lock_deal(
    req: LockDealRequest,
    current_user: User = Depends(require_buyer),
    db: AsyncSession = Depends(get_db)
):
    """
    Lock a product for negotiation. Prevents other buyers from negotiating.
    """
    product_repo = ProductRepository(db)
    neg_repo = NegotiationRepository(db)
    
    product = await product_repo.get_by_id(UUID(req.product_id))
    if not product:
        raise NotFoundException("Product not found")
        
    if product.status != ProductStatus.ACTIVE.value:
        raise ConflictException("Product is not available for negotiation.")
        
    # Check if a negotiation already exists
    active_neg = await neg_repo.get_active_for_product(product.id)
    if active_neg:
        raise ConflictException("Product is already locked by another buyer.")
        
    # Lock product
    await product_repo.update(product, {"status": ProductStatus.LOCKED.value})
    
    # Create Negotiation Room
    neg_data = {
        "product_id": product.id,
        "buyer_id": current_user.id,
        "seller_id": product.seller_id,
        "status": NegotiationStatus.PENDING.value,
        "is_locked": True,
        "fair_price_floor": product.fair_price,
    }
    return await neg_repo.create(neg_data)


@router.get("/{negotiation_id}", response_model=NegotiationResponse)
async def get_negotiation(
    negotiation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get negotiation details including message history."""
    neg_repo = NegotiationRepository(db)
    neg = await neg_repo.get_with_messages(negotiation_id)
    if not neg:
        raise NotFoundException("Negotiation not found")
    return neg
