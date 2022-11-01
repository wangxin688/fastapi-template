from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from app.api.base import BaseModel


class AccessTokenBase(BaseModel):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AuthTokenBase(BaseModel):
    id: int
    target_user: EmailStr
    created_by: EmailStr
    is_active: bool
    expires_at: datetime
    description: str
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserUpdateRequest(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
