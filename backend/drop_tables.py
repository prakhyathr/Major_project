import asyncio
from sqlalchemy import text
from database import engine

async def drop_tables():
    async with engine.begin() as conn:
        print("Dropping indexes...")
        await conn.execute(text("DROP INDEX IF EXISTS idx_cluster_centroid;"))
        await conn.execute(text("DROP INDEX IF EXISTS idx_event_location;"))
        await conn.execute(text("DROP INDEX IF EXISTS idx_vendor_location;"))
        
        print("Dropping tables...")
        await conn.execute(text("DROP TABLE IF EXISTS vendor CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS event CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS cluster CASCADE;"))
        await conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
    print("Cleanup complete.")

if __name__ == "__main__":
    asyncio.run(drop_tables())
