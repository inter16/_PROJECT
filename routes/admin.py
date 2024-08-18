from database.connection import Settings
from models.sensors import Sensor
from models.users import User
from fastapi import APIRouter, Depends, HTTPException, status, Body
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from data import testdata

admin_router = APIRouter(
    tags=["Admin"],
)

settings = Settings()




@admin_router.get("/reset")
async def admin_reset():
    await settings.reset_database()
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    return {
        "message":"hard reset complete",
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

# from beanie import init_beanie
# @admin_router.get("/set")
# async def admin_get_us():
#     client = AsyncIOMotorClient(settings.DATABASE_URL)
#     class UU(User):
#         class Collection:
#             name="kkk"
#     await init_beanie(database=client.UserDB, document_models=[UU])
#     d=UU(
#         id='hjg',
#         password='dfg',
#         sensors=[]
#     )
#     await d.insert()
#     return {"message":"adfs"}



@admin_router.get("/sss")
async def admins():
    nt=datetime.now()
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    nt1=datetime.now()
    # testcol=client.testdb.testcol
    ntlist=[{"_id": nt,"n":1},{"_id": nt1,"n":2}]
    # await client.testdb.testcol.insert_one({"current_time": nt})
    await client.testdb.testcol.insert_many(ntlist)
    # a=await client.testdb.testcol.find({}, {"_id": 0}).to_list(None)
    a=await client.testdb.testcol.find({}).to_list(None)
    # a=await client.testdb.testcol.find_one()
    return {"messsage":a}

# @detector_router.patch("/vision/{sn}")
# async def detect_vision(sn:str):
#     client=AsyncIOMotorClient(settings.DATABASE_URL)
#     snlogdb=client.SensorLogDB[f'sensor_{sn}']
#     latest=await snlogdb.find().sort({_id: -1}).limit(1)
#     if latest['id']



@admin_router.get("/test/init")
async def test_init():
    test_user1=User(
        id="01066666666",
        password="$2b$12$rZxgWm9zeOzFOqUyzVHJA.sRZOudZ1Fx/3WZLL9y/4A0vbhZpg8a6",
        name="test acount 1",
        sensors=["111111111111","222222222222"],
        loc="11"
    )
    test_user2=User(
        id="01077777777",
        password="$2b$12$rZxgWm9zeOzFOqUyzVHJA.sRZOudZ1Fx/3WZLL9y/4A0vbhZpg8a6",
        name="test acount 2",
        sensors=["333333333333","444444444444"],
        loc="11"
    )
    test_sensor1=Sensor(
        id="111111111111",
        user="01066666666",
        name="test sensor 1"
    )
    test_sensor2=Sensor(
        id="222222222222",
        user="01066666666",
        name="test sensor 2"
    )
    test_sensor3=Sensor(
        id="333333333333",
        user="01077777777",
        name="test sensor 3"
    )
    test_sensor4=Sensor(
        id="444444444444",
        user="01077777777",
        name="test sensor 4"
    )
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    # await client.UserDB.user_01066666666_log.insert_many({"date": nt})
    # await client.UserDB.user_01077777777_log.insert_many({"date": nt})
    # log1=[
    #     {
    #         "date":datetime.fromisoformat("2024-08-17T16:20:54.907000"),
    #     }
    # ]
    # a=await testcol.find({}, {"_id": 0}).to_list(None)

    await test_user1.insert()
    await test_user2.insert()
    await test_sensor1.insert()
    await test_sensor2.insert()
    await test_sensor3.insert()
    await test_sensor4.insert()
    await client.UserLogDB.user_01066666666.insert_many(testdata.log1)

    return {
        "message" : "test initialize"
    }
    

# @admin_router.post("/test/log")
# async def log_test():
