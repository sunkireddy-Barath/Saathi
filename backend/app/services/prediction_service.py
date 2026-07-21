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

        # Call the actual AI Engine Microservice
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.AI_ENGINE_URL}/predict", 
                    json={
                        "product_id": str(product_id),
                        "category": product.category if hasattr(product, 'category') else 'Silk' # Default fallback
                    },
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Add expected revenue based on the dynamic units calculated by the ML model
                data['expected_revenue'] = data.get('expected_demand_units', 0) * product.selling_price

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
