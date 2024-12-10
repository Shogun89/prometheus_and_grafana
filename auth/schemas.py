from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for JWT token payload."""
    email: Optional[str] = None
    user_id: Optional[int] = None
    exp: Optional[datetime] = None

class AuthUserBase(BaseModel):
    """Base schema for authentication user."""
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False

class AuthUserCreate(AuthUserBase):
    """Schema for creating a new authentication user."""
    password: str

class AuthUserUpdate(BaseModel):
    """Schema for updating an authentication user."""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class AuthUser(AuthUserBase):
    """Schema for complete authentication user data."""
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr

class PasswordChange(BaseModel):
    """Schema for password change request."""
    current_password: str
    new_password: str 