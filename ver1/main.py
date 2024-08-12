import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from database.connection import Settings, Database
from routes.sensors import sensor_router
from routes.users import user_router

from models.sensors import Sensor
from sn_list import sn_list

app = FastAPI()

settings = Settings()



app.include_router(user_router, prefix="/user")
app.include_router(sensor_router, prefix="/sensor")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()
    sensor_db = Database(Sensor)
    for sn in sn_list:
        sensor_exist = await Sensor.find_one(Sensor.SN==sn)
        if not sensor_exist:
            new_sensor = Sensor(
                SN=sn,
                hist=[]
            )
            await sensor_db.save(new_sensor)


@app.get("/")
async def home() -> dict:
    return {
        "Message" : "hi"
    }


if __name__ == '__main__':
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("main:app", host="203.236.8.208", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
