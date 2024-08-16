from database.connection import Settings
from models.sensors import Sensor
from models.users import User
from fastapi import APIRouter, Depends, HTTPException, status, Body


admin_router = APIRouter(
    tags=["Admin"],
)

settings = Settings()


@admin_router.get("/reset")
async def admin_reset():
    await settings.reset_database()
    return {
        "message":"hard reset complete"
    }

@admin_router.get("/sensor")
async def admin_get_all_sensors():
    sensors=await Sensor.find_all().to_list()
    return sensors

@admin_router.get("/sensor/{SN}")
async def admin_get_one_sensor(SN:str):
    sensor=await Sensor.find_one(Sensor.id==SN)
    if not sensor:
        return {
            "message":"Invaild SN"
        }
    return sensor

@admin_router.get("/sensor_registered")
async def admin_get_registered_sensors():
    sensors=await Sensor.find_one(Sensor.user != None)
    return sensors

@admin_router.get("/user")
async def admin_get_all_users():
    users=await User.find_all().to_list()
    return users

@admin_router.get("/user/{id}")
async def admin_get_user(id:str):
    user=await User.find_one(User.id==id)
    if not user:
        return {
            "message":"Invaild id"
        }
    return user

# @admin_router.get("/test/init")
# async def test_init():
#     test_user=User(
#         id="01077777777",
#         name="테스트계정",
#         sensor=["111111111111","111111111112"],
#         loc="11"
#     )
#     test_sensor1=Sensor(
#         SN="111111111111",
#         user="01077777777",
#         name="테스트양봉1",
#         hist=[]
#     )
#     test_sensor2=Sensor(
#         SN="111111111112",
#         user="01077777777",
#         name="테스트양봉1",
#         hist=[]
#     )
    # await test_user.insert_one()
    # await test_sensor1.insert_one()
    # await test_sensor2.insert_one()
    # userdb=Database(User)
    # sensordb=Database(Sensor)

# @admin_router.post("/test/log")
# async def log_test():
