"""
AuditLog ORM model.

Records every significant action performed in the system, including
admin actions, account changes, and dispute resolutions.

This table is append-only — no rows should ever be updated or deleted.
"""

import uuid
from typing import Any, Dict, Optional

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin


class AuditLog(Base, UUIDPrimaryKeyMixin):
    """
    Immutable audit trail entry.

    Fields
    ------
    actor_id  : The user who performed the action (NULL for system actions).
    action    : Short verb describing what happened, e.g. "user.suspend".
    resource  : The type of entity affected, e.g. "user", "product".
    resource_id: The UUID of the affected entity.
    payload   : Additional context as a JSON object.
    ip_address: IP of the client that triggered the action.
    """

    __tablename__ = "audit_logs"

    # ── Who did it ─────────────────────────────────────────────────────────────
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ── What happened ──────────────────────────────────────────────────────────
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # ── When it happened (NOT using TimestampMixin to avoid updated_at) ────────
    from sqlalchemy import DateTime, func
    from datetime import datetime

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_audit_logs_action_resource", "action", "resource"),
        Index("ix_audit_logs_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AuditLog actor={self.actor_id} action={self.action} resource={self.resource}>"
