"""
Auth Service.
Handles signup, login, password changes, and token blacklisting.
"""

from datetime import timedelta
from typing import Dict, Any
from uuid import UUID

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    decode_token,
)
from app.models.user import User
from app.models.seller import SellerProfile
from app.models.buyer import BuyerProfile
from app.repository.user_repository import UserRepository
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.utils.constants import UserRole
from app.utils.exceptions import (
    BadRequestException,
    ConflictException,
    CredentialsException,
    AccountSuspendedException,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def signup(self, req: SignupRequest) -> User:
        # Check if email exists
        existing = await self.user_repo.get_by_email(req.email)
        if existing:
            raise ConflictException(detail="Email is already registered.")

        # Create user
        hashed_pwd = hash_password(req.password)
        user_data = {
            "name": req.name,
            "email": req.email,
            "hashed_password": hashed_pwd,
            "phone": req.phone,
            "role": req.role.value,
        }
        user = await self.user_repo.create(user_data)

        # Create corresponding profile
        if req.role == UserRole.SELLER:
            from app.repository.seller_repository import SellerRepository
            seller_repo = SellerRepository(self.db)
            await seller_repo.create({"user_id": user.id})
        elif req.role == UserRole.BUYER:
            from app.repository.buyer_repository import BuyerRepository
            buyer_repo = BuyerRepository(self.db)
            await buyer_repo.create({"user_id": user.id})

        return user

    async def login(self, req: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(req.email)
        
        if not user or not verify_password(req.password, user.hashed_password):
            raise CredentialsException(detail="Invalid email or password.")
            
        if not user.is_active:
            raise AccountSuspendedException()

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60, # 30 mins
        )
