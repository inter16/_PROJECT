import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict

from motor.motor_asyncio import AsyncIOMotorClient


from database.connection import Database
from fastapi import APIRouter, Depends, HTTPException, status, Body
from auth.authenticate import authenticate
from database.connection import Settings

from models.users import User, UpdateUser
from models.sensors import Sensor, RegisterSensor, SensorName
# from ai import detector

import asyncio
from typing import Dict

sensor_router = APIRouter(
    tags=["Sensor"],
)

settings = Settings()

user_database = Database(User)
sensor_database = Database(Sensor)


tasks={}


@sensor_router.get("/")
async def load_all_sensors(id: str = Depends(authenticate)) -> dict:
    user=await User.find_one(User.id == id)
    Sensors=user.sensors
    dic={}

    for s in Sensors:
        sens=await Sensor.find_one(Sensor.SN==s)
        dic[s]=sens.name
    return dic


#req:RegisterSensor
@sensor_router.patch("/register", status_code=status.HTTP_201_CREATED)
async def register_sensor(req:RegisterSensor, id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.id == req.SN)
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
    await sensor_exist.update({"$set": {"user": id,"name":req.name}})
    await User.find_one(User.id==id).update({"$push": {"sensors": req.SN}})
    

    return {
        "message" : "Sensor registration successful"
    }

@sensor_router.patch("/unregister")
async def unregister_sensor(SN:str= Body(..., embed=True), id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.id == SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if sensor_exist.user:
        if sensor_exist.user==id:
            user_exist=await User.find_one(User.id==id)
            await user_exist.update({"$pull": {"sensors": SN}})
            await sensor_exist.update({"$set": {"user": None, "ip":None, "name":None}})
            return {
                "message":"Sensor unregistration successful"
            }
        raise HTTPException(
            status_code=status.HTTP_401_NOT_FOUND,
            detail="Not your sensor"
        )
    raise HTTPException(
        status_code=status.HTTP_409_NOT_FOUND,
        detail="Sensor already unregistered"
    )



@sensor_router.post("/getip")
async def get_ip(SN:str= Body(..., embed=True), id: str = Depends(authenticate)) -> dict:
    sensor_exist=await Sensor.find_one(Sensor.id == SN)
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
    sensor_exist=await Sensor.find_one(Sensor.id == req.SN)
    if not sensor_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor does not exist."
        )
    if id == sensor_exist.user:
        await sensor_exist.update({"$set": {"name": req.name}})
        return {
            "message":"update sensor name successfully",
        }
    raise HTTPException(
        status_code=status.HTTP_401_NOT_FOUND,
        detail="Not your sensor"
    )

# ### yet

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
#         tasks[req.SN]=asyncio.create_task(detector.audio_stream(URL))
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
async def load_hist(SN:str= Body(..., embed=True), id: str = Depends(authenticate))->dict:
    sensor_exist=await Sensor.find_one(Sensor.id == SN)
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
    nt=datetime.now()
    one_year_ago_firstday = nt.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta(years=1)
    one_year_ago_monday=one_year_ago_firstday-timedelta(days=one_year_ago_firstday.weekday())

    client = AsyncIOMotorClient(settings.DATABASE_URL)

    data = client.SensorLogDB[f'SN_{SN}'].find({"_id": {"$gt": one_year_ago_monday.strftime("%Y/%m/%d/%H")}}).to_list(None)

    # per day
    daily_max = defaultdict(int)
    for entry in data:
        date = entry["_id"][:10]
        num = entry["num"]
        if num > daily_max[date]:
            daily_max[date] = num
    daily_max_dict=dict(daily_max)

    # per week
    weekly_sum = defaultdict(int)
    for date, num in daily_max.items():
        date_datetime = datetime.strptime(date, "%Y/%m/%d")
        monday_datetime = date_datetime - timedelta(days=date_datetime.weekday())
        monday = monday_datetime.strftime("%Y/%m/%d")
        weekly_sum[monday] += num
    weekly_sum_dict = dict(weekly_sum)


    # for target month
    target_month=nt.strftime("%Y/%m")
    first_day_of_month = datetime.strptime(target_month, "%Y/%m")
    first_monday = first_day_of_month - timedelta(days=first_day_of_month.weekday())
    last_day_of_month = first_day_of_month + relativedelta(months=1) - timedelta(days=1)
    last_monday=last_day_of_month - timedelta(days=last_day_of_month.weekday())
    target={k: v for k, v in weekly_sum.items() if datetime.strptime(first_monday, "%Y/%m/%d") <= k <= datetime.strptime(last_monday, "%Y/%m/%d")}


    # for year per month
    monthly_sum = defaultdict(int)
    for date, num in daily_max.items():
        month_str = date[:7]
        monthly_sum[month_str] += num
    monthly_sum_dict = dict(monthly_sum)
    





    

# ############################# sensor to server


# @sensor_router.patch("/onair")
# async def sensor_onair(req:SensorIP)->dict:
#     sensor_exist=await Sensor.find_one(Sensor.SN == req.SN)
#     if not sensor_exist:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Sensor does not exist."
#         )
#     await sensor_exist.update({"$set": {"ip": req.ip}})
#     return {
#         "message":"Sensor OnAir"
#     }






