"""
Buyer Pydantic schemas.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.utils.validators import validate_gst_number


class BuyerProfileCreate(BaseModel):
    company_name: Optional[str] = Field(default=None, max_length=200)
    gst_number: Optional[str] = None
    business_type: Optional[str] = Field(default=None, max_length=50)
    shipping_address: Optional[str] = Field(default=None, max_length=500)
    billing_address: Optional[str] = Field(default=None, max_length=500)

    @field_validator("gst_number")
    @classmethod
    def valid_gst(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_gst_number(v)


class BuyerProfileUpdate(BuyerProfileCreate):
    pass


class BuyerProfileResponse(BaseModel):
    id: str
    user_id: str
    company_name: Optional[str]
    gst_number: Optional[str]
    business_type: Optional[str]
    shipping_address: Optional[str]
    created_at: str

    model_config = {"from_attributes": True}
