"""
Order Pydantic schemas.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.constants import DeliveryStatus, OrderStatus, PaymentType


class ConfirmPurchaseRequest(BaseModel):
    product_id: str
    negotiation_id: Optional[str] = None
    payment_type: PaymentType = PaymentType.ONLINE
    payment_reference: Optional[str] = Field(default=None, max_length=100)


class SubmitRatingRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(default=None, max_length=500)


class OrderResponse(BaseModel):
    id: str
    buyer_id: str
    seller_id: str
    product_id: str
    negotiation_id: Optional[str]
    amount: float
    payment_type: str
    status: str
    delivery_status: str
    tracking_number: Optional[str]
    buyer_rating: Optional[int]
    buyer_review: Optional[str]
    rating_submitted: bool
    created_at: str

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    items: List[OrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
