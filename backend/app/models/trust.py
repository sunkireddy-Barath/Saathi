"""
TrustEvent ORM model.

Every change to a user's trust score is recorded as an immutable event.
The user's current ``trust_score`` on the ``users`` table is the running sum
of all events — keeping both lets us display history and recompute if needed.
"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.utils.constants import TrustEventType

if TYPE_CHECKING:
    from app.models.user import User


class TrustEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Immutable audit log entry for a trust score change.

    A negative ``delta`` reduces the score; a positive ``delta`` increases it.
    ``performed_by_id`` is set when an admin manually adjusts the score, and
    is NULL for system-generated events.
    """

    __tablename__ = "trust_events"

    # ── Target user ────────────────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Event ──────────────────────────────────────────────────────────────────
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    delta: Mapped[int] = mapped_column(Integer, nullable=False)      # Signed integer
    score_before: Mapped[int] = mapped_column(Integer, nullable=False)
    score_after: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Reference to the triggering entity ────────────────────────────────────
    reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )  # e.g. order_id, dispute_id

    # ── Performed by (admin, or NULL for system) ───────────────────────────────
    performed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="trust_events")
    performed_by: Mapped[Optional["User"]] = relationship("User", foreign_keys=[performed_by_id])

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_trust_events_user_type", "user_id", "event_type"),
    )

    def __repr__(self) -> str:
        return (
            f"<TrustEvent user={self.user_id} type={self.event_type} "
            f"delta={self.delta:+d} ({self.score_before}→{self.score_after})>"
        )
