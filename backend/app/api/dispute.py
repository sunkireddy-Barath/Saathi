"""
Dispute API Router.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, require_admin
from app.models.user import User
from app.schemas.dispute import DisputeListResponse, DisputeResponse, RaiseDisputeRequest, ResolveDisputeRequest
from app.services.dispute_service import DisputeService
from app.repository.dispute_repository import DisputeRepository

router = APIRouter(prefix="/api/v1/disputes", tags=["Disputes"])


@router.post("/", response_model=DisputeResponse, status_code=status.HTTP_201_CREATED)
async def raise_dispute(
    req: RaiseDisputeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Raise a dispute for an order."""
    service = DisputeService(db)
    return await service.raise_dispute(current_user.id, req)


@router.get("/", response_model=DisputeListResponse)
async def get_user_disputes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get disputes involving the current user."""
    repo = DisputeRepository(db)
    skip = (page - 1) * page_size
    disputes, total = await repo.get_user_disputes(current_user.id, skip=skip, limit=page_size)
    
    return DisputeListResponse(
        items=disputes, total=total, page=page, page_size=page_size
    )


@router.put("/{dispute_id}/resolve", response_model=DisputeResponse)
async def resolve_dispute(
    dispute_id: UUID,
    req: ResolveDisputeRequest,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Resolve a dispute (Admin only)."""
    service = DisputeService(db)
    return await service.resolve_dispute(dispute_id, current_user, req)
