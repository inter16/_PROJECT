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

    class Collection:
        name = "users"


class SigninUser(BaseModel):
    form:OAuth2PasswordRequestForm
    fcm:Optional[str]
    class Config:
        arbitrary_types_allowed = True

class SigninKakao(BaseModel):
    token:str
    fcm:Optional[str]

        
class UpdateUser(BaseModel):
    id: Optional[str]
    password: Optional[str]
    name:Optional[str]
    fcm:Optional[str]
    sensors:Optional[List[str]]



class TokenResponse(BaseModel):
    access_token: str
    token_type: str
