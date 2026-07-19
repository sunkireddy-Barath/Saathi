"""
Negotiation and Message Pydantic schemas.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.constants import NegotiationStatus


class LockDealRequest(BaseModel):
    product_id: str = Field(..., description="UUID of the product to lock")


class SubmitOfferRequest(BaseModel):
    offer_price: float = Field(..., gt=0, description="Buyer's offered price in INR")
    note: Optional[str] = Field(default=None, max_length=500)


class RespondToOfferRequest(BaseModel):
    action: str = Field(
        ...,
        pattern="^(accept|reject|counter)$",
        description="Seller's response: accept, reject, or counter",
    )
    counter_price: Optional[float] = Field(
        default=None, gt=0, description="Required when action is 'counter'"
    )
    note: Optional[str] = Field(default=None, max_length=500)


class MessageResponse(BaseModel):
    id: str
    negotiation_id: str
    sender_id: Optional[str]
    content: str
    msg_type: str
    offer_amount: Optional[float]
    created_at: str

    model_config = {"from_attributes": True}


class NegotiationResponse(BaseModel):
    id: str
    product_id: str
    buyer_id: str
    seller_id: str
    status: str
    is_locked: bool
    fair_price_floor: float
    buyer_offer_price: Optional[float]
    seller_counter_price: Optional[float]
    agreed_price: Optional[float]
    seller_note: Optional[str]
    buyer_note: Optional[str]
    created_at: str
    messages: List[MessageResponse] = []

    model_config = {"from_attributes": True}
