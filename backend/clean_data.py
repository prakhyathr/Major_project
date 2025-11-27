import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Config
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "blr_geo_events")

async def clean_data():
    print("Cleaning up legacy/seed data...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Delete events that don't have a 'source' field (legacy seed data)
    # OR events where source is 'seed' (if we had set that)
    # Since our new scrapers set 'source', we can delete anything without it.
    
    result = await db.events_clean.delete_many({
        "$or": [
            {"source": {"$exists": False}},
            {"source": "seed"} # If we explicitly named it seed
        ]
    })
    
    print(f"Deleted {result.deleted_count} legacy events.")
    
    # Verify remaining
    count = await db.events_clean.count_documents({})
    print(f"Remaining events in DB: {count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(clean_data())
