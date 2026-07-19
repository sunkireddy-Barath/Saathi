"""
Dispute Pydantic schemas.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.constants import DisputeStatus, DisputeWinner


class RaiseDisputeRequest(BaseModel):
    order_id: str = Field(..., description="UUID of the order under dispute")
    reason: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=2000)
    evidence_urls: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Comma-separated list of evidence file URLs",
    )


class ResolveDisputeRequest(BaseModel):
    winner: DisputeWinner
    admin_notes: str = Field(..., min_length=10, max_length=2000)


class DisputeResponse(BaseModel):
    id: str
    order_id: str
    raised_by_id: str
    defendant_id: str
    reason: str
    description: str
    evidence_urls: Optional[str]
    status: str
    admin_notes: Optional[str]
    winner: Optional[str]
    resolved_by_id: Optional[str]
    created_at: str

    model_config = {"from_attributes": True}


class DisputeListResponse(BaseModel):
    items: List[DisputeResponse]
    total: int
    page: int
    page_size: int
