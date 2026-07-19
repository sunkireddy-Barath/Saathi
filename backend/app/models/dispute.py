"""
Dispute ORM model.

A buyer or seller can raise a dispute against an order.  Disputes are
reviewed by admins who can then adjust trust scores and resolve the case.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.utils.constants import DisputeStatus, DisputeWinner

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.order import Order


class Dispute(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Dispute raised by a buyer or seller about an order.

    Fields
    ------
    raised_by_id  : The user who opened the dispute.
    defendant_id  : The user against whom the dispute is raised.
    winner        : Set by admin when resolving — 'buyer', 'seller', or 'split'.
    """

    __tablename__ = "disputes"

    # ── Linked order ───────────────────────────────────────────────────────────
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ── Parties ────────────────────────────────────────────────────────────────
    raised_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    defendant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # ── Dispute details ────────────────────────────────────────────────────────
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_urls: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated

    # ── Resolution ─────────────────────────────────────────────────────────────
    status: Mapped[str] = mapped_column(
        String(30), default=DisputeStatus.OPEN.value, nullable=False, index=True
    )
    admin_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    winner: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    resolved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    order: Mapped["Order"] = relationship("Order", back_populates="dispute")
    raised_by: Mapped["User"] = relationship("User", foreign_keys=[raised_by_id])
    defendant: Mapped["User"] = relationship("User", foreign_keys=[defendant_id])
    resolved_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[resolved_by_id])

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_disputes_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Dispute id={self.id} status={self.status} order={self.order_id}>"
