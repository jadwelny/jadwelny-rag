from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, Settings 

base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)

@base_router.get("/")
def welcome(app_settings:Settings=Depends(get_settings) ):
    app_settings = get_settings()
    app_name = app_settings.app_name
    app_version = app_settings.app_version
    return {
        "app_name": app_name,
        "app_version": app_version
    }