"""
Pricing Pydantic schemas.
"""

from pydantic import BaseModel, Field


class FairPriceCalculateRequest(BaseModel):
    material_cost: float = Field(..., ge=0)
    labor_hours: float = Field(..., ge=0)
    regional_wage_per_hour: float = Field(..., ge=0)
    dye_cost: float = Field(default=0.0, ge=0)
    transport_cost: float = Field(default=0.0, ge=0)
    wastage_cost: float = Field(default=0.0, ge=0)
    profit_margin: float = Field(..., ge=0)


class FairPriceResponse(BaseModel):
    labor_cost_total: float
    fair_price_floor: float
    recommended_price: float
    premium_price: float
    breakdown: dict[str, float]
