"""
BuyerProfile ORM model.

Stores business-specific details for buyers.  One-to-one with ``users``.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class BuyerProfile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Extended profile for buyers (retailers, wholesalers, exporters, individuals).
    """

    __tablename__ = "buyer_profiles"

    # ── Foreign key to users ───────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Business identity ──────────────────────────────────────────────────────
    company_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    gst_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    business_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    shipping_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    billing_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Relationship ───────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="buyer_profile")

    def __repr__(self) -> str:
        return f"<BuyerProfile id={self.id} company={self.company_name}>"
