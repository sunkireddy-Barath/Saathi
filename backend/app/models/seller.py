"""
SellerProfile ORM model.

Stores artisan-specific details.  One-to-one with ``users``.
The actual product listings are in the ``products`` table.
"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product


class SellerProfile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Extended profile for artisan sellers.

    Verification flags
    ------------------
    aadhaar_verified : Set to True after admin verifies the Aadhaar scan.
    artisan_verified : Set to True after admin verifies the artisan certificate.
    """

    __tablename__ = "seller_profiles"

    # ── Foreign key to users ───────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Artisan identity ───────────────────────────────────────────────────────
    artisan_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    years_of_experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    specialization: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Bank / payment details ─────────────────────────────────────────────────
    bank_account_number: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    ifsc_code: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    upi_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Verification flags ─────────────────────────────────────────────────────
    aadhaar_number: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    aadhaar_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    artisan_certificate_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    artisan_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Aggregate stats (denormalised for fast dashboard reads) ────────────────
    total_sales: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rating_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ──────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="seller_profile")
    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="seller", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<SellerProfile id={self.id} artisan={self.artisan_name}>"
