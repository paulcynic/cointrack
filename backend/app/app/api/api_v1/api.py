from fastapi import APIRouter

from app.api.api_v1.endpoints import cointrack, auth


api_router = APIRouter()
api_router.include_router(cointrack.router, prefix="/coins", tags=["coins"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
