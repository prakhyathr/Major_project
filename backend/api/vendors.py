from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId

from database import get_database
from models import Vendor
from api.deps import get_current_vendor

router = APIRouter()

class VendorUpdate(BaseModel):
    business_name: Optional[str] = None
    category: Optional[str] = None
    interests: Optional[List[str]] = None
    travel_radius_km: Optional[float] = None
    location: Optional[dict] = None

@router.get("/me", response_model=Vendor)
async def read_current_vendor(
    current_vendor: Vendor = Depends(get_current_vendor)
):
    return current_vendor

@router.put("/me", response_model=Vendor)
async def update_current_vendor(
    vendor_in: VendorUpdate,
    current_vendor: Vendor = Depends(get_current_vendor),
    db = Depends(get_database)
):
    update_data = vendor_in.dict(exclude_unset=True)
    
    if update_data:
        # Ensure ID is ObjectId
        vendor_id = ObjectId(current_vendor.id)
        
        await db.vendors.update_one(
            {"_id": vendor_id},
            {"$set": update_data}
        )
        
        # Fetch updated vendor
        updated_vendor = await db.vendors.find_one({"_id": vendor_id})
        return Vendor(**updated_vendor)
    
    return current_vendor

@router.post("/saved-events/{event_id}")
async def save_event(
    event_id: str,
    current_vendor: Vendor = Depends(get_current_vendor),
    db = Depends(get_database)
):
    vendor_id = ObjectId(current_vendor.id)
    
    # Add to set (addToSet prevents duplicates)
    await db.vendors.update_one(
        {"_id": vendor_id},
        {"$addToSet": {"saved_events": event_id}}
    )
    return {"status": "success", "message": "Event saved"}

@router.delete("/saved-events/{event_id}")
async def unsave_event(
    event_id: str,
    current_vendor: Vendor = Depends(get_current_vendor),
    db = Depends(get_database)
):
    vendor_id = ObjectId(current_vendor.id)
    
    # Remove from array
    await db.vendors.update_one(
        {"_id": vendor_id},
        {"$pull": {"saved_events": event_id}}
    )
    return {"status": "success", "message": "Event removed from saved"}

@router.get("/saved-events", response_model=List[dict])
async def get_saved_events(
    current_vendor: Vendor = Depends(get_current_vendor),
    db = Depends(get_database)
):
    if not current_vendor.saved_events:
        return []
        
    # Convert string IDs to ObjectIds if necessary, but events usually use string IDs in this system setup or need conversion.
    # Assuming IDs are stored as strings in saved_events.
    # Depending on how Event IDs are stored in DB, we might need ObjectId(e_id).
    # Let's try matching string IDs first as per the schema.
    
    # Actually, Event IDs in Mongo are ObjectIds.
    try:
        event_object_ids = [ObjectId(e_id) for e_id in current_vendor.saved_events]
    except Exception:
        return [] # Handle bad IDs gracefully
        
    events = await db.events_clean.find({"_id": {"$in": event_object_ids}}).to_list(length=100)
    
    # Convert _id to id string for response
    results = []
    for e in events:
        e['id'] = str(e['_id'])
        results.append(e)
        
    return results
