from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def get_database():
    return db.db

async def init_db():
    db.client = AsyncIOMotorClient(settings.MONGO_URL)
    db.db = db.client[settings.MONGO_DB_NAME]
    
    # Create indexes
    await db.db.vendors.create_index("email", unique=True)
    await db.db.events_clean.create_index([("location", "2dsphere")])
    await db.db.events_clean.create_index("main_zone")
    
    print("MongoDB Initialized")

async def close_db():
    db.client.close()
