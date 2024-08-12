from beanie import Document
from typing import Optional, List, Tuple, Any
from pydantic import BaseModel
from datetime import date


class Sensor(Document):
    SN: int
    ip: Optional[str]
    user: Optional[str]
    name: Optional[str]
    hist:List[List[Any]]

    class Collection:
        name = "sensors"


class UpdateSensor(BaseModel):
    SN: Optional[int]
    ip: Optional[str]
    user: Optional[str]
    name: Optional[str]

class SensorName(BaseModel):
    SN: int
    name: str   

class RegisterSensor(BaseModel):
    SN: int
    name: str   


class SensorLog(BaseModel):
    SN:int
    log:List[Any]

class TestSensor(BaseModel):
    SN: int
    user: str   


class SensorIP(BaseModel):
    SN:int
    ip:str


class Operate(BaseModel):
    SN: int
    activate: bool   