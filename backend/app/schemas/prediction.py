"""
Prediction Pydantic schemas.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    id: str
    product_id: str
    seller_id: str
    forecast_data: Optional[Dict[str, Any]]
    confidence_score: float
    best_selling_window: Optional[str]
    worst_selling_window: Optional[str]
    expected_demand_units: Optional[int]
    expected_revenue: Optional[float]
    competition_level: Optional[str]
    recommendation: Optional[Dict[str, Any]]
    model_version: str
    created_at: str

    model_config = {"from_attributes": True}
