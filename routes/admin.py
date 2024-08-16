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
    sensors=await Sensor.find(Sensor.user != None).to_list()
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


@admin_router.get("/test/init")
async def test_init():
    test_user1=User(
        id="01066666666",
        password="thisishashedobject1",
        name="테스트계정1",
        sensors=["111111111111","222222222222"],
        loc="11"
    )
    test_user2=User(
        id="01077777777",
        password="thisishashedobject2",
        name="테스트계정2",
        sensors=["333333333333","444444444444"],
        loc="11"
    )
    test_sensor1=Sensor(
        id="111111111111",
        user="01066666666",
        name="테스트양봉1",
    )
    test_sensor2=Sensor(
        id="222222222222",
        user="01066666666",
        name="테스트양봉2",
    )
    test_sensor3=Sensor(
        id="333333333333",
        user="01077777777",
        name="테스트양봉3",
    )
    test_sensor4=Sensor(
        id="444444444444",
        user="01077777777",
        name="테스트양봉4",
    )
    await test_user1.insert()
    await test_user2.insert()
    await test_sensor1.insert()
    await test_sensor2.insert()
    await test_sensor3.insert()
    await test_sensor4.insert()

    return {
        "message" : "test initialize"
    }
    

# @admin_router.post("/test/log")
# async def log_test():
