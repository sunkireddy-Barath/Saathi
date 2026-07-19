"""
Marketplace Service.
Handles product listings, search, and featured products.
"""

from typing import List, Tuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repository.product_repository import ProductRepository
from app.repository.seller_repository import SellerRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.exceptions import NotFoundException, ForbiddenException
from app.services.pricing_service import PricingService
from app.schemas.pricing import FairPriceCalculateRequest


class MarketplaceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.seller_repo = SellerRepository(db)

    async def create_product(self, user_id: UUID, req: ProductCreate) -> Product:
        seller = await self.seller_repo.get_by_user_id(user_id)
        if not seller:
            raise ForbiddenException(detail="Only sellers can create products.")

        # Re-calculate fair price to ensure data integrity
        price_calc = PricingService.calculate_fair_price(
            FairPriceCalculateRequest(
                material_cost=req.material_cost,
                labor_hours=req.labor_hours,
                regional_wage_per_hour=req.labor_cost / req.labor_hours if req.labor_hours > 0 else 0, # Inverse logic just for validation
                dye_cost=req.dye_cost,
                transport_cost=req.transport_cost,
                wastage_cost=req.wastage_cost,
                profit_margin=req.profit_margin
            )
        )
        
        # Enforce that selling price cannot be below fair price
        if req.selling_price < price_calc.fair_price_floor:
            req.selling_price = price_calc.fair_price_floor

        product_data = req.model_dump()
        product_data["seller_id"] = seller.id
        product_data["fair_price"] = price_calc.fair_price_floor
        product_data["recommended_price"] = price_calc.recommended_price
        product_data["premium_price"] = price_calc.premium_price
        
        # Convert enum to value
        product_data["fabric_type"] = req.fabric_type.value

        return await self.product_repo.create(product_data)

    async def update_product(self, product_id: UUID, user_id: UUID, req: ProductUpdate) -> Product:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail="Product not found.")
            
        seller = await self.seller_repo.get_by_user_id(user_id)
        if not seller or product.seller_id != seller.id:
            raise ForbiddenException(detail="Not authorized to edit this product.")

        update_data = req.model_dump(exclude_unset=True)
        if "fabric_type" in update_data and update_data["fabric_type"]:
             update_data["fabric_type"] = update_data["fabric_type"].value
             
        return await self.product_repo.update(product, update_data)

    async def get_product(self, product_id: UUID) -> Product:
        product = await self.product_repo.get_with_seller(product_id)
        if not product:
            raise NotFoundException(detail="Product not found.")
        
        # Increment view count
        await self.product_repo.update(product, {"view_count": product.view_count + 1})
        return product

    async def search_marketplace(
        self,
        search: str | None = None,
        fabric_type: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Product], int]:
        return await self.product_repo.get_marketplace_products(
            search=search,
            fabric_type=fabric_type,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit
        )
