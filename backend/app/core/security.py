"""
Security utilities — password hashing and JWT token management.

All token operations are centralised here so the rest of the codebase
never imports jose or passlib directly.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# ── Password hashing ───────────────────────────────────────────────────────────
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash of *plain_password*."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if *plain_password* matches the stored *hashed_password*."""
    return _pwd_context.verify(plain_password, hashed_password)


# ── JWT helpers ────────────────────────────────────────────────────────────────
def _create_token(subject: Any, token_type: str, expires_delta: timedelta) -> str:
    """
    Internal helper that creates a signed JWT.

    Args:
        subject:      The value to embed as the ``sub`` claim (usually user id).
        token_type:   ``"access"`` or ``"refresh"``.
        expires_delta: How long until the token expires.

    Returns:
        A compact serialised JWT string.
    """
    now = datetime.now(tz=timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: Any) -> str:
    """Create a short-lived access token."""
    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: Any) -> str:
    """Create a long-lived refresh token."""
    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """
    Decode and verify a JWT.

    Returns the payload dict on success, or None if the token is invalid
    or expired.  Callers should treat None as an authentication failure.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None


def extract_user_id(token: str) -> Optional[str]:
    """
    Convenience wrapper — returns the ``sub`` claim or None.
    """
    payload = decode_token(token)
    if payload is None:
        return None
    return payload.get("sub")
