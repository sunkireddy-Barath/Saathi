from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.utils.validators import validate_aadhaar_number, validate_phone_number


class SellerProfileCreate(BaseModel):
    artisan_name: str = Field(..., min_length=2, max_length=150)
    state: str = Field(..., max_length=100)
    district: str = Field(..., max_length=100)
    pincode: Optional[str] = Field(default=None, max_length=10)
    years_of_experience: int = Field(default=0, ge=0, le=80)
    specialization: Optional[str] = Field(default=None, max_length=200)
    bio: Optional[str] = Field(default=None, max_length=1000)
    bank_account_number: Optional[str] = Field(default=None, max_length=30)
    ifsc_code: Optional[str] = Field(default=None, max_length=15)
    upi_id: Optional[str] = Field(default=None, max_length=100)
    aadhaar_number: Optional[str] = None

    @field_validator("aadhaar_number")
    @classmethod
    def valid_aadhaar(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_aadhaar_number(v)


class SellerProfileUpdate(BaseModel):
    artisan_name: Optional[str] = Field(default=None, max_length=150)
    state: Optional[str] = Field(default=None, max_length=100)
    district: Optional[str] = Field(default=None, max_length=100)
    pincode: Optional[str] = Field(default=None, max_length=10)
    years_of_experience: Optional[int] = Field(default=None, ge=0, le=80)
    specialization: Optional[str] = Field(default=None, max_length=200)
    bio: Optional[str] = Field(default=None, max_length=1000)
    bank_account_number: Optional[str] = Field(default=None, max_length=30)
    ifsc_code: Optional[str] = Field(default=None, max_length=15)
    upi_id: Optional[str] = Field(default=None, max_length=100)


class SellerProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    artisan_name: Optional[str]
    state: Optional[str]
    district: Optional[str]
    years_of_experience: int
    specialization: Optional[str]
    bio: Optional[str]
    upi_id: Optional[str]
    aadhaar_verified: bool
    artisan_verified: bool
    total_sales: int
    total_revenue: float
    avg_rating: float
    rating_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SellerDashboardResponse(BaseModel):
    profile: SellerProfileResponse
    trust_score: int
    active_products: int
    pending_orders: int
    total_revenue: float
    avg_rating: float
    recent_negotiations: int
