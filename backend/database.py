import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SHARD = os.getenv("SHARD", "a")  # Get shard ID from environment
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
DB_HOST = os.getenv("DB_HOST", f"mysql-master-{SHARD}")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")

# Database URLs
MASTER_DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
REPLICA_DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@mysql-replica-{SHARD}/{DB_NAME}?charset=utf8mb4"

# Create engine for master database
engine = create_async_engine(
    MASTER_DB_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create base class for declarative models
Base = declarative_base()

# Dependency to get database session
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
