import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27018")
DB_NAME = os.getenv("MONGO_DB_NAME", "blr_geo_events")

async def check_db():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    pipeline = [
        {"$group": {"_id": "$source", "count": {"$sum": 1}}}
    ]
    
    print("--- Event Counts by Source ---")
    async for doc in db.events_clean.aggregate(pipeline):
        print(f"{doc['_id']}: {doc['count']}")
        
    client.close()

if __name__ == "__main__":
    asyncio.run(check_db())
