"""
Trust Pydantic schemas.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.constants import TrustEventType


class TrustEventResponse(BaseModel):
    id: str
    user_id: str
    event_type: str
    delta: int
    score_before: int
    score_after: int
    reason: Optional[str]
    reference_id: Optional[str]
    performed_by_id: Optional[str]
    created_at: str

    model_config = {"from_attributes": True}


class TrustScoreResponse(BaseModel):
    user_id: str
    current_score: int
    can_negotiate: bool
    is_suspended: bool
    recent_events: List[TrustEventResponse]


class AdminTrustAdjustRequest(BaseModel):
    delta: int = Field(..., description="Positive to add, negative to subtract")
    reason: str = Field(..., min_length=5, max_length=500)
