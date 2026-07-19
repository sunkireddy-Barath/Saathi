"""
Application-wide constants and enumerations.

Using Python Enum classes instead of bare strings prevents typos and makes
the code self-documenting.
"""

from enum import Enum


# ── User roles ─────────────────────────────────────────────────────────────────
class UserRole(str, Enum):
    SELLER = "seller"
    BUYER = "buyer"
    ADMIN = "admin"


# ── Product status ─────────────────────────────────────────────────────────────
class ProductStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"       # A buyer has locked it for negotiation
    SOLD = "sold"
    INACTIVE = "inactive"


# ── Negotiation status ─────────────────────────────────────────────────────────
class NegotiationStatus(str, Enum):
    PENDING = "pending"         # Buyer locked, no offer yet
    OFFER_MADE = "offer_made"   # Buyer submitted an offer
    COUNTERED = "countered"     # Seller sent a counter-offer
    ACCEPTED = "accepted"       # Both parties agreed
    REJECTED = "rejected"       # Seller rejected the offer
    EXPIRED = "expired"         # Timed out without agreement


# ── Order status ───────────────────────────────────────────────────────────────
class OrderStatus(str, Enum):
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# ── Delivery status ────────────────────────────────────────────────────────────
class DeliveryStatus(str, Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    RETURNED = "returned"


# ── Dispute status ─────────────────────────────────────────────────────────────
class DisputeStatus(str, Enum):
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    CLOSED = "closed"


# ── Dispute winner ─────────────────────────────────────────────────────────────
class DisputeWinner(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    SPLIT = "split"


# ── Trust event types ──────────────────────────────────────────────────────────
class TrustEventType(str, Enum):
    TRANSACTION_COMPLETE = "transaction_complete"   # +5
    POSITIVE_RATING = "positive_rating"             # +2
    FALSE_DISPUTE = "false_dispute"                 # -20
    FRAUD_DETECTED = "fraud_detected"               # -40
    ADMIN_ADJUSTMENT = "admin_adjustment"           # custom
    DISPUTE_RAISED = "dispute_raised"               # 0 (event log only)
    DISPUTE_WON = "dispute_won"                     # +3
    DISPUTE_LOST = "dispute_lost"                   # -5


# ── Trust score thresholds ─────────────────────────────────────────────────────
class TrustThreshold:
    STARTING = 100
    NEGOTIATION_DISABLED = 40   # Cannot initiate new negotiations below this
    ACCOUNT_SUSPENDED = 20      # Account is auto-suspended below this


# ── Trust score deltas ─────────────────────────────────────────────────────────
TRUST_DELTA: dict[TrustEventType, int] = {
    TrustEventType.TRANSACTION_COMPLETE: +5,
    TrustEventType.POSITIVE_RATING: +2,
    TrustEventType.FALSE_DISPUTE: -20,
    TrustEventType.FRAUD_DETECTED: -40,
    TrustEventType.DISPUTE_WON: +3,
    TrustEventType.DISPUTE_LOST: -5,
}

# ── Payment types ──────────────────────────────────────────────────────────────
class PaymentType(str, Enum):
    ONLINE = "online"
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    COD = "cod"


# ── Fabric types ───────────────────────────────────────────────────────────────
class FabricType(str, Enum):
    SILK = "silk"
    COTTON = "cotton"
    WOOL = "wool"
    LINEN = "linen"
    JUTE = "jute"
    BANARASI = "banarasi"
    CHANDERI = "chanderi"
    KHADI = "khadi"
    PASHMINA = "pashmina"
    OTHER = "other"


# ── Business type (Buyer) ──────────────────────────────────────────────────────
class BusinessType(str, Enum):
    RETAILER = "retailer"
    WHOLESALER = "wholesaler"
    EXPORTER = "exporter"
    INDIVIDUAL = "individual"
    NGO = "ngo"


# ── Pagination defaults ────────────────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
