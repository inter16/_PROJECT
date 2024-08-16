import uvicorn
from fastapi import FastAPI


from database.connection import Settings
from routes.sensors import sensor_router
from routes.users import user_router
from routes.admin import admin_router

# from models.sensors import Sensor
# from sn_list import sn_list

from motor.motor_asyncio import AsyncIOMotorClient

from models.sensors import Sensor

app = FastAPI()

settings = Settings()



# client = AsyncIOMotorClient("mongodb+srv://admin:1234@sktproject.fsdw0.mongodb.net/")

# UserDB = client['UserDB']
# SensorDB = client['SensorDB']


app.include_router(user_router, prefix="/user")
app.include_router(sensor_router, prefix="/sensor")
app.include_router(admin_router, prefix="/admin")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

@app.get("/")
async def home():
    return {
        "Message" : "hi"
    }

# @app.get("/a")
# async def aaaae():
#     await settings.reset_database()
#     return {
#         "Message" : "suc"
#     }

# @app.get("/b")
# async def b():
#     # docs = await Sensor.find_one(Sensor.SN=='100000000000')
#     docs = await Sensor.find_all().to_list()
#     return docs




if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
