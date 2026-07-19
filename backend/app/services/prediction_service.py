"""
Prediction Service.
Connects to the external AI Engine (FastAPI -> FastAPI).
"""

import httpx
from typing import Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.prediction import Prediction
from app.models.product import Product
from app.repository.prediction_repository import PredictionRepository
from app.repository.product_repository import ProductRepository
from app.utils.exceptions import NotFoundException
from app.utils.logger import logger


class PredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.prediction_repo = PredictionRepository(db)
        self.product_repo = ProductRepository(db)

    async def fetch_and_store_prediction(self, product_id: UUID) -> Prediction:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail="Product not found.")

        # Simulate or make actual call to AI Engine
        try:
            async with httpx.AsyncClient() as client:
                # In production, this would hit the actual AI microservice
                # response = await client.post(f"{settings.AI_ENGINE_URL}/predict", json={"product_id": str(product_id)})
                # response.raise_for_status()
                # data = response.json()
                
                # For now, mock the response structure as requested
                data = {
                    "forecast_data": {"days": list(range(1, 31)), "demand": [10, 12, 15, 20, 25, 30, 28, 25, 20, 15, 10, 8, 5, 5, 8, 10, 15, 20, 25, 30, 35, 40, 45, 50, 48, 45, 40, 35, 30, 25]},
                    "confidence_score": 0.85,
                    "best_selling_window": "Days 20-25",
                    "worst_selling_window": "Days 12-14",
                    "expected_demand_units": 150,
                    "expected_revenue": 150 * product.selling_price,
                    "competition_level": "Medium",
                    "recommendation": {"action": "increase_stock", "reason": "Upcoming festival peak detected"},
                    "model_version": "hybrid_v1"
                }
        except Exception as e:
            logger.error(f"Failed to fetch prediction from AI Engine: {str(e)}")
            raise
            
        prediction_data = {
            "product_id": product.id,
            "seller_id": product.seller_id,
            "forecast_data": data["forecast_data"],
            "confidence_score": data["confidence_score"],
            "best_selling_window": data["best_selling_window"],
            "worst_selling_window": data["worst_selling_window"],
            "expected_demand_units": data["expected_demand_units"],
            "expected_revenue": data["expected_revenue"],
            "competition_level": data["competition_level"],
            "recommendation": data["recommendation"],
            "model_version": data["model_version"]
        }

        return await self.prediction_repo.create(prediction_data)

    async def get_latest_prediction(self, product_id: UUID) -> Prediction:
        prediction = await self.prediction_repo.get_latest_for_product(product_id)
        if not prediction:
            # Generate one on the fly if it doesn't exist
            return await self.fetch_and_store_prediction(product_id)
        return prediction
