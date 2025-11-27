from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId

from database import get_database
from models import Event, Vendor
from api.deps import get_current_vendor

router = APIRouter()

import logging

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[Event])
async def get_recommendations(
    current_vendor: Vendor = Depends(get_current_vendor),
    db = Depends(get_database)
):
    # 1. Get Vendor Preferences
    if not current_vendor.location:
        logger.warning(f"Vendor {current_vendor.email} has no location set.")
        raise HTTPException(status_code=400, detail="Vendor location not set")
        
    logger.info(f"Vendor Location: {current_vendor.location}")
    logger.info(f"Radius: {current_vendor.travel_radius_km} km")

    # 2. Simple Proximity-based Recommendation (MongoDB $near)
    radius_meters = current_vendor.travel_radius_km * 1000
    
    query = {
        "location": {
            "$near": {
                "$geometry": current_vendor.location,
                "$maxDistance": radius_meters
            }
        }
    }
    
    cursor = db.events_clean.find(query).limit(20)
    events = await cursor.to_list(length=20)
    
    logger.info(f"Geospatial query found {len(events)} events.")
    
    # FALLBACK: If no events found near vendor, return latest events
    # This ensures the panel is never empty during demo/testing
    if not events:
        logger.info("No events found nearby. Falling back to latest events.")
        cursor = db.events_clean.find().sort("start_time", 1).limit(10)
        events = await cursor.to_list(length=10)
    
    # 3. Content-Based Filtering (ML Re-ranking)
    from ml.engine import MLEngine
    
    # In a real app, the model would be pre-trained and loaded.
    # Here, we train on-the-fly with the fetched candidates for demonstration.
    ml_engine = MLEngine()
    
    # Convert MongoDB objects to dicts for the engine
    candidate_events = [event for event in events]
    
    # Train on these candidates to build the TF-IDF matrix
    ml_engine.train(candidate_events)
    
    # Prepare vendor profile for prediction
    vendor_profile = {
        "business_type": current_vendor.category or "General",
        "preferred_zones": current_vendor.interests or []
    }
    
    # Predict/Rank
    ranked_events = ml_engine.predict(vendor_profile, candidate_events)
    
    logger.info(f"ML Engine ranked {len(ranked_events)} events.")
    
    return [Event(**event) for event in ranked_events]
