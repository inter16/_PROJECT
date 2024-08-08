from beanie import Document
from typing import Optional
from pydantic import BaseModel


class Sensor(Document):
    SN: int
    ip: Optional[str]
    user: Optional[str]

    class Collection:
        name = "sensors"

    class Config:
        schema_extra = {
            "example": {
                "SN": 123456789012,
                "ip": "abc123", 
                "user": "1012345678",
            }
        }

class UpdateSensor(BaseModel):
    SN: Optional[int]
    ip: Optional[str]
    user: Optional[str]

class TestSensor(BaseModel):
    SN: int
    user: str   