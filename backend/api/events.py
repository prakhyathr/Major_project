from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from bson import ObjectId

from database import get_database
from models import Event

router = APIRouter()

@router.get("/", response_model=List[Event])
async def read_events(
    skip: int = 0, 
    limit: int = 1000, 
    zone: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: Optional[float] = 10.0,
    db = Depends(get_database)
):
    query = {}
    
    if zone:
        query["main_zone"] = zone
        
    if lat is not None and lng is not None:
        query["location"] = {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "$maxDistance": radius_km * 1000 # Convert km to meters
            }
        }
        
    cursor = db.events_clean.find(query).skip(skip).limit(limit)
    events = await cursor.to_list(length=limit)
    return [Event(**event) for event in events]

@router.post("/", response_model=Event)
async def create_event(
    event: Event, 
    db = Depends(get_database)
):
    # Ensure location is GeoJSON
    if not event.location or event.location.get("type") != "Point":
        raise HTTPException(status_code=400, detail="Invalid GeoJSON location")
        
    result = await db.events_clean.insert_one(event.dict(by_alias=True, exclude={"id"}))
    created_event = await db.events_clean.find_one({"_id": result.inserted_id})
    return Event(**created_event)

@router.get("/{event_id}", response_model=Event)
async def read_event(
    event_id: str, 
    db = Depends(get_database)
):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    event = await db.events_clean.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event(**event)
