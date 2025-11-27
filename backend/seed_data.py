import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random

MONGO_URL = "mongodb://mongo:27017"
DB_NAME = "blr_geo_events"

# Bengaluru Zones & Coordinates
ZONES = {
    "Indiranagar": [77.6412, 12.9719],
    "Koramangala": [77.6271, 12.9352],
    "Whitefield": [77.7499, 12.9698],
    "Electronic City": [77.6687, 12.8452],
    "Malleshwaram": [77.5703, 13.0031],
    "Jayanagar": [77.5808, 12.9250]
}

CATEGORIES = ["Music", "Tech", "Food", "Art", "Business"]

async def seed_data():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("Clearing existing data...")
    await db.events_clean.delete_many({})
    await db.vendors.delete_many({})
    
    events = []
    print("Generating events...")
    for i in range(50):
        zone_name = random.choice(list(ZONES.keys()))
        base_coords = ZONES[zone_name]
        
        # Add random jitter to coordinates
        lng = base_coords[0] + random.uniform(-0.02, 0.02)
        lat = base_coords[1] + random.uniform(-0.02, 0.02)
        
        event = {
            "title": f"{random.choice(CATEGORIES)} Event in {zone_name} #{i+1}",
            "description": "A great event you should not miss!",
            "source_url": "https://example.com",
            "start_time": datetime.utcnow() + timedelta(days=random.randint(1, 30)),
            "end_time": datetime.utcnow() + timedelta(days=random.randint(1, 30), hours=4),
            "location": {
                "type": "Point",
                "coordinates": [lng, lat]
            },
            "main_zone": zone_name,
            "category": random.choice(CATEGORIES) # Adding category field for filtering
        }
        events.append(event)
    
    await db.events_clean.insert_many(events)
    print(f"Inserted {len(events)} events.")
    
    # Create indexes
    await db.events_clean.create_index([("location", "2dsphere")])
    await db.events_clean.create_index("main_zone")
    print("Indexes created.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
