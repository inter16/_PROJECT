import requests
import datetime

from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status, Body
from auth.authenticate import authenticate

from models.users import User, UpdateUser
from models.sensors import Sensor, SensorIP, TestSensor, Operate, SensorName, SensorLog, RegisterSensor
from ai import detector

import asyncio
from typing import Dict

sensor_router = APIRouter(
    tags=["Sensor"],
)

user_database = Database(User)
sensor_database = Database(Sensor)


# tasks=Dict[int,asyncio.Task]={}


@sensor_router.get("/")
async def load_all_sensors(id: str = Depends(authenticate)) -> dict:
    user=await User.find_one(User.id == id)
    return {
        "Sensors" : user.sensors
    }



@sensor_router.patch("/register", status_code=status.HTTP_201_CREATED)
async def register_sensor(req:RegisterSensor, id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == req.SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if sensor_exist.user:
        if sensor_exist.user==id:
            raise HTTPException(
                status_code=status.HTTP_409_NOT_FOUND,
                detail="Sensor already registered"
            )
        already_user=await User.find_one(User.id==sensor_exist.user)
        await already_user.update({"$pull": {"sensors": req.SN}})
    await sensor_exist.update({"$set": {"user": id, "name":req.name}})
    await User.find_one(User.id==id).update({"$push": {"sensors": req.SN}})

    return {
        "message" : "Sensor registration successful",
    }



@sensor_router.post("/getip")
async def get_ip(SN:int= Body(..., embed=True), id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if id == sensor_exist.user:
        return {
            "message":"give sensor ip",
            "ip":sensor_exist.ip
        }
    raise HTTPException(
        status_code=status.HTTP_401_NOT_FOUND,
        detail="Not your sensor"
    )

@sensor_router.put("/name")
async def sensor_edit_name(req:SensorName, id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == req.SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if id == sensor_exist.user:
        await sensor_exist.update({"$set": {"name": req.name}})
        return {
            "message":"update sensor name successfully",
            "test":True
        }
    raise HTTPException(
        status_code=status.HTTP_401_NOT_FOUND,
        detail="Not your sensor"
    )

### yet

# @sensor_router.post("/activate")
# async def activate_sensor(req:Operate, id: str = Depends(authenticate)) -> dict:
#     sensor_exist=await Sensor.find_one(Sensor.SN == req.SN)
#     if not sensor_exist:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Sensor does not exist."
#         )
#     if sensor_exist.user != id:
#         raise HTTPException(
#             status_code=status.HTTP_401_NOT_FOUND,
#             detail="Not your sensor."
#         )
#     URL="httt://" + sensor_exist.ip + ":8000/"
#     response = requests.get(URL)
#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=status.HTTP_405_NOT_FOUND,
#             detail="Sensor not OnAir"
#         )
#     if req.activate:
#         if req.SN in tasks:
#             raise HTTPException(
#                 status_code=status.HTTP_403_NOT_FOUND,
#                 detail="Detector already activated"
#             )
#         await sensor_exist.update({"$push": {"hist": [datetime.datetime.now(),0]}})
#         # active detector
#         tasks[req.SN]=asyncio.create_task(detector)
#         return {
#             "message" : "Activate detector"
#         }
#     await sensor_exist.update({"$push": {"hist": [datetime.datetime.now(),1]}})
#     # deactive detector
#     return {
#         "message" : "Deactivate detector"
#     }


# @sensor_router.post("/speaker")
# async def activate_speaker(req:Operate, id: str = Depends(authenticate)) -> dict:
#     sensor_exist=await Sensor.find_one(Sensor.SN == req.SN)
#     if not sensor_exist:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Sensor does not exist."
#         )
#     if sensor_exist.user != id:
#         raise HTTPException(
#             status_code=status.HTTP_401_NOT_FOUND,
#             detail="Not your sensor."
#         )
#     if not sensor_exist.ip:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Sensor doesn't be activated"
#         )
#     URL="httt://" + sensor_exist.ip + ":8000/speaker"
#     params = {
#         "on":req.activate
#     }
#     response = requests.get(URL, params=params)
#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid"
#         )
#     if req.activate:
#         await sensor_exist.update({"$push": {"hist": [datetime.datetime.now(),6]}})
#         return {
#             "message" : "Activate speaker"
#         }
#     await sensor_exist.update({"$push": {"hist": [datetime.datetime.now(),7]}})
#     return {
#         "message" : "Deactivate speaker"
#     }


@sensor_router.post("/hist")
async def load_hist(SN:int= Body(..., embed=True), id: str = Depends(authenticate))->dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if id != sensor_exist.user:
        raise HTTPException(
            status_code=status.HTTP_401_NOT_FOUND,
            detail="Not your sensor"
        )
    return {
        "message" : "Load hist successfully",
        "hist":sensor_exist.hist
    }

    

############################# sensor to server


@sensor_router.patch("/onair")
async def sensor_onair(req:SensorIP)->dict:
    sensor_exist=await Sensor.find_one(Sensor.SN == req.SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    await sensor_exist.update({"$set": {"ip": req.ip}})
    return {
        "message":"Sensor OnAir"
    }






