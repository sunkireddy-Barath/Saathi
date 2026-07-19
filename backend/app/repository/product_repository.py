"""
Product Repository.
"""

from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.repository.base_repository import BaseRepository
from app.utils.constants import ProductStatus


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Product, db_session)

    async def get_with_seller(self, product_id: UUID | str) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.seller))
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_seller_products(
        self, seller_id: UUID | str, skip: int = 0, limit: int = 20
    ) -> Tuple[List[Product], int]:
        base_stmt = select(Product).where(Product.seller_id == seller_id)
        
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = await self.db_session.scalar(count_stmt) or 0
        
        stmt = base_stmt.order_by(Product.created_at.desc()).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        
        return list(result.scalars().all()), total

    async def get_marketplace_products(
        self,
        search: Optional[str] = None,
        fabric_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Product], int]:
        conditions = [Product.status == ProductStatus.ACTIVE.value]

        if search:
            conditions.append(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                    Product.fabric_type.ilike(f"%{search}%"),
                )
            )
        if fabric_type:
            conditions.append(Product.fabric_type == fabric_type)
        if min_price is not None:
            conditions.append(Product.selling_price >= min_price)
        if max_price is not None:
            conditions.append(Product.selling_price <= max_price)

        base_stmt = select(Product).where(and_(*conditions))
        
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = await self.db_session.scalar(count_stmt) or 0
        
        stmt = base_stmt.order_by(Product.created_at.desc()).offset(skip).limit(limit)
        result = await self.db_session.execute(stmt)
        
        return list(result.scalars().all()), total
