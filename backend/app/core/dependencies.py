"""
FastAPI dependency functions.

These are the reusable ``Depends()`` callables injected into route handlers.
Keeping them in one file avoids circular imports and makes the DI graph obvious.
"""

from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionFactory
from app.core.security import decode_token
from app.utils.constants import UserRole
from app.utils.exceptions import (
    CredentialsException,
    ForbiddenException,
    AccountSuspendedException,
)

# ── HTTP Bearer extractor ──────────────────────────────────────────────────────
bearer_scheme = HTTPBearer(auto_error=False)


# ── Database session ───────────────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a SQLAlchemy async session for the duration of a single request.

    The session is committed on clean exit and rolled back on any exception.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Current user resolution ────────────────────────────────────────────────────
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Validate the Bearer token and return the active User ORM object.

    Raises 401 if the token is missing, invalid, or expired.
    Raises 403 if the account is suspended.
    """
    # Deferred import to avoid circular dependency with models
    from app.repository.user_repository import UserRepository

    if credentials is None:
        raise CredentialsException()

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("type") != "access":
        raise CredentialsException()

    user_id_str: str | None = payload.get("sub")
    if user_id_str is None:
        raise CredentialsException()

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise CredentialsException()

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)

    if user is None:
        raise CredentialsException()

    if not user.is_active:
        raise AccountSuspendedException()

    return user


# ── Role guards ────────────────────────────────────────────────────────────────
def require_role(*roles: UserRole):
    """
    Factory that returns a dependency enforcing one of the given roles.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role(UserRole.ADMIN))])
    """
    async def _guard(current_user=Depends(get_current_user)):
        if current_user.role not in [r.value for r in roles]:
            raise ForbiddenException(
                detail=f"This endpoint requires one of these roles: {[r.value for r in roles]}"
            )
        return current_user

    return _guard


# ── Convenience aliases ────────────────────────────────────────────────────────
require_seller = require_role(UserRole.SELLER)
require_buyer = require_role(UserRole.BUYER)
require_admin = require_role(UserRole.ADMIN)
require_seller_or_admin = require_role(UserRole.SELLER, UserRole.ADMIN)
require_buyer_or_admin = require_role(UserRole.BUYER, UserRole.ADMIN)
