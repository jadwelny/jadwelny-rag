from fastapi import FastAPI
from routers import base, data
from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI() 

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client = app.mongodb_client[settings.MONGO_DB_NAME]

@ app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(base.base_router)
app.include_router(data.data_router)