"""
User ORM model.

Every person who uses the platform (seller, buyer, or admin) has exactly
one row in the ``users`` table.  Role-specific data lives in the
``seller_profiles`` or ``buyer_profiles`` tables (one-to-one).
"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.utils.constants import UserRole, TrustThreshold

if TYPE_CHECKING:
    from app.models.seller import SellerProfile
    from app.models.buyer import BuyerProfile
    from app.models.order import Order
    from app.models.dispute import Dispute
    from app.models.trust import TrustEvent
    from app.models.audit import AuditLog


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    Central user record shared across all roles.

    Fields
    ------
    role        : One of 'seller', 'buyer', 'admin'.
    trust_score : Integer score in the range [0, 200+].  Starts at 100.
    is_active   : Set to False when an account is suspended.
    """

    __tablename__ = "users"

    # ── Core identity ──────────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Role & status ──────────────────────────────────────────────────────────
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, default=UserRole.BUYER.value, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Trust ──────────────────────────────────────────────────────────────────
    trust_score: Mapped[int] = mapped_column(
        Integer, default=TrustThreshold.STARTING, nullable=False
    )

    # ── Profile picture ────────────────────────────────────────────────────────
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ── Relationships ──────────────────────────────────────────────────────────
    seller_profile: Mapped[Optional["SellerProfile"]] = relationship(
        "SellerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    buyer_profile: Mapped[Optional["BuyerProfile"]] = relationship(
        "BuyerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    trust_events: Mapped[List["TrustEvent"]] = relationship(
        "TrustEvent", back_populates="user", cascade="all, delete-orphan"
    )

    # ── Table-level indexes ────────────────────────────────────────────────────
    __table_args__ = (
        Index("ix_users_role_active", "role", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
