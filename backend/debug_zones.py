import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27018")
DB_NAME = os.getenv("MONGO_DB_NAME", "mp2_db")

async def analyze_zones():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["events_clean"]
    
    # Check total count
    count = await collection.count_documents({})
    print(f"Total events: {count}")

    # Dump a sample event
    sample = await collection.find_one({})
    print("Sample Event:", sample)
    
    pipeline = [
        {"$group": {"_id": "$main_zone", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    
    results = await collection.aggregate(pipeline).to_list(length=20)
    
    print("Top 20 Main Zones in DB:")
    for r in results:
        print(f"'{r['_id']}': {r['count']}")

if __name__ == "__main__":
    asyncio.run(analyze_zones())
