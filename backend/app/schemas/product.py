"""
Product Pydantic schemas.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.utils.constants import FabricType, ProductStatus


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    fabric_type: FabricType
    weaving_style: Optional[str] = Field(default=None, max_length=100)
    color: Optional[str] = Field(default=None, max_length=50)
    dimensions: Optional[str] = Field(default=None, max_length=100)
    weight_grams: Optional[float] = Field(default=None, gt=0)
    stock_quantity: int = Field(default=1, ge=1)

    # Cost breakdown — all required to compute fair price
    material_cost: float = Field(..., ge=0, description="Raw material cost in INR")
    labor_hours: float = Field(..., ge=0, description="Total hours spent weaving")
    labor_cost: float = Field(..., ge=0, description="labor_hours × regional wage")
    dye_cost: float = Field(..., ge=0, description="Cost of dyes in INR")
    transport_cost: float = Field(..., ge=0, description="Logistics cost in INR")
    wastage_cost: float = Field(..., ge=0, description="Estimated wastage in INR")
    profit_margin: float = Field(..., ge=0, description="Desired profit in INR")

    # The seller's chosen listing price — validated >= fair_price in service layer
    selling_price: float = Field(..., gt=0)

    tags: Optional[List[str]] = Field(default=None, max_length=10)

    @field_validator("tags")
    @classmethod
    def limit_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v and len(v) > 10:
            raise ValueError("Maximum 10 tags allowed.")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    fabric_type: Optional[FabricType] = None
    weaving_style: Optional[str] = Field(default=None, max_length=100)
    color: Optional[str] = Field(default=None, max_length=50)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    material_cost: Optional[float] = Field(default=None, ge=0)
    labor_hours: Optional[float] = Field(default=None, ge=0)
    labor_cost: Optional[float] = Field(default=None, ge=0)
    dye_cost: Optional[float] = Field(default=None, ge=0)
    transport_cost: Optional[float] = Field(default=None, ge=0)
    wastage_cost: Optional[float] = Field(default=None, ge=0)
    profit_margin: Optional[float] = Field(default=None, ge=0)
    selling_price: Optional[float] = Field(default=None, gt=0)
    tags: Optional[List[str]] = None


class ProductResponse(BaseModel):
    id: UUID
    seller_id: UUID
    name: str
    description: Optional[str]
    fabric_type: str
    weaving_style: Optional[str]
    color: Optional[str]
    dimensions: Optional[str]
    weight_grams: Optional[float]
    stock_quantity: int
    status: str
    material_cost: float
    labor_hours: float
    labor_cost: float
    dye_cost: float
    transport_cost: float
    wastage_cost: float
    profit_margin: float
    fair_price: float
    recommended_price: float
    premium_price: float
    selling_price: float
    image_urls: Optional[List[str]]
    authenticity_video_url: Optional[str]
    tags: Optional[List[str]]
    is_featured: bool
    view_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
