from fastapi import APIRouter

from app.api.api_v1.endpoints import cointrack


api_router = APIRouter()
api_router.include_router(cointrack.router, prefix="/coins", tags=["coins"])
