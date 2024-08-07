from beanie import Document
from typing import Optional


class Sensor(Document):
    SN: str
    ip: Optional[str]
    id:Optional[int]

    class Collection:
        name = "sensors"

    class Config:
        schema_extra = {
            "example": {
                "SN": "ABCDEF123456",
                "ip": "abc123",
                "id": 1012345678,
            }
        }
