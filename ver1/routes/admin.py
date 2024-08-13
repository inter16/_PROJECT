from database.connection import Settings, Database
from routes.sensors import sensor_router
from models.sensors import Sensor
from models.users import User
from sn_list import sn_list
from fastapi import APIRouter, Depends, HTTPException, status, Body



admin_router = APIRouter(
    tags=["Admin"],
)

settings = Settings()

user_database = Database(User)
sensor_database = Database(Sensor)


@admin_router.get("/reset")
async def admin_reset():
    await settings.reset_database()
    await settings.initialize_database()
    for sn in sn_list:
        new_sensor = Sensor(
            SN=sn,
            hist=[]
        )
        await new_sensor.insert_one(new_sensor)
    return {
        "message":"hard reset complete"
    }

@admin_router.get("/sensors")
async def admin_sensors():
    sensors=await sensor_database.get_all()
    return sensors

@admin_router.get("/sensors/{SN}")
async def admin_sensor(SN:str):
    sensor=await Sensor.find_one(Sensor.SN==SN)
    if not sensor:
        return {
            "message":"Invaild SN"
        }
    return sensor

@admin_router.get("/users")
async def admin_users():
    users=await user_database.get_all()
    return users

@admin_router.get("/users/{id}")
async def admin_user(id:str):
    user=await User.find_one(User.id==id)
    if not user:
        return {
            "message":"Invaild id"
        }
    return user