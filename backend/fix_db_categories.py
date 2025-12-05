from pymongo import MongoClient
import os

# Connect to DB
client = MongoClient("mongodb://localhost:27018")
db = client["blr_geo_events"]
collection = db["events_clean"]

garbage_category = "All?ref=cityhome_viewall"
target_category = "Entertainment" # Default fallback

# Count how many
count = collection.count_documents({"category": garbage_category})
print(f"Found {count} events with garbage category: '{garbage_category}'")

if count > 0:
    # Update them
    result = collection.update_many(
        {"category": garbage_category},
        {"$set": {"category": target_category}}
    )
    print(f"✅ Updated {result.modified_count} events to '{target_category}'")
else:
    print("No events found with that category. Checking for partial matches...")
    # Check for regex content just in case
    cursor = collection.find({"category": {"$regex": "ref="}})
    fixed = 0
    for doc in cursor:
        print(f"Fixing {doc.get('title')} - Category: {doc.get('category')}")
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"category": target_category}}
        )
        fixed += 1
    print(f"✅ Fixed {fixed} partial matches.")

print("Database cleanup complete.")
