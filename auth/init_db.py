import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models import Base
from database import DATABASE_URL

async def init_db():
    """Initialize the database with all tables."""
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        print("Database initialized successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db()) 