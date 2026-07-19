"""
Models package.

Import all ORM models here so SQLAlchemy's metadata object knows about
every table.  This is required for Alembic autogenerate to work correctly
and for create_all_tables() in database.py.
"""

from app.models.user import User
from app.models.seller import SellerProfile
from app.models.buyer import BuyerProfile
from app.models.product import Product
from app.models.negotiation import Negotiation, Message
from app.models.order import Order
from app.models.dispute import Dispute
from app.models.trust import TrustEvent
from app.models.prediction import Prediction
from app.models.audit import AuditLog

__all__ = [
    "User",
    "SellerProfile",
    "BuyerProfile",
    "Product",
    "Negotiation",
    "Message",
    "Order",
    "Dispute",
    "TrustEvent",
    "Prediction",
    "AuditLog",
]
