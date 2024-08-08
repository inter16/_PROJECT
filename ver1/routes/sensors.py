from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status, Body
from auth.authenticate import authenticate

from models.users import User, UpdateUser
from models.sensors import Sensor, UpdateSensor, TestSensor

sensor_router = APIRouter(
    tags=["Sensor"],
)

user_database = Database(User)
sensor_database = Database(Sensor)


@sensor_router.post("/add")
async def add_test(SN:int= Body(..., embed=True)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == SN)
    if sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sensor exists already."
        )
    new_sensor=Sensor(SN=SN)
    await sensor_database.save(new_sensor)
    return {
        "message": "Sensor created successfully"
    }


@sensor_router.get("/")
async def load_all_sensors(id: str = Depends(authenticate)) -> dict:
    user=await User.find_one(User.id == id)
    return {
        "Sensors" : user.sensors
    }

@sensor_router.patch("/reg")
async def reg_sensor(sens:TestSensor) -> dict:
    user_exist=await User.find_one(User.id==sens.user)
    sensor_exist = await Sensor.find_one(Sensor.SN==sens.SN)
    if not user_exist:
        return {
            "message":"not exist user"
        }
    if not sensor_exist:
        return {
            "message":"not exist user"
        }
    if sensor_exist.user:
        if sensor_exist.user == sens.user:
            return {
                "message":"already registered"
            }
        already_user=await User.find_one(User.id==sensor_exist.user)
        await already_user.update({"$pull": {"sensors": sens.SN}})
    await sensor_exist.update({"$set": {"user": sens.user}})
    await user_exist.update({"$push": {"sensors": sens.SN}})
    return {
        "message" : "successful",
        "sens" : sensor_exist,
        "user" : user_exist
    }


@sensor_router.patch("/register", status_code=status.HTTP_201_CREATED)
async def register_sensor(SN:int= Body(..., embed=True), id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    # if sensor_exist.user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_NOT_FOUND,
    #         detail="Sensor already registered"
    #     )
    us=UpdateSensor(user=id)
    await sensor_database.update(sensor_exist.id, us)
    
    exuser=await User.find_one(User.id==id)
    exuser.sensors.append(SN)
    es=exuser.sensors
    uub=UpdateUser(sensors=es)
    await user_database.update(id,uub)

    return {
        "message" : "Sensor registration successful",
        "es" : es
        
    }

### yet

@sensor_router.post("/activate")
async def activate_sensor(SN:int, activate:bool, id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if activate:
        return {
            "message" : "Activate detector"
        }
    return {
        "message" : "Deactivate detector"
    }


@sensor_router.post("/speaker")
async def activate_speaker(SN:str, activate:bool, id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if activate:
        return {
            "message" : "Activate speaker"
        }
    return {
        "message" : "Deactivate speaker"
    }
