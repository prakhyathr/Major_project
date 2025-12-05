from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import Optional, List, Any, Annotated
from datetime import datetime
from bson import ObjectId

# Pydantic v2 compatible ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Vendor(MongoBaseModel):
    email: EmailStr
    hashed_password: str
    business_name: Optional[str] = None
    category: Optional[str] = None
    interests: List[str] = []
    saved_events: List[str] = [] # List of Event IDs
    travel_radius_km: float = 10.0
    location: Optional[dict] = None # GeoJSON Point
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Event(MongoBaseModel):
    title: str
    description: Optional[str] = None
    source_url: str
    start_time: datetime
    end_time: Optional[datetime] = None
    location: dict # GeoJSON Point
    main_zone: Optional[str] = None
    category: Optional[str] = None
    embedding: Optional[List[float]] = None # For ML
    cluster_id: Optional[int] = None

class Interaction(MongoBaseModel):
    vendor_id: str
    event_id: str
    action: str # 'view', 'bookmark', 'click'
    timestamp: datetime = Field(default_factory=datetime.utcnow)
