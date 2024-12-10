from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class AuthUser(Base):
    """Model for authentication user data."""
    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Define relationship to BlacklistedToken
    tokens = relationship("BlacklistedToken", back_populates="user")


class BlacklistedToken(Base):
    """Model for storing blacklisted JWT tokens."""
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_users.id"))
    expires_at = Column(DateTime(timezone=True))
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Define relationship to AuthUser
    user = relationship("AuthUser", back_populates="tokens") 