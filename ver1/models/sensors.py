from beanie import Document
from typing import Optional, List, Tuple, Any
from pydantic import BaseModel
from datetime import date


class Sensor(Document):
    SN: str
    ip: Optional[str]
    user: Optional[str]
    name: Optional[str]
    hist:List[List[Any]]

    class Collection:
        name = "sensors"


class UpdateSensor(BaseModel):
    SN: Optional[str]
    ip: Optional[str]
    user: Optional[str]
    name: Optional[str]

class SensorName(BaseModel):
    SN: str
    name: str   

class RegisterSensor(BaseModel):
    SN: str
    name: str  


class SensorLog(BaseModel):
    SN:str
    log:List[Any]

class TestSensor(BaseModel):
    SN: str
    user: str   


class SensorIP(BaseModel):
    SN:str
    ip:str


class Operate(BaseModel):
    SN: str
    activate: bool   