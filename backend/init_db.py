import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from database import MASTER_DB_URL
from sqlalchemy.sql import text
from models import Base

async def init_db():
    """Initialize the database for this shard"""
    print(f"Initializing database with URL: {MASTER_DB_URL}")
    engine = create_async_engine(MASTER_DB_URL, echo=True)
    
    async with engine.begin() as conn:
        # Test connection
        print("Testing database connection...")
        result = await conn.execute(text("SELECT 1"))
        print("Connection test result:", result.scalar())
        
        # Create all tables
        print("Creating tables...")
        print("Registered models:", Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")
        
        # List created tables
        result = await conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
        print("Created tables:", tables)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db()) 