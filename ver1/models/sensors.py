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

class SensorLog(BaseModel):
    SN:int
    log:List[Tuple[date, int]]

class TestSensor(BaseModel):
    SN: int
    user: str   



class Operate(BaseModel):
    SN: int
    activate: bool   