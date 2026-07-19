"""
Prediction ORM model.

Stores the output of the AI forecast engine for a given product.
Results are cached here so dashboards can load instantly without
re-running expensive model inference on every page view.
"""

import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.seller import SellerProfile


class Prediction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Cached AI forecast result for a product.

    Columns
    -------
    forecast_data      : Full 30-day daily demand forecast as JSON array.
    confidence_score   : Model confidence (0.0 – 1.0).
    best_selling_window: Natural-language string e.g. "Oct 1 – Oct 15".
    worst_selling_window: Natural-language string e.g. "Jan 5 – Jan 20".
    recommendation     : AI recommendation text / structured JSON.
    model_version      : Which model version produced this prediction.
    """

    __tablename__ = "predictions"

    # ── References ────────────────────────────────────────────────────────────
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    seller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("seller_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Forecast outputs ───────────────────────────────────────────────────────
    forecast_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    best_selling_window: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    worst_selling_window: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Revenue forecast ───────────────────────────────────────────────────────
    expected_demand_units: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    expected_revenue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    competition_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # ── Recommendation ─────────────────────────────────────────────────────────
    recommendation: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    model_version: Mapped[str] = mapped_column(String(50), default="hybrid_v1", nullable=False)

    # ── Relationships ──────────────────────────────────────────────────────────
    product: Mapped["Product"] = relationship("Product", back_populates="predictions")
    seller: Mapped["SellerProfile"] = relationship("SellerProfile")

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_predictions_product_created", "product_id", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<Prediction id={self.id} product={self.product_id} "
            f"confidence={self.confidence_score:.2f}>"
        )
