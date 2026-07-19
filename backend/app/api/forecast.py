"""
Pricing & Forecast API Routers.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_seller
from app.schemas.pricing import FairPriceCalculateRequest, FairPriceResponse
from app.schemas.prediction import PredictionResponse
from app.services.pricing_service import PricingService
from app.services.prediction_service import PredictionService

pricing_router = APIRouter(prefix="/api/v1/pricing", tags=["Pricing"])
forecast_router = APIRouter(prefix="/api/v1/forecast", tags=["Forecast"])


@pricing_router.post("/calculate", response_model=FairPriceResponse)
async def calculate_fair_price(
    req: FairPriceCalculateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Calculate the Fair Price floor based on cost inputs."""
    # Stateless calculation, no DB save here
    return PricingService.calculate_fair_price(req)


@forecast_router.get("/{product_id}", response_model=PredictionResponse)
async def get_forecast(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get the latest AI demand forecast for a product."""
    service = PredictionService(db)
    return await service.get_latest_prediction(product_id)
