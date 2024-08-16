from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId

from models.sensors import Sensor
from models.users import User


from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, BaseModel

import motor.motor_asyncio

from pymongo import MongoClient
import os

from database.sn_list import sn_list

from models.users import User
from models.sensors import Sensor

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)

        await init_beanie(database=client.UserDB, document_models=[User])

        await init_beanie(database=client.SensorDB, document_models=[Sensor])

        for sn in sn_list:
            sensor_exist=await Sensor.find_one(Sensor.id==sn)
            if not sensor_exist:
                new_sensor = Sensor(SN=sn)
                await new_sensor.insert()

    async def reset_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await client.drop_database("UserDB")
        await client.drop_database("SensorDB")
        await init_beanie(database=client.UserDB, document_models=[User])
        await init_beanie(database=client.SensorDB, document_models=[Sensor])
        for sn in sn_list:
            new_sensor = Sensor(id=sn)
            await new_sensor.insert()
        

    class Config:
        env_file = ".env"

    
        


class Database:
    def __init__(self, model):
        self.model = model

#     async def save(self, document):
#         await document.create()
#         return

    async def get(self, id: PydanticObjectId):
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self):
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel):
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

#     async def delete(self, id: PydanticObjectId):
#         doc = await self.get(id)
#         if not doc:
#             return False
#         await doc.delete()
#         return True
    
 