from beanie import Document
from typing import Optional, List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends


class User(Document):
    id: str
    password: str
    name:Optional[str]
    fcm:Optional[str]
    sensors:List[str]
    loc:Optional[str]

    class Collection:
        name = "users"



class SigninKakao(BaseModel):
    token:str
    fcm:Optional[str]

        
class UpdateUser(BaseModel):
    id: Optional[str]
    password: Optional[str]
    name:Optional[str]
    fcm:Optional[str]
    sensors:Optional[List[str]]
    loc:Optional[str]

