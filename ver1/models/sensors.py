from beanie import Document
from typing import Optional, List, Tuple, Any
from pydantic import BaseModel
from datetime import date


class Sensor(Document):
    id: str
    ip: Optional[str]
    user: Optional[str]
    name: Optional[str]

    class Collection:
        name = "sensors"

    async def before_event(self):
        self.id = self.SN

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["SN"] = data.pop("_id", None)
        return data
    
    

class RegisterSensor(BaseModel):
    SN: str
    name: str  

# class UpdateSensor(BaseModel):
#     SN: Optional[str]
#     ip: Optional[str]
#     user: Optional[str]
#     name: Optional[str]

class SensorName(BaseModel):
    SN: str
    name: str   




# class SensorLog(BaseModel):
#     SN:str
#     log:List[Any]

# class TestSensor(BaseModel):
#     SN: str
#     user: str   


# class SensorIP(BaseModel):
#     SN:str
#     ip:str


# class Operate(BaseModel):
#     SN: str
#     activate: bool   