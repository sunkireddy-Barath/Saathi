"""
Order ORM model.

An Order is created when a negotiation reaches 'accepted' status or
when a buyer purchases a product at the listed price without negotiation.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.utils.constants import DeliveryStatus, OrderStatus, PaymentType

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product
    from app.models.negotiation import Negotiation
    from app.models.dispute import Dispute


class Order(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Represents a confirmed purchase transaction.

    The ``amount`` field captures the final agreed price (which may differ
    from the product's listing price if a negotiation occurred).
    """

    __tablename__ = "orders"

    # ── Parties and product ────────────────────────────────────────────────────
    buyer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    seller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )
    negotiation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("negotiations.id", ondelete="SET NULL"),
        nullable=True,  # Null for direct purchases
    )

    # ── Financial ──────────────────────────────────────────────────────────────
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_type: Mapped[str] = mapped_column(
        String(30), default=PaymentType.ONLINE.value, nullable=False
    )
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Status ─────────────────────────────────────────────────────────────────
    status: Mapped[str] = mapped_column(
        String(30), default=OrderStatus.CONFIRMED.value, nullable=False, index=True
    )
    delivery_status: Mapped[str] = mapped_column(
        String(30), default=DeliveryStatus.PENDING.value, nullable=False
    )
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Rating ─────────────────────────────────────────────────────────────────
    buyer_rating: Mapped[Optional[int]] = mapped_column(nullable=True)       # 1–5
    buyer_review: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    rating_submitted: Mapped[bool] = mapped_column(default=False, nullable=False)

    # ── Relationships ──────────────────────────────────────────────────────────
    buyer: Mapped["User"] = relationship("User", foreign_keys=[buyer_id])
    seller: Mapped["User"] = relationship("User", foreign_keys=[seller_id])
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    negotiation: Mapped[Optional["Negotiation"]] = relationship(
        "Negotiation", back_populates="order"
    )
    dispute: Mapped[Optional["Dispute"]] = relationship(
        "Dispute", back_populates="order", uselist=False
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_orders_buyer_status", "buyer_id", "status"),
        Index("ix_orders_seller_status", "seller_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} amount={self.amount} status={self.status}>"
