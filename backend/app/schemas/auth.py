"""
Auth schemas — signup, login, and token responses.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.constants import UserRole
from app.utils.validators import validate_password_strength, validate_phone_number


class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Ramesh Kumar"])
    email: EmailStr = Field(..., examples=["ramesh@example.com"])
    password: str = Field(..., min_length=8, examples=["Str0ng@Pass!"])
    phone: str | None = Field(default=None, examples=["9876543210"])
    role: UserRole = Field(default=UserRole.BUYER)

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        return validate_password_strength(v)

    @field_validator("phone")
    @classmethod
    def valid_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return validate_phone_number(v)


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["ramesh@example.com"])
    password: str = Field(..., examples=["Str0ng@Pass!"])


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
    trust_score: int
    is_active: bool
    is_verified: bool
    phone: str | None = None
    avatar_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def strong_new_password(cls, v: str) -> str:
        return validate_password_strength(v)

