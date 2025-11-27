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
