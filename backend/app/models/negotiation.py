"""
Negotiation and Message ORM models.

Negotiation implements the "Lock & Talk" pattern:
  1. Buyer locks a product → product.status = 'locked'.
  2. Buyer and seller exchange messages in real-time via WebSocket.
  3. Every offer is validated against the fair_price floor before saving.
  4. Seller accepts / rejects / counter-offers.
  5. On acceptance, an Order is created and the product is marked 'sold'.
"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.utils.constants import NegotiationStatus

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User
    from app.models.order import Order


class Negotiation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Represents a single negotiation session between a buyer and a seller
    for a specific product.

    Lifecycle
    ---------
    PENDING → OFFER_MADE → (COUNTERED | ACCEPTED | REJECTED)
    """

    __tablename__ = "negotiations"

    # ── Parties and product ────────────────────────────────────────────────────
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    buyer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    seller_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Negotiation state ──────────────────────────────────────────────────────
    status: Mapped[str] = mapped_column(
        String(20), default=NegotiationStatus.PENDING.value, nullable=False, index=True
    )
    is_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Pricing ────────────────────────────────────────────────────────────────
    fair_price_floor: Mapped[float] = mapped_column(Float, nullable=False)
    buyer_offer_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    seller_counter_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    agreed_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # ── Metadata ───────────────────────────────────────────────────────────────
    seller_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    buyer_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    product: Mapped["Product"] = relationship("Product", back_populates="negotiations")
    buyer: Mapped["User"] = relationship("User", foreign_keys=[buyer_id])
    seller: Mapped["User"] = relationship("User", foreign_keys=[seller_id])
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="negotiation", cascade="all, delete-orphan"
    )
    order: Mapped[Optional["Order"]] = relationship(
        "Order", back_populates="negotiation", uselist=False
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_negotiations_buyer_status", "buyer_id", "status"),
        Index("ix_negotiations_seller_status", "seller_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<Negotiation id={self.id} product={self.product_id} status={self.status}>"


class Message(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    A single chat message inside a negotiation room.

    msg_type options:
        'text'          — plain text message
        'offer'         — buyer submits a price offer
        'counter_offer' — seller counters with a new price
        'system'        — system event (e.g. "deal locked", "offer rejected")
    """

    __tablename__ = "messages"

    negotiation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("negotiations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,  # NULL for system messages
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    msg_type: Mapped[str] = mapped_column(String(20), default="text", nullable=False)

    # ── For offer/counter_offer messages ───────────────────────────────────────
    offer_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    negotiation: Mapped["Negotiation"] = relationship("Negotiation", back_populates="messages")
    sender: Mapped[Optional["User"]] = relationship("User", foreign_keys=[sender_id])

    def __repr__(self) -> str:
        return f"<Message id={self.id} type={self.msg_type} from={self.sender_id}>"
