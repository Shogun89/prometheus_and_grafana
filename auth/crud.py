from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models import AuthUser, BlacklistedToken
from schemas import AuthUserCreate, AuthUserUpdate
from password import get_password_hash

# User Management
async def get_user_by_email(db: AsyncSession, email: str):
    """Get a user by email address."""
    result = await db.execute(
        select(AuthUser).filter(AuthUser.email == email)
    )
    return result.scalar_one_or_none()

async def get_user(db: AsyncSession, user_id: int):
    """Get a user by ID."""
    result = await db.execute(
        select(AuthUser).filter(AuthUser.id == user_id)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: AuthUserCreate):
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = AuthUser(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise

# Authentication Management
async def update_last_login(db: AsyncSession, user_id: int):
    """Update user's last login timestamp."""
    db_user = await get_user(db, user_id)
    if db_user:
        db_user.last_login = datetime.utcnow()
        await db.commit()

async def blacklist_token(db: AsyncSession, token: str, expires_at: datetime, user_id: int):
    """Add a token to the blacklist."""
    db_token = BlacklistedToken(
        token=token,
        expires_at=expires_at,
        user_id=user_id
    )
    db.add(db_token)
    await db.commit()

async def is_token_blacklisted(db: AsyncSession, token: str) -> bool:
    """Check if a token is blacklisted."""
    result = await db.execute(
        select(BlacklistedToken).filter(BlacklistedToken.token == token)
    )
    return result.scalar_one_or_none() is not None

# Password Management
async def update_password(db: AsyncSession, user: AuthUser, new_password: str):
    """Update user's password."""
    user.hashed_password = get_password_hash(new_password)
    await db.commit() 