from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from database.connection import Settings
from models.ai import VisionResult
from datetime import datetime

detector_router = APIRouter(
    tags=["Detector"],
)

settings = Settings()


# @detector_router.get("/")
# async def helllo



# @detector_router.post("/audio/{sn}")
# async def detect_sound(sn:str):





@detector_router.patch("/vision")
async def detect_vision(req:VisionResult):
    nt=datetime.now().replace(minute=0, second=0, microsecond=0)
    client=AsyncIOMotorClient(settings.DATABASE_URL)
    snlogdb=client.SensorLogDB[f'SN_{req.SN}']
    latest=await snlogdb.find().sort({_id: -1}).limit(1)
    if not latest:
        await snlogdb.insert_one({"_id":nt, "num":req.num})
    elif latest['_id']<nt:
        await snlogdb.insert_one({"_id":nt, "num":req.num})
    else:
        if latest['num']<req.num:
            await snlogdb.update_one({"_id":nt}, {"$set": {"num":req.num}})
    return




# @detector_router.post("/{sn}/")

