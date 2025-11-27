import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "blr_geo_events")

async def analyze_zones():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    pipeline = [
        {"$group": {"_id": "$main_zone", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    
    print("--- Event Counts by Zone ---")
    async for doc in db.events_clean.aggregate(pipeline):
        print(f"{doc['_id']}: {doc['count']}")
        
    client.close()

if __name__ == "__main__":
    asyncio.run(analyze_zones())
