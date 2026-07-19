"""
Product ORM model.

Represents a single handloom product listed by a seller.

Cost breakdown columns (material_cost, labor_cost, dye_cost, etc.) feed
directly into the Fair Price Engine so the server can re-validate prices
at any time without asking the seller to re-enter data.
"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.utils.constants import ProductStatus, FabricType

if TYPE_CHECKING:
    from app.models.seller import SellerProfile
    from app.models.negotiation import Negotiation
    from app.models.order import Order
    from app.models.prediction import Prediction


class Product(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    A handloom product listing.

    Fair Price columns
    ------------------
    material_cost  : Raw material cost in INR.
    labor_cost     : Total labour cost = labor_hours × regional_wage_per_hour.
    dye_cost       : Cost of dyes used.
    transport_cost : Estimated transport/logistics cost.
    wastage_cost   : Estimated wastage during weaving.
    profit_margin  : Desired profit in INR (not percentage).
    fair_price     : Computed = sum of all cost columns + profit_margin.
    selling_price  : The price the seller actually lists (must be >= fair_price).
    """

    __tablename__ = "products"

    # ── Foreign key to seller ──────────────────────────────────────────────────
    seller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("seller_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Basic info ─────────────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fabric_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    weaving_style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dimensions: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g. "6m x 1.2m"
    weight_grams: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # ── Inventory ──────────────────────────────────────────────────────────────
    stock_quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=ProductStatus.ACTIVE.value, nullable=False, index=True
    )

    # ── Cost breakdown ─────────────────────────────────────────────────────────
    material_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    labor_hours: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    labor_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    dye_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    transport_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    wastage_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    profit_margin: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # ── Computed price fields ──────────────────────────────────────────────────
    fair_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    recommended_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    premium_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    selling_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # ── Media ─────────────────────────────────────────────────────────────────
    image_urls: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    authenticity_video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ── Tags and metadata ──────────────────────────────────────────────────────
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ──────────────────────────────────────────────────────────
    seller: Mapped["SellerProfile"] = relationship("SellerProfile", back_populates="products")
    negotiations: Mapped[List["Negotiation"]] = relationship(
        "Negotiation", back_populates="product", cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="product", cascade="all, delete-orphan"
    )
    predictions: Mapped[List["Prediction"]] = relationship(
        "Prediction", back_populates="product", cascade="all, delete-orphan"
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_products_fabric_status", "fabric_type", "status"),
        Index("ix_products_seller_status", "seller_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name} status={self.status}>"
