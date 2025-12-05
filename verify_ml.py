from backend.ml.engine import MLEngine
from backend.models import Event
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Mock Database Connection
async def get_events():
    mongo_url = "mongodb://localhost:27018"
    client = AsyncIOMotorClient(mongo_url)
    db = client["blr_geo_events"]
    cursor = db.events_clean.find({})
    events = await cursor.to_list(length=1000)
    return events

async def test_model():
    print("Fetching events from DB...")
    events = await get_events()
    print(f"Loaded {len(events)} events.")
    
    # Initialize Engine
    engine = MLEngine()
    engine.train(events)
    
    # Test Profiles
    profiles = [
        {"business_name": "DJ Snake", "category": "Entertainment", "interests": ["Music", "Party", "Concert"]},
        {"business_name": "Tech Startup", "category": "Technology", "interests": ["Business", "Workshop", "Startup"]},
        {"business_name": "Art Gallery", "category": "Art", "interests": ["Exhibition", "Painting", "Culture"]},
        {"business_name": "Food Truck", "category": "Food", "interests": ["Food", "Festival", "Market"]}
    ]

    total_score = 0
    count = 0

    print("\n--- Model Confidence Evaluation ---")
    for profile in profiles:
        recommendations = engine.predict(profile, events, top_n=5)
        if recommendations:
            # Calculate average score for this profile's top 5
            avg_rec_score = sum(e.get('ml_score', 0) for e in recommendations) / len(recommendations)
            print(f"Profile: {profile['category']:<15} | Avg Similarity: {avg_rec_score:.4f}")
            total_score += avg_rec_score
            count += 1
    
    if count > 0:
        overall_confidence = (total_score / count) * 100
        print(f"\n✅ Overall Model Confidence Score: {overall_confidence:.2f}%")
        with open("ml_score.txt", "w") as f:
            f.write(f"{overall_confidence:.2f}")

if __name__ == "__main__":
    asyncio.run(test_model())
