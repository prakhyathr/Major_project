from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from pydantic import BaseModel, EmailStr

from database import get_database
from models import Vendor
from core.security import create_access_token, get_password_hash, verify_password

router = APIRouter()

class VendorRegister(BaseModel):
    email: EmailStr
    password: str
    business_name: str
    category: str
    is_vendor: bool = True # Legacy field compatibility

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_database)
) -> Any:
    # Query vendor by email
    vendor_data = await db.vendors.find_one({"email": form_data.username})
    
    if not vendor_data or not verify_password(form_data.password, vendor_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=str(vendor_data["_id"]))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(
    vendor_in: VendorRegister,
    db = Depends(get_database)
) -> Any:
    # Check existing
    existing_vendor = await db.vendors.find_one({"email": vendor_in.email})
    if existing_vendor:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    new_vendor = Vendor(
        email=vendor_in.email,
        hashed_password=get_password_hash(vendor_in.password),
        business_name=vendor_in.business_name,
        category=vendor_in.category,
        location={"type": "Point", "coordinates": [77.5946, 12.9716]} # Default Bengaluru Center
    )
    
    # Insert into MongoDB
    result = await db.vendors.insert_one(new_vendor.dict(by_alias=True, exclude={"id"}))
    
    created_vendor = await db.vendors.find_one({"_id": result.inserted_id})
    return Vendor(**created_vendor)
