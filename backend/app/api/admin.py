"""
Admin API Router.
"""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.trust import AdminTrustAdjustRequest, TrustEventResponse
from app.services.trust_service import TrustService

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.post("/users/{user_id}/trust", response_model=TrustEventResponse)
async def adjust_user_trust(
    user_id: UUID,
    req: AdminTrustAdjustRequest,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Manually adjust a user's trust score."""
    service = TrustService(db)
    return await service.custom_admin_adjustment(
        user_id=user_id,
        delta=req.delta,
        reason=req.reason,
        admin_id=current_admin.id
    )
