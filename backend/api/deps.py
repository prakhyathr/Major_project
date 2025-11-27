from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from bson import ObjectId

from core.config import settings
from database import get_database
from models import Vendor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_vendor(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_database)
) -> Vendor:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    vendor = await db.vendors.find_one({"_id": ObjectId(token_data)})
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
        
    return Vendor(**vendor)
