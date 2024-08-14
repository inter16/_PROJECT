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
        # await new_sensor.insert_one(new_sensor)
        await new_sensor.create()
    return {
        "message":"hard reset complete"
    }

@admin_router.get("/sensor")
async def admin_sensors():
    sensors=await sensor_database.get_all()
    return sensors

@admin_router.get("/sensor/{SN}")
async def admin_sensor(SN:str):
    sensor=await Sensor.find_one(Sensor.SN==SN)
    if not sensor:
        return {
            "message":"Invaild SN"
        }
    return sensor

@admin_router.get("/sensor_registered")
async def admin_registered_sensors():
    sensors=await Sensor.find_one(Sensor.user != None)
    return sensors

@admin_router.get("/user")
async def admin_users():
    users=await user_database.get_all()
    return users

@admin_router.get("/user/{id}")
async def admin_user(id:str):
    user=await User.find_one(User.id==id)
    if not user:
        return {
            "message":"Invaild id"
        }
    return user

@admin_router.get("/test/init")
async def test_init():
    test_user=User(
        id="01077777777",
        name="테스트계정",
        sensor=["111111111111","111111111112"],
        loc="11"
    )
    test_sensor1=Sensor(
        SN="111111111111",
        user="01077777777",
        name="테스트양봉1",
        hist=[]
    )
    test_sensor2=Sensor(
        SN="111111111112",
        user="01077777777",
        name="테스트양봉1",
        hist=[]
    )
    # await test_user.insert_one()
    # await test_sensor1.insert_one()
    # await test_sensor2.insert_one()
    userdb=Database(User)
    sensordb=Database(Sensor)

# @admin_router.post("/test/log")
# async def log_test():
