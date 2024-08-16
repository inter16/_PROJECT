import uvicorn
from fastapi import FastAPI


from database.connection import Settings
from routes.sensors import sensor_router
from routes.users import user_router
from routes.admin import admin_router


from motor.motor_asyncio import AsyncIOMotorClient

from models.sensors import Sensor

app = FastAPI()

settings = Settings()



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


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
