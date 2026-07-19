"""
Trust API Router.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.trust import TrustScoreResponse
from app.repository.trust_repository import TrustRepository
from app.utils.constants import TrustThreshold

router = APIRouter(prefix="/api/v1/trust", tags=["Trust"])


@router.get("/score", response_model=TrustScoreResponse)
async def get_my_trust_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the current user's trust score and recent events."""
    repo = TrustRepository(db)
    events = await repo.get_user_events(current_user.id, limit=10)
    
    return TrustScoreResponse(
        user_id=str(current_user.id),
        current_score=current_user.trust_score,
        can_negotiate=current_user.trust_score >= TrustThreshold.NEGOTIATION_DISABLED,
        is_suspended=not current_user.is_active,
        recent_events=events,
    )
