from fastapi import APIRouter
from api import auth, events, vendors, recommendations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
