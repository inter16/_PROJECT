from beanie import Document
from typing import Optional, List
from pydantic import BaseModel


class User(Document):
    id: str
    password: str
    fcm:Optional[str]
    sensors:List[int]

    class Collection:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "id": 1012345678,
                "password": "abc123",
                "fcm": "asdfasdfsdfa",
                "sensors": ["ABCDEF123456","QWERTY123456"]
            }
        }

        
class UpdateUser(BaseModel):
    id: Optional[str]
    password: Optional[str]
    fcm:Optional[str]
    sensors:Optional[List[int]]

    class Collection:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "id": 1012345678,
                "password": "abc123",
                "fcm": "asdfasdfsdfa",
                "sensors": ["ABCDEF123456","QWERTY123456"]
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str