import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27018")
DB_NAME = os.getenv("MONGO_DB_NAME", "mp2_db")

async def check_categories():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["events_clean"]
    
    count = await collection.count_documents({})
    print(f"Total events: {count}")
    
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    
    results = await collection.aggregate(pipeline).to_list(length=100)
    
    print("Categories found:")
    for r in results:
        print(f"'{r['_id']}': {r['count']}")

if __name__ == "__main__":
    asyncio.run(check_categories())
