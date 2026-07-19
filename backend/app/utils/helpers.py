"""
General-purpose helper functions shared across the application.
"""

import math
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, TypeVar

T = TypeVar("T")


def utcnow() -> datetime:
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(tz=timezone.utc)


def generate_uuid() -> uuid.UUID:
    """Return a new random UUID v4."""
    return uuid.uuid4()


def paginate(query_total: int, page: int, page_size: int) -> dict[str, Any]:
    """
    Build pagination metadata for a list response.

    Args:
        query_total: Total number of records matching the query.
        page:        Current page (1-indexed).
        page_size:   Number of records per page.

    Returns:
        A dict with pagination metadata suitable for including in API responses.
    """
    total_pages = math.ceil(query_total / page_size) if page_size > 0 else 0
    return {
        "total": query_total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


def slugify(text: str) -> str:
    """Convert a human-readable string to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def mask_email(email: str) -> str:
    """
    Mask an email address for safe display in logs.

    Example: "john.doe@example.com" → "jo*****e@example.com"
    """
    parts = email.split("@")
    if len(parts) != 2:
        return "***"
    local = parts[0]
    domain = parts[1]
    if len(local) <= 2:
        masked_local = "*" * len(local)
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked_local}@{domain}"


def rupees(amount: float) -> str:
    """Format a float as Indian Rupee string (e.g. ₹1,23,456.00)."""
    formatted = f"{amount:,.2f}"
    return f"₹{formatted}"


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp *value* between *minimum* and *maximum*."""
    return max(minimum, min(value, maximum))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Divide *numerator* by *denominator*, returning *default* if denominator is 0."""
    if denominator == 0:
        return default
    return numerator / denominator
